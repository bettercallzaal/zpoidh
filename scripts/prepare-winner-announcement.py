#!/usr/bin/env python3
"""
Stage 4: Prepare winner announcement draft.

Assembles winner announcement content (who won, why, score) as a DRAFT for human review.
Does NOT post the announcement - that stays human-gated. Outputs a structured JSON draft
+ a plaintext version for review.

    python3 scripts/prepare-winner-announcement.py --round 3

Outputs:
    rounds/r{N}/winner-announcement-DRAFT.json  - structured draft data
    rounds/r{N}/winner-announcement-DRAFT.txt   - plaintext version for copy/paste

Human gates:
- Winner PICK is human (not algorithmic) - this script uses the human's choice from judging.json
- Posting/publishing is human - this script only generates a DRAFT
- On-chain payout is human - announcement prep does not trigger payout
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_judging_json(round_num: int) -> dict | None:
    """Load judging.json for a given round."""
    judging_path = REPO_ROOT / f"rounds/r{round_num}/judging.json"
    if not judging_path.exists():
        print(f"ERROR: {judging_path} not found")
        return None

    try:
        with open(judging_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading judging.json: {e}")
        return None


def find_winner(submissions: list) -> dict | None:
    """Find the winner from submissions (marked winner=true)."""
    for sub in submissions:
        if sub.get("winner"):
            return sub
    return None


def build_draft(judging: dict, winner: dict, round_num: int) -> dict:
    """Build announcement draft."""

    bounty_id = judging.get("bounty_id")
    bounty_title = judging.get("bounty_title", "POIDH Bounty")
    bounty_url = judging.get("bounty_url")
    amount_eth = judging.get("amount_eth_at_judging", 0)

    claim_id = winner.get("claim_id", "?")
    fc_handle = winner.get("fc_handle", "unknown")
    display_name = winner.get("display_name", fc_handle)
    wallet = winner.get("wallet", "")
    x_url = winner.get("x_url", "")
    title = winner.get("title", "Untitled")
    rubric_score = winner.get("rubric_score", {})

    # Build why section
    why_lines = []
    if rubric_score.get("distribution"):
        why_lines.append(f"Distribution: {rubric_score['distribution']}")
    if rubric_score.get("craft"):
        why_lines.append(f"Craft: {rubric_score['craft']}")
    if rubric_score.get("substance"):
        why_lines.append(f"Substance: {rubric_score['substance']}")
    if rubric_score.get("bonus"):
        why_lines.append(f"Bonus: {rubric_score['bonus']}")

    why_text = "\n".join(why_lines) if why_lines else "Rubric scores not yet filled in judging.json"

    draft = {
        "status": "DRAFT - NOT POSTED",
        "timestamp": None,  # Human to fill
        "round": round_num,
        "bounty_id": bounty_id,
        "bounty_url": bounty_url,
        "bounty_title": bounty_title,
        "prize_eth": amount_eth,
        "winner": {
            "claim_id": claim_id,
            "farcaster_handle": fc_handle,
            "display_name": display_name,
            "wallet": wallet,
            "x_post_url": x_url,
            "submission_title": title,
        },
        "why_winner": why_text,
        "next_steps": [
            "REVIEW THIS DRAFT - verify winner details and reasoning are correct",
            "PICK MEDIA - choose a screenshot or thumbnail from the winning submission",
            "DRAFT CAST - write the congratulations message in your own voice",
            "CROSS-POST - plan where to share (X, Farcaster, etc.)",
            "POST CAST - Zaal posts the cast with media embed",
            "CONFIRM ON-CHAIN - verify on-chain payout (human action, not automated)",
        ],
        "templates": {
            "farcaster_cast": f"""Congratulations to {fc_handle}! Your entry for POIDH Round {round_num} ({bounty_title}) won the {amount_eth} ETH prize.

[EMBED SUBMISSION VIDEO/IMAGE]

Reason: [ADD YOUR REASONING - refer to rubric above]

You've earned a slot in $ZABAL leaderboard. Details: [bounty URL]""",
            "x_post": f"""Big congrats to @{fc_handle.lstrip('@')}! Your POIDH Round {round_num} entry ({bounty_title}) took the top prize.

[EMBED SUBMISSION VIDEO]

Here's why it won: [ADD YOUR REASONING]

Check it out: {bounty_url}""",
        },
    }

    return draft


def build_plaintext_draft(draft: dict) -> str:
    """Build plaintext version for copy/paste review."""

    w = draft["winner"]
    text = f"""POIDH ROUND {draft['round']} - WINNER ANNOUNCEMENT DRAFT
{'=' * 70}

STATUS: {draft['status']}

BOUNTY:
  ID: {draft['bounty_id']}
  Title: {draft['bounty_title']}
  Prize: {draft['prize_eth']} ETH
  URL: {draft['bounty_url']}

WINNER:
  Claim ID: {w['claim_id']}
  Farcaster: @{w['farcaster_handle']}
  Display Name: {w['display_name']}
  Wallet: {w['wallet']}
  Submission: {w['submission_title']}
  X Post: {w['x_post_url']}

WHY THEY WON:
{draft['why_winner']}

NEXT STEPS TO PUBLISH:
{chr(10).join(f"  {i+1}. {step}" for i, step in enumerate(draft['next_steps']))}

SUGGESTED FARCASTER CAST:
{'-' * 70}
{draft['templates']['farcaster_cast']}
{'-' * 70}

SUGGESTED X POST:
{'-' * 70}
{draft['templates']['x_post']}
{'-' * 70}

HUMAN GATES (preserved):
  - Winner pick: HUMAN (this draft uses your choice from judging.json)
  - Announcement text: HUMAN (use templates above as guides, write in your own voice)
  - Media selection: HUMAN (pick screenshot/thumbnail)
  - Publishing: HUMAN (you post the cast, not automated)
  - On-chain payout: HUMAN (verify manually after posting)

Generated by: scripts/prepare-winner-announcement.py (Stage 4)
Action: Review this draft. Customize templates. Post when ready (manual step).
"""

    return text


def main() -> int:
    p = argparse.ArgumentParser(
        description="Stage 4: Prepare winner announcement draft (not posted)"
    )
    p.add_argument("--round", type=int, required=True, help="Round number")

    args = p.parse_args()

    # Load judging.json
    print(f"Loading judging data for round {args.round}...")
    judging = load_judging_json(args.round)
    if not judging:
        return 1

    submissions = judging.get("submissions", [])

    # Find winner
    print("Finding winner...")
    winner = find_winner(submissions)
    if not winner:
        print("ERROR: No winner marked in judging.json (set winner=true for one submission)")
        return 1

    print(f"Winner: @{winner.get('fc_handle')} (claim {winner.get('claim_id')})")

    # Build draft
    print("Building announcement draft...")
    draft = build_draft(judging, winner, args.round)

    # Write JSON draft
    round_dir = REPO_ROOT / f"rounds/r{args.round}"
    round_dir.mkdir(parents=True, exist_ok=True)

    json_path = round_dir / "winner-announcement-DRAFT.json"
    with open(json_path, "w") as f:
        json.dump(draft, f, indent=2)
        f.write("\n")
    print(f"Wrote {json_path.relative_to(REPO_ROOT)}")

    # Write plaintext draft
    plaintext = build_plaintext_draft(draft)
    txt_path = round_dir / "winner-announcement-DRAFT.txt"
    with open(txt_path, "w") as f:
        f.write(plaintext)
    print(f"Wrote {txt_path.relative_to(REPO_ROOT)}")

    print("\n" + "=" * 60)
    print("ANNOUNCEMENT DRAFT READY")
    print("=" * 60)
    print(f"\nReview the plaintext version for quick reading:")
    print(f"  {txt_path}")
    print(f"\nStructured data for programmatic use:")
    print(f"  {json_path}")
    print("\nNext steps:")
    print("  1. Review the draft and fix any errors in reasoning")
    print("  2. Customize the cast templates with your own voice")
    print("  3. Pick media to embed (screenshot or thumbnail)")
    print("  4. Post the cast (manual, human action)")
    print("  5. Verify on-chain payout (manual, human action)")
    print("\nHuman gates preserved:")
    print("  - Winner pick is from your judging.json (not algorithmic)")
    print("  - Posting is manual (not automated)")
    print("  - Payout is manual (not triggered by this script)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
