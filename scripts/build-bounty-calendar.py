#!/usr/bin/env python3
"""
Proof-of-concept for the POID bounty deadline calendar (zpoidh issue #6, from the
2026-07-08 ZABAL Gamez x POIDH fireside - ZAO OS V1 doc 994).

POID bounties have no structured, on-chain deadline field by design (a philosophical
choice per Kenny - social standard, not smart-contract enforced). But bounty creators
write a deadline into the free-text description anyway. This script proves the idea on
data we already control - BCZ's own R1-R4 bounties - before generalizing to arbitrary
POID bounties: it pulls each bounty's raw description via POID's tRPC, regex-extracts
the stated deadline date out of free text, and writes one JSON file a calendar view can
render. Bounties with no parseable deadline are flagged, not silently dropped.

    python3 scripts/build-bounty-calendar.py

Writes data/bounty-calendar.json.
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POIDH_BASE = "https://poidh.xyz/api/trpc"
UA = "Mozilla/5.0 (zpoidh-bounty-calendar)"

# BCZ's own rounds - the known-data proof set. R5 has no bounty id yet (not cast).
ROUNDS = [
    {"round": 1, "bounty_id": 1151, "title": "R1 - Hannah Ep 17 clip-up"},
    {"round": 2, "bounty_id": 1166, "title": "R2 - Best 60s POIDH ad from Ep 19"},
    {"round": 3, "bounty_id": 1180, "title": "R3 - Best ad for ZABAL Gamez"},
    {"round": 4, "bounty_id": 1249, "title": "R4 - ZABAL Gamez open pot"},
]

MONTHS = (
    "January|February|March|April|May|June|July|August|September|October|November|December"
)
# Matches "May 4, 2026", "June 14, 2026", "July 31, 2026" etc, case-sensitive on the
# month name (as POID descriptions are written in normal prose).
DATE_RE = re.compile(rf"({MONTHS})\s+(\d{{1,2}}),?\s*(\d{{4}})")


def trpc(proc: str, payload: dict) -> dict:
    inp = urllib.parse.quote(json.dumps({"0": {"json": payload}}))
    req = urllib.request.Request(
        f"{POIDH_BASE}/{proc}?batch=1&input={inp}", headers={"User-Agent": UA}
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())[0]["result"]["data"]["json"]


def extract_deadline(description: str) -> tuple[str | None, str | None]:
    """Find the free-text deadline in a bounty description.

    Looks for the word "deadline" (case-insensitive) and reads the first
    Month-DD-YYYY date after it. Falls back to scanning the whole description for
    any date at all, since not every bounty labels the section "DEADLINE" (R1's
    reads "Deadline to enter ..." inline, not as its own section).
    Returns (iso_date_or_None, raw_matched_text_or_None).
    """
    lower = description.lower()
    idx = lower.find("deadline")
    window = description[idx : idx + 300] if idx >= 0 else description
    m = DATE_RE.search(window)
    if not m:
        m = DATE_RE.search(description)
    if not m:
        return None, None
    month_name, day, year = m.group(1), int(m.group(2)), int(m.group(3))
    try:
        dt = datetime.strptime(f"{month_name} {day} {year}", "%B %d %Y").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        return None, m.group(0)
    return dt.date().isoformat(), m.group(0)


def main() -> int:
    now = datetime.now(timezone.utc).date()
    entries = []

    for r in ROUNDS:
        try:
            b = trpc("bounties.fetch", {"id": r["bounty_id"], "chainId": 8453})
        except Exception as e:
            print(f"  WARN: could not fetch bounty {r['bounty_id']}: {e}")
            entries.append(
                {
                    **r,
                    "deadline_iso": None,
                    "deadline_raw_text": None,
                    "status": "fetch_failed",
                    "url": f"https://poidh.xyz/base/bounty/{r['bounty_id']}",
                }
            )
            continue

        deadline_iso, raw = extract_deadline(b.get("description", ""))
        status = "no_deadline_found"
        if deadline_iso:
            status = "closed" if deadline_iso < now.isoformat() else "upcoming"

        entries.append(
            {
                "round": r["round"],
                "bounty_id": r["bounty_id"],
                "title": r["title"],
                "deadline_iso": deadline_iso,
                "deadline_raw_text": raw,
                "status": status,
                "url": f"https://poidh.xyz/base/bounty/{r['bounty_id']}",
            }
        )
        print(f"  R{r['round']} (bounty {r['bounty_id']}): {deadline_iso or 'NOT FOUND'} <- {raw!r}")

    # R5 is drafted but not cast - no bounty id, so no tRPC fetch is possible. Include
    # it as a placeholder row so the calendar doesn't silently omit a known round.
    entries.append(
        {
            "round": 5,
            "bounty_id": None,
            "title": "R5 - POIDH x Unlock Protocol clip bounty",
            "deadline_iso": None,
            "deadline_raw_text": None,
            "status": "not_cast",
            "url": None,
        }
    )

    entries.sort(key=lambda e: e["deadline_iso"] or "9999-99-99")

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "note": (
            "Proof-of-concept for zpoidh issue #6 - deadlines are parsed from each "
            "bounty's free-text description via POID's tRPC, not read from a "
            "structured on-chain field (POID intentionally has none). Built against "
            "BCZ's own R1-R4 bounties first; generalizing to arbitrary POID bounties "
            "is a follow-up, not done here."
        ),
        "bounties": entries,
    }

    out_path = REPO_ROOT / "data" / "bounty-calendar.json"
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
