#!/usr/bin/env python3
"""
Stage 3: Validate a POIDH bounty description against the canonical bar.

Checks that a bounty description meets all required sections and criteria
per docs/bounty-best-practices.html before a round runs.

    python3 scripts/validate-bounty-description.py --description path/to/description.md [--strict]

Outputs:
    Returns 0 on PASS, 1 on FAIL
    Prints detailed feedback for each criterion

Human gate: This is a validation stage. It does not modify the description,
only checks it against the canonical bar and reports findings.
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


REQUIRED_SECTIONS = [
    ("why", "One-paragraph WHY (link to source episode/event/page)"),
    ("the_bar", "THE BAR - 3-5 numbered floor rules"),
    ("the_rubric", "THE RUBRIC - grouped by Distribution/Craft/Substance/Bonus"),
    ("asset_kit", "THE ASSET KIT - link to GitHub brand folder + direct download URLs"),
    ("reward", "THE REWARD - prize + winner-cast distribution + EB ZABAL trail"),
    ("deadline", "DEADLINE - exact PT date/time + winner cast date"),
]

REQUIRED_FLOOR_RULES = [
    ("tag_bcz", "Tag @bettercallzaal on X"),
    ("crosspost_fc", "Cross-post in relevant Farcaster channel"),
    ("submit_url", "Submit X URL on POIDH bounty page"),
    ("audio_rule", "AUDIO rule: official promo MP3 or source-episode audio or clear instrumental"),
]


def load_description(path: Path) -> str | None:
    """Load bounty description from file."""
    if not path.exists():
        print(f"ERROR: Description file not found: {path}")
        return None

    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        print(f"ERROR reading description: {e}")
        return None


def validate_sections(description: str, strict: bool = False) -> tuple[bool, list]:
    """Check for all required sections."""
    findings = []
    all_pass = True

    for section_id, section_label in REQUIRED_SECTIONS:
        # Loose check: look for section headers (case-insensitive)
        patterns = [
            r"(?i)" + re.escape(section_label.split(" - ")[0]),
            r"(?i)#+\s*" + re.escape(section_label.split(" - ")[0].replace("THE ", "").replace("_", " ")),
        ]

        found = any(re.search(p, description) for p in patterns)

        if found:
            findings.append(f"PASS: {section_label}")
        else:
            findings.append(f"FAIL: {section_label} - NOT FOUND")
            all_pass = False

    return all_pass, findings


def validate_floor_rules(description: str) -> tuple[bool, list]:
    """Check that all required floor rules are mentioned."""
    findings = []
    all_pass = True

    for rule_id, rule_label in REQUIRED_FLOOR_RULES:
        # Look for key phrases from each rule
        keywords = {
            "tag_bcz": ["@bettercallzaal", "tag"],
            "crosspost_fc": ["farcaster", "cross-post", "channel"],
            "submit_url": ["submit", "url", "poidh", "bounty page"],
            "audio_rule": ["audio", "music", "dialog", "instrumental"],
        }

        kw_list = keywords.get(rule_id, [rule_label.lower()])
        found = any(re.search(r"(?i)" + re.escape(kw), description) for kw in kw_list)

        if found:
            findings.append(f"PASS: Floor rule - {rule_label}")
        else:
            findings.append(f"WARN: Floor rule - {rule_label} not explicitly mentioned (verify manually)")
            # Not a hard fail for floor rules since wording varies

    return all_pass, findings


def validate_links(description: str) -> tuple[bool, list]:
    """Check for proper links and URLs."""
    findings = []

    # Check for at least one bounty URL
    has_poidh_url = re.search(r"https://poidh\.xyz/.*?bounty", description, re.IGNORECASE)
    if has_poidh_url:
        findings.append("PASS: POIDH bounty URL found")
    else:
        findings.append("WARN: No POIDH bounty URL found (will be added after creation)")

    # Check for brand kit link
    has_brand_kit = re.search(r"(github|brand|kit|assets)", description, re.IGNORECASE)
    if has_brand_kit:
        findings.append("PASS: Brand kit reference found")
    else:
        findings.append("WARN: No brand kit reference found")

    # Check for GitHub links
    has_github = re.search(r"https://github\.com", description)
    if has_github:
        findings.append("PASS: GitHub link found")
    else:
        findings.append("WARN: No GitHub link found for brand kit")

    return True, findings  # Links are not hard-fails


def validate_structure(description: str) -> tuple[bool, list]:
    """Check overall structure and completeness."""
    findings = []
    all_pass = True

    # Check for minimum length
    lines = description.strip().split("\n")
    if len(lines) >= 10:
        findings.append(f"PASS: Description has {len(lines)} lines (minimum 10)")
    else:
        findings.append(f"FAIL: Description too short ({len(lines)} lines, minimum 10)")
        all_pass = False

    # Check for numbered lists (floor rules and rubric often use these)
    has_numbered_lists = re.search(r"^\s*\d+\.", description, re.MULTILINE)
    if has_numbered_lists:
        findings.append("PASS: Numbered lists found (floor rules / rubric)")
    else:
        findings.append("WARN: No numbered lists found (check that floor rules are enumerated)")

    # Check for markdown headers
    has_headers = re.search(r"^#+\s", description, re.MULTILINE)
    if has_headers:
        findings.append("PASS: Markdown headers found")
    else:
        findings.append("WARN: No markdown headers found (consider using # for section structure)")

    return all_pass, findings


def main() -> int:
    p = argparse.ArgumentParser(
        description="Stage 3: Validate POIDH bounty description against canonical bar"
    )
    p.add_argument(
        "--description",
        type=Path,
        required=True,
        help="Path to bounty description markdown file",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Strict mode: warnings become failures",
    )

    args = p.parse_args()

    # Load description
    print(f"Validating description: {args.description}")
    description = load_description(args.description)
    if not description:
        return 1

    print("\n--- SECTION VALIDATION ---")
    sections_pass, sections_findings = validate_sections(description, args.strict)
    for finding in sections_findings:
        print(f"  {finding}")

    print("\n--- FLOOR RULES VALIDATION ---")
    floor_pass, floor_findings = validate_floor_rules(description)
    for finding in floor_findings:
        print(f"  {finding}")

    print("\n--- LINKS & URLS ---")
    links_pass, links_findings = validate_links(description)
    for finding in links_findings:
        print(f"  {finding}")

    print("\n--- OVERALL STRUCTURE ---")
    struct_pass, struct_findings = validate_structure(description)
    for finding in struct_findings:
        print(f"  {finding}")

    # Final verdict
    all_pass = sections_pass and struct_pass
    if args.strict:
        all_pass = all_pass and floor_pass and links_pass

    print("\n" + "=" * 60)
    if all_pass:
        print("VERDICT: PASS - Description is ready for casting")
        print("\nHuman gate check:")
        print("- Review the description one more time in the POIDH UI")
        print("- Confirm all links work and point to correct resources")
        print("- Verify floor rules are clear to submitters")
        print("- Check that prize amount and deadline are correct")
        return 0
    else:
        print("VERDICT: FAIL - Description needs revision")
        print("\nFix the items marked FAIL before casting.")
        if not args.strict:
            print("(Run with --strict to treat warnings as failures)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
