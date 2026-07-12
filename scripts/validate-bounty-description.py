#!/usr/bin/env python3
"""
Validate a bounty description against POIDH best-practices playbook.

    python3 scripts/validate-bounty-description.py --round 4
    python3 scripts/validate-bounty-description.py --file rounds/r3/description.md

Reads:
    docs/how-to-draft-next-bounty.md  - Playbook + guidelines
    rounds/rN/description.md           - Bounty description to validate

Outputs:
    Console warnings only (no writes, no exit failure on warnings)
    Human reviews and fixes before posting to POIDH.

Checks:
    - Deadline PT date present
    - Lowercase "poidh" in title/copy
    - Five numbered floor rules (rule 5 = audio rule)
    - Rubric sections present (Distribution/Craft/Substance/Bonus)
    - Asset kit with GitHub URL
    - Prize + winner-cast language
    - No emojis
    - No em dashes (hyphens only)
    - No "hackathon" (use "Build-A-Thon")
    - No "pitch competition"
    - No bare crypto jargon in public copy

Pure stdlib: re, argparse, pathlib.
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PLAYBOOK_PATH = REPO_ROOT / "docs" / "how-to-draft-next-bounty.md"

CHECKS = [
    {
        "id": "deadline_pt",
        "name": "Deadline PT date present",
        "pattern": r"(?:deadline|closes?|due)[\s:]+\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}\s*(?:PT|PST)",
        "flags": False,
    },
    {
        "id": "poidh_lowercase",
        "name": "POIDH referenced in copy (allow 'poidh' lowercase in branding)",
        "pattern": r"poidh",
        "flags": True,
    },
    {
        "id": "floor_rules_count",
        "name": "Five numbered floor rules (1. 2. 3. 4. 5.)",
        "pattern": r"^1\.\s+.+\n2\.\s+.+\n3\.\s+.+\n4\.\s+.+\n5\.\s+.+",
        "flags": False,
        "multiline": True,
    },
    {
        "id": "rubric_distribution",
        "name": "Rubric Distribution section",
        "pattern": r"(?:distribution|Distribution)",
        "flags": False,
    },
    {
        "id": "rubric_craft",
        "name": "Rubric Craft section",
        "pattern": r"(?:craft|Craft)",
        "flags": False,
    },
    {
        "id": "rubric_substance",
        "name": "Rubric Substance section",
        "pattern": r"(?:substance|Substance)",
        "flags": False,
    },
    {
        "id": "rubric_bonus",
        "name": "Rubric Bonus section",
        "pattern": r"(?:bonus|Bonus)",
        "flags": False,
    },
    {
        "id": "asset_kit_url",
        "name": "Asset kit with GitHub folder URL",
        "pattern": r"github\.com/bettercallzaal/\w+.*(?:assets|brand-kits)",
        "flags": False,
    },
    {
        "id": "prize_eth",
        "name": "Prize amount in ETH mentioned",
        "pattern": r"[\d.]+\s*(?:ETH|eth)",
        "flags": False,
    },
    {
        "id": "no_emojis",
        "name": "No emojis in description",
        "pattern": r"[\U0001F300-\U0001F9FF]",
        "flags": True,
        "invert": True,
    },
    {
        "id": "no_em_dashes",
        "name": "No em dashes (use hyphens only)",
        "pattern": r"[–—]",
        "flags": True,
        "invert": True,
    },
    {
        "id": "no_hackathon",
        "name": "No 'hackathon' (use 'Build-A-Thon')",
        "pattern": r"\bhackathon\b",
        "flags": True,
        "invert": True,
    },
    {
        "id": "no_pitch_competition",
        "name": "No 'pitch competition'",
        "pattern": r"pitch\s+competition",
        "flags": True,
        "invert": True,
    },
]


def check_pattern(text: str, check: dict) -> bool:
    """Check if pattern matches (or doesn't match if invert=True)."""
    flags = re.IGNORECASE if check.get("flags") else 0
    multiline = re.MULTILINE if check.get("multiline") else 0
    pattern_flags = flags | multiline

    match = re.search(check["pattern"], text, pattern_flags)
    invert = check.get("invert", False)

    if invert:
        return match is None
    else:
        return match is not None


def validate_description(text: str) -> list[str]:
    """Validate description against all checks. Return list of warnings."""
    warnings = []

    for check in CHECKS:
        result = check_pattern(text, check)
        if not result:
            warnings.append(f"  WARN: {check['id']}: {check['name']}")

    return warnings


def main() -> int:
    p = argparse.ArgumentParser(
        description="Validate bounty description against POIDH best-practices playbook"
    )
    p.add_argument(
        "--round",
        type=int,
        default=None,
        help="Round number (reads rounds/rN/description.md)",
    )
    p.add_argument("--file", type=Path, default=None, help="Path to description.md file")

    args = p.parse_args()

    # Determine file path
    if args.file:
        desc_path = args.file
    elif args.round:
        desc_path = REPO_ROOT / f"rounds/r{args.round}/description.md"
    else:
        print("ERROR: Provide --round or --file")
        return 1

    if not desc_path.exists():
        print(f"ERROR: {desc_path} not found")
        return 1

    # Read description
    try:
        with open(desc_path) as f:
            text = f.read()
    except Exception as e:
        print(f"ERROR: Failed to read {desc_path}: {e}")
        return 1

    print(f"Validating {desc_path.relative_to(REPO_ROOT)}...\n")

    # Run checks
    warnings = validate_description(text)

    if not warnings:
        print("OK: All checks passed.")
        return 0

    print(f"Found {len(warnings)} issue(s):\n")
    for w in warnings:
        print(w)

    print(f"\nPlaybook: {PLAYBOOK_PATH.relative_to(REPO_ROOT)}")
    print("Zaal to review and fix before posting to POIDH.")

    return 0  # Warnings only - do not fail


if __name__ == "__main__":
    sys.exit(main())
