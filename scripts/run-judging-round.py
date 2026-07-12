#!/usr/bin/env python3
"""
Stage 5: Full run-round orchestrator.

Chains stages 1-4 together into one "run a judging round" flow:
  1. Process judging videos (download, extract duration, scaffold judging.json)
  2. Render HTML scorecard for review
  3. Validate bounty description
  4. Prepare winner announcement (if judging complete)

Does NOT automate any human-gated actions:
  - Rubric scoring is manual (Zaal fills scores in judging.json)
  - Winner selection is manual (Zaal picks winner, marks in judging.json)
  - Posting/announcing is manual
  - On-chain payout is manual

    python3 scripts/run-judging-round.py --bounty 1166 --round 2 --description rounds/r2/description.md

Outputs:
    rounds/r{N}/durations.json              - from stage 1
    rounds/r{N}/judging.json                - scaffold with floor checks (stage 1)
    rounds/r{N}/judging.html                - rendered scorecard (stage 2)
    rounds/r{N}/winner-announcement-DRAFT.* - if winner marked (stage 4)
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_stage(name: str, script: str, args: list) -> bool:
    """Run a stage script."""
    print(f"\n{'=' * 60}")
    print(f"STAGE: {name}")
    print('=' * 60)

    script_path = REPO_ROOT / "scripts" / script
    if not script_path.exists():
        print(f"ERROR: {script} not found")
        return False

    try:
        result = subprocess.run(
            ["python3", str(script_path)] + args,
            cwd=REPO_ROOT,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"ERROR running {script}: {e}")
        return False


def main() -> int:
    p = argparse.ArgumentParser(
        description="Stage 5: Full orchestrator - chains stages 1-4 for a complete judging round"
    )
    p.add_argument("--bounty", type=int, required=True, help="POIDH bounty ID")
    p.add_argument("--round", type=int, required=True, help="Round number")
    p.add_argument(
        "--description",
        type=Path,
        default=None,
        help="Path to bounty description file (for validation in stage 3)",
    )
    p.add_argument(
        "--skip-stage",
        type=int,
        action="append",
        default=[],
        help="Skip a stage (e.g. --skip-stage 1 --skip-stage 3)",
    )
    p.add_argument(
        "--media-urls",
        type=Path,
        default=None,
        help="Optional JSON file mapping claim_id to video.twimg.com URLs (stage 1)",
    )

    args = p.parse_args()

    print(f"\nPOIDH Judging Round Orchestrator")
    print(f"Bounty: {args.bounty}, Round: {args.round}")
    print(f"Stages to run: 1, 2, 3, 4")

    # Stage 1: Process judging videos
    if 1 not in args.skip_stage:
        stage1_args = [
            "--bounty", str(args.bounty),
            "--round", str(args.round),
        ]
        if args.media_urls:
            stage1_args.extend(["--media-urls", str(args.media_urls)])

        if not run_stage("1: Process Judging Videos", "process-judging-videos.py", stage1_args):
            print("\nStage 1 failed. Proceeding anyway (may have partial data).")
    else:
        print(f"\nSkipping stage 1 (--skip-stage 1)")

    # Stage 2: Render HTML scorecard
    if 2 not in args.skip_stage:
        stage2_args = ["--round", str(args.round)]
        if not run_stage("2: Render Judging HTML", "render-judging-html.py", stage2_args):
            print("\nStage 2 failed. Continuing to stage 3.")
    else:
        print(f"\nSkipping stage 2 (--skip-stage 2)")

    # Stage 3: Validate description
    if 3 not in args.skip_stage:
        if args.description and args.description.exists():
            stage3_args = ["--description", str(args.description)]
            if not run_stage("3: Validate Bounty Description", "validate-bounty-description.py", stage3_args):
                print("\nStage 3: Validation found issues. Review and fix before casting.")
        else:
            print(f"\nSkipping stage 3 (no --description provided)")
    else:
        print(f"\nSkipping stage 3 (--skip-stage 3)")

    # Stage 4: Prepare winner announcement
    if 4 not in args.skip_stage:
        stage4_args = ["--round", str(args.round)]
        if not run_stage("4: Prepare Winner Announcement", "prepare-winner-announcement.py", stage4_args):
            print("\nStage 4: No winner marked in judging.json yet. Skip for now.")
    else:
        print(f"\nSkipping stage 4 (--skip-stage 4)")

    # Final summary
    print(f"\n{'=' * 60}")
    print("JUDGING ROUND ORCHESTRATION COMPLETE")
    print('=' * 60)

    print("\nWhat happened:")
    print("  [Stage 1] Videos processed -> judging.json scaffold created")
    print("  [Stage 2] Judging data rendered to HTML for review")
    print("  [Stage 3] Bounty description validated")
    print("  [Stage 4] Winner announcement drafted (if winner marked)")

    print("\nNext steps (all manual, human-gated):")
    print("  1. Open rounds/r{round_num}/judging.html in your browser")
    print("  2. Review submissions and floor checks")
    print("  3. Fill in rubric scores in rounds/r{round_num}/judging.json")
    print("  4. Mark the winner (set winner=true for one submission)")
    print("  5. Run stage 4 again to generate announcement draft")
    print("  6. Customize and post the announcement (manual)")
    print("  7. Execute on-chain payout (manual)")

    print("\nHuman gates preserved:")
    print("  - Rubric scores: MANUAL (you fill them in)")
    print("  - Winner pick: MANUAL (you mark it in judging.json)")
    print("  - Posting: MANUAL (no automated casting)")
    print("  - Payout: MANUAL (no automated on-chain actions)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
