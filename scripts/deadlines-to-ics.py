#!/usr/bin/env python3
"""Turn the parsed POID bounty deadlines into a subscribable .ics calendar.

The deadline scanners (scan-poidh-deadlines.py, build-bounty-calendar.py) write
JSON; this converts that JSON into an RFC-5545 iCalendar so anyone can subscribe
in Google/Apple Calendar and never miss a bounty deadline (a missed deadline is a
lost submission - this feeds the ZABAL Gamez / tokenless-empire funnel). One
all-day VEVENT per bounty that has a parseable deadline.

    python3 scripts/deadlines-to-ics.py [--in data/poidh-deadlines-global.json]
                                        [--out data/poidh-deadlines.ics]
    python3 scripts/deadlines-to-ics.py --selftest   # no files, no network

Input JSON shape (either scanner's output works): a list under
`bounties_with_deadline_found` (global scan) or `entries` (BCZ calendar), each
with deadline_iso, title, url, and optionally bounty_id / amount_eth /
deadline_raw_text.
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _esc(text: str) -> str:
    """RFC 5545 TEXT escaping: backslash, comma, semicolon, newline."""
    s = str(text or "")
    s = s.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;")
    return s.replace("\r\n", "\\n").replace("\n", "\\n")


def _fold(line: str) -> str:
    """RFC 5545 line folding at 75 octets (continuation lines start with a space)."""
    if len(line) <= 75:
        return line
    out, rest = line[:75], line[75:]
    while rest:
        out += "\r\n " + rest[:74]
        rest = rest[74:]
    return out


def entries_from(data: dict) -> list[dict]:
    return data.get("bounties_with_deadline_found") or data.get("entries") or []


def build_ics(entries: list[dict], dtstamp: str) -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//zpoidh//POID bounty deadlines//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:POID Bounty Deadlines",
    ]
    for e in entries:
        iso = e.get("deadline_iso")
        if not iso:
            continue
        date = iso[:10].replace("-", "")  # YYYYMMDD, all-day event
        uid = f"poidh-{e.get('bounty_id') or date}-{abs(hash(e.get('url') or e.get('title') or iso)) % 10**8}@zpoidh"
        amount = e.get("amount_eth")
        desc_bits = []
        if e.get("deadline_raw_text"):
            desc_bits.append(f"Stated: {e['deadline_raw_text']}")
        if amount:
            desc_bits.append(f"{amount} ETH")
        if e.get("url"):
            desc_bits.append(e["url"])
        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{dtstamp}",
            f"DTSTART;VALUE=DATE:{date}",
            _fold(f"SUMMARY:{_esc((e.get('title') or 'POID bounty') + ' - deadline')}"),
        ]
        if desc_bits:
            lines.append(_fold(f"DESCRIPTION:{_esc(' - '.join(desc_bits))}"))
        if e.get("url"):
            lines.append(_fold(f"URL:{_esc(e['url'])}"))
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def _selftest() -> int:
    entries = [
        {"bounty_id": 1249, "title": "ZABAL Gamez open pot", "deadline_iso": "2026-07-31",
         "url": "https://poidh.xyz/base/bounty/1249", "amount_eth": 0.05,
         "deadline_raw_text": "closes July 31, 2026; semicolons, commas & \\ backslashes"},
        {"title": "no-deadline entry"},  # skipped (no deadline_iso)
    ]
    ics = build_ics(entries, "20260717T000000Z")
    checks = [
        ("valid VCALENDAR envelope", ics.startswith("BEGIN:VCALENDAR") and ics.rstrip().endswith("END:VCALENDAR")),
        ("one VEVENT (no-deadline entry skipped)", ics.count("BEGIN:VEVENT") == 1),
        ("all-day DTSTART formatted YYYYMMDD", "DTSTART;VALUE=DATE:20260731" in ics),
        # unit-test the escaper directly (checking the folded .ics for substrings is
        # unreliable - RFC-5545 folding can split them across a "\r\n " boundary)
        ("TEXT escaping (backslash/comma/semicolon/newline)",
         _esc("a, b; c\\ d\ne") == "a\\, b\\; c\\\\ d\\ne"),
        ("CRLF line endings", "\r\n" in ics),
        ("URL carried through", "https://poidh.xyz/base/bounty/1249" in ics),
    ]
    fails = 0
    for label, ok in checks:
        fails += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    print(f"selftest: {len(checks) - fails}/{len(checks)} passed")
    return 1 if fails else 0


def main() -> int:
    from datetime import datetime, timezone
    p = argparse.ArgumentParser()
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--in", dest="inp", default=str(REPO_ROOT / "data" / "poidh-deadlines-global.json"))
    p.add_argument("--out", default=str(REPO_ROOT / "data" / "poidh-deadlines.ics"))
    args = p.parse_args()
    if args.selftest:
        return _selftest()
    try:
        data = json.load(open(args.inp))
    except FileNotFoundError:
        print(f"error: {args.inp} not found - run scan-poidh-deadlines.py first", file=sys.stderr)
        return 2
    entries = entries_from(data)
    dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ics = build_ics(entries, dtstamp)
    Path(args.out).write_text(ics)
    n = ics.count("BEGIN:VEVENT")
    print(f"wrote {args.out} ({n} deadline event(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
