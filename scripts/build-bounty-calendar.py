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

# Words that actually signal a submission cutoff. Word-boundary matched so "due"
# does not fire inside "residue"/"produce". A date only counts as a deadline when
# it sits shortly AFTER one of these. (Mirrors scan-poidh-deadlines.py; once that
# fix merges these two parsers should share one module - see zpoidh issue #6.)
DEADLINE_RE = re.compile(
    r"\b(?:deadline|closes?|closing|due|ends?|ending|submit\s+by|until)\b",
    re.IGNORECASE,
)


def trpc(proc: str, payload: dict) -> dict:
    inp = urllib.parse.quote(json.dumps({"0": {"json": payload}}))
    req = urllib.request.Request(
        f"{POIDH_BASE}/{proc}?batch=1&input={inp}", headers={"User-Agent": UA}
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())[0]["result"]["data"]["json"]


def _parse_match(m: "re.Match[str]") -> tuple[str | None, str | None]:
    month_name, day, year = m.group(1), int(m.group(2)), int(m.group(3))
    try:
        dt = datetime.strptime(f"{month_name} {day} {year}", "%B %d %Y").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        return None, m.group(0)
    return dt.date().isoformat(), m.group(0)


def extract_deadline(description: str) -> tuple[str | None, str | None]:
    """Find the free-text submission deadline in a bounty description.

    A date only counts as a deadline when it appears within ~300 chars AFTER a
    deadline-signalling keyword (deadline / closes / due / ends / submit by / ...),
    tried in text order. We do NOT fall back to grabbing an arbitrary date from
    elsewhere in the text: that mislabelled unrelated dates (e.g. an event kickoff
    "August 5") as the deadline even when the text said "no deadline stated".
    Returns (iso_date_or_None, raw_matched_text_or_None).
    """
    for hit in DEADLINE_RE.finditer(description):
        m = DATE_RE.search(description[hit.start() : hit.start() + 300])
        if m:
            return _parse_match(m)
    return None, None


def _selftest() -> int:
    """Guard the deadline parser against the false-positive it used to have.
    Run: python3 scripts/build-bounty-calendar.py --selftest"""
    cases = [
        ("Build a game. Event kickoff on August 5, 2026. No deadline stated.", None),
        ("Submissions close on July 5, 2026. Prizes paid after.", "2026-07-05"),
        ("Deadline to enter is August 12, 2026.", "2026-08-12"),
        ("This bounty ends September 1, 2026.", "2026-09-01"),
        ("Prize pool. Judging happens live.", None),
    ]
    fails = 0
    for desc, want in cases:
        got, _ = extract_deadline(desc)
        ok = got == want
        fails += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} want={want!r:>14} got={got!r:>14}  <- {desc[:50]}")
    print(f"selftest: {len(cases) - fails}/{len(cases)} passed")
    return 1 if fails else 0


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()

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
