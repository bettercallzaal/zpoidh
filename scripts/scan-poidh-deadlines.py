#!/usr/bin/env python3
"""
Generalized POID bounty deadline scanner (zpoidh issue #6, the follow-up beyond BCZ's
own rounds). scripts/build-bounty-calendar.py proved the free-text parsing approach
against 4 known BCZ bounties; this scans the live, platform-wide POID bounty feed
(bounties.fetchAll) so the calendar isn't limited to bounties we already know about.

Confirms Kenny's exact point from the 2026-07-08 fireside: POID's own `deadline` field
on a bounty object is essentially unused - it comes back `null` on real bounties even
when the description explicitly states one ("Submissions close on July 5, 2026").
There genuinely is no structured deadline; the only source of truth is free text.

    python3 scripts/scan-poidh-deadlines.py [--pages 4] [--limit 25] [--status open]

Writes data/poidh-deadlines-global.json.
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POIDH_BASE = "https://poidh.xyz/api/trpc"
UA = "Mozilla/5.0 (zpoidh-bounty-deadline-scanner)"

MONTHS = (
    "January|February|March|April|May|June|July|August|September|October|November|December"
)
DATE_RE = re.compile(rf"({MONTHS})\s+(\d{{1,2}}),?\s*(\d{{4}})")

# Words that actually signal a submission cutoff. Word-boundary matched so
# "due" does not fire inside "residue"/"produce". A date only counts as a
# deadline when it sits shortly AFTER one of these.
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
    """Return (iso_date, raw_text) for the submission deadline, or (None, None).

    A date only counts as a deadline when it appears within ~300 chars AFTER a
    deadline-signalling keyword (deadline / closes / due / ends / submit by / ...),
    trying each keyword occurrence in text order. We deliberately do NOT grab an
    arbitrary date from elsewhere in the text: that produced false positives, e.g.
    an event kickoff date ("kickoff on August 5") being reported as the submission
    deadline even when the text says "no deadline stated". Per this tool's own
    framing, "no stated deadline -> just don't show it".
    """
    for hit in DEADLINE_RE.finditer(description):
        m = DATE_RE.search(description[hit.start() : hit.start() + 300])
        if m:
            return _parse_match(m)
    return None, None


def selftest() -> int:
    """Guard the deadline parser against the false-positive it used to have.
    Run: python3 scripts/scan-poidh-deadlines.py --selftest"""
    cases = [
        # (description, expected_iso)
        ("Build a game. Event kickoff on August 5, 2026. No deadline stated.", None),
        ("Submissions close on July 5, 2026. Prizes paid after.", "2026-07-05"),
        ("Deadline: submissions due August 12, 2026.", "2026-08-12"),
        ("This bounty ends September 1, 2026 at midnight.", "2026-09-01"),
        ("Submit by October 3, 2026 to qualify.", "2026-10-03"),
        ("Prize pool. Judging happens live, winners announced later.", None),
        ("Launched June 2024, still open.", None),  # no day -> not a date match
    ]
    fails = 0
    for desc, want in cases:
        got, _ = extract_deadline(desc)
        ok = got == want
        fails += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} want={want!r:>14} got={got!r:>14}  <- {desc[:52]}")
    total = len(cases)
    print(f"selftest: {total - fails}/{total} passed")
    return 1 if fails else 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--selftest", action="store_true", help="run the deadline-parser self-test and exit")
    p.add_argument("--pages", type=int, default=4, help="how many pages of the live feed to scan")
    p.add_argument("--limit", type=int, default=25, help="bounties per page")
    p.add_argument("--status", default="open", choices=["open", "progress", "past"])
    p.add_argument("--chain", type=int, default=8453)
    args = p.parse_args()

    if args.selftest:
        return selftest()

    now = datetime.now(timezone.utc).date()
    scanned = []
    native_deadline_field_ever_set = 0
    cursor = None

    for page in range(args.pages):
        payload = {"chainId": args.chain, "status": args.status, "limit": args.limit}
        if cursor is not None:
            payload["cursor"] = cursor
        try:
            d = trpc("bounties.fetchAll", payload)
        except Exception as e:
            print(f"  WARN: page {page} fetch failed: {e}")
            break

        items = d.get("items", [])
        if not items:
            break
        cursor = d.get("nextCursor")

        for b in items:
            if b.get("deadline") is not None:
                native_deadline_field_ever_set += 1

            deadline_iso, raw = extract_deadline(b.get("description", ""))
            if not deadline_iso:
                continue  # per Kenny's own framing: no stated deadline -> just don't show it

            scanned.append(
                {
                    "bounty_id": b["id"],
                    "title": b.get("title", "")[:120],
                    "issuer": b.get("issuer"),
                    "amount_eth": int(b.get("amount", "0") or 0) / 1e18,
                    "deadline_iso": deadline_iso,
                    "deadline_raw_text": raw,
                    "status": "closed" if deadline_iso < now.isoformat() else "upcoming",
                    "url": f"https://poidh.xyz/base/bounty/{b['id']}",
                }
            )

        if cursor is None:
            break  # fetchAll's nextCursor is absent on the last page - end of feed

        time.sleep(0.3)  # courtesy delay - this is someone else's public API

    scanned.sort(key=lambda e: e["deadline_iso"])

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scan_status": args.status,
        "pages_scanned": args.pages,
        "note": (
            "Generalized scan beyond BCZ's own rounds (see build-bounty-calendar.py for "
            "the BCZ-specific proof of concept). Confirms POID's on-chain/API `deadline` "
            f"field is essentially unused in practice - only {native_deadline_field_ever_set} "
            f"of the bounties scanned had it set at all, even though many describe a clear "
            "deadline in free text. That gap is exactly why this tool exists."
        ),
        "bounties_with_deadline_found": scanned,
    }

    out_path = REPO_ROOT / "data" / "poidh-deadlines-global.json"
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Scanned {args.pages} page(s) of '{args.status}' bounties, found {len(scanned)} with a parseable deadline.")
    print(f"Native 'deadline' field was set on {native_deadline_field_ever_set} bounties out of the scan.")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
