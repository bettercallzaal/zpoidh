#!/usr/bin/env python3
"""
Prepare winner announcement cast scaffolds from judging.json data.

    python3 scripts/prepare-winner-announcement.py --round 2 --winner 6645

Reads:
    rounds/rN/judging.json        - Judging data with winner submission

Writes:
    rounds/rN/winner-announce.md  - Scaffold with Farcaster/X/TG templates,
                                    leaves [WHY THEY WON] for Zaal to fill

The script does NOT post, does NOT do on-chain calls.
Never assumes gender - uses handle/they, no he/she.

Pure stdlib: json, argparse, pathlib.
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def escape_md(s: str) -> str:
    """Escape markdown special characters."""
    if not s:
        return ""
    return s.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def find_submission_by_claim_id(submissions: list, claim_id: int) -> dict | None:
    """Find submission by claim_id."""
    for sub in submissions:
        if sub.get("claim_id") == claim_id:
            return sub
    return None


def build_winner_announce_md(
    round_num: int, bounty_id: int, winner_sub: dict, bounty_url: str, bounty_title: str
) -> str:
    """Build winner announcement markdown scaffold."""
    claim_id = winner_sub.get("claim_id")
    fc_handle = winner_sub.get("fc_handle", "unknown")
    display_name = winner_sub.get("display_name", fc_handle)
    x_handle = winner_sub.get("x_handle", winner_sub.get("twitter_handle", fc_handle))
    x_url = winner_sub.get("x_url", "")
    poidh_url = winner_sub.get("poidh_claim_url", "")
    amount_eth = winner_sub.get("amount_eth_at_judging", 0)  # Will come from judging data

    # Find amount from judging data if not on submission
    if not amount_eth and "judging" in str(REPO_ROOT):
        # Amount will be filled by Zaal from bounty data
        amount_eth = 0.0

    # Build templates
    md = f"""# Round {round_num} Winner Announcement

**Winner:** @{escape_md(fc_handle)} ({escape_md(display_name)})
**Claim ID:** {claim_id}
**Bounty:** {escape_md(bounty_title)}
**Round:** {round_num}
**Bounty URL:** {bounty_url}

---

## Why They Won

[WHY THEY WON - Zaal to fill: the specific thing that beat the cohort. Felt like a real ad/clip, not a dump. 1-2 sentences max.]

---

## Farcaster (long)

```
@{fc_handle} won Round {round_num} of the BCZ x POIDH bounty.

The submission: {x_url or poidh_url}

[WHY THEY WON]. Felt like a real submission, not a clip dump.

Real congrats. Earned it.

~{amount_eth:.4f} ETH released to you once the contributor vote resolves (approximately 48 hours on POIDH's open bounty flow).

And here is the part that actually scales - every single submitter to Round {round_num} already got ZABAL airdropped to their wallet via slot 8 of the ZABAL Empire on Empire Builder. Winning the ETH is the spike. Showing up earns the baseline. That is the whole model.

Full breakdown of all submissions + rubric scoring + the judging logic:
- Page: https://bettercallzaal.com/poidh-round{round_num}-judging.html
- GitHub: https://github.com/bettercallzaal/zpoidh/tree/main/rounds/r{round_num}

cc @poidhxyz
```

## X (under 280)

```
@{x_handle} / {escape_md(display_name)} won Round {round_num} of the BCZ x POIDH bounty - real congrats

[WHY THEY WON - one line max]

winner takes ~{amount_eth:.4f} ETH. every submitter already earned ZABAL via @empirebuilder slot 8

clip: {x_url or poidh_url}
breakdown: https://bettercallzaal.com/poidh-round{round_num}-judging.html
```

## Telegram / GC / Discord (mid-length)

```
Round {round_num} BCZ x POIDH winner: @{fc_handle} / {escape_md(display_name)}. Real congrats - earned it.

Winner takes ~{amount_eth:.4f} ETH after the approximately 48-hour contributor vote. Every submitter to Round {round_num} already got ZABAL airdropped via the ZABAL Empire leaderboard - submitting is the reward, winning is the bonus.

Clip: {x_url or poidh_url}
Breakdown: https://bettercallzaal.com/poidh-round{round_num}-judging.html
Source: https://github.com/bettercallzaal/zpoidh/tree/main/rounds/r{round_num}
```

## Reply-cast to winner on the thread

```
brought heat with that [SPECIFIC THING] @{fc_handle} - shipping you the next bounty brief direct when Round {round_num + 1} drops, would love to see you defend it
```

---

## Checklist before posting

- [ ] Zaal filled [WHY THEY WON] section
- [ ] Verified winner handle @{fc_handle} is correct (no typos)
- [ ] Confirmed ETH amount ~{amount_eth:.4f} is correct
- [ ] Verified X URL or POIDH claim URL is correct
- [ ] Cast the Farcaster version in /poidh + /zao + X (Firefly)
- [ ] Reply with the thread version
- [ ] Do NOT post the on-chain vote or payout - Zaal handles those via POIDH UI

---

**Notes:**
- This scaffold uses handle + they/them pronouns (never assumes gender)
- All templates are paste-ready with placeholders for Zaal to fill
- No on-chain operations here - Zaal executes submitClaimForVote/acceptClaim separately
"""

    return md


def main() -> int:
    p = argparse.ArgumentParser(
        description="Prepare winner announcement scaffolds from judging.json"
    )
    p.add_argument("--round", type=int, required=True, help="Round number")
    p.add_argument("--winner", type=int, required=True, help="Winner claim_id")
    p.add_argument(
        "--json-file",
        type=Path,
        default=None,
        help="Path to judging.json (default: rounds/rN/judging.json)",
    )

    args = p.parse_args()

    # Determine JSON path
    if args.json_file:
        json_path = args.json_file
    else:
        json_path = REPO_ROOT / f"rounds/r{args.round}/judging.json"

    if not json_path.exists():
        print(f"ERROR: {json_path} not found")
        return 1

    # Load judging.json
    try:
        with open(json_path) as f:
            judging_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse {json_path}: {e}")
        return 1
    except Exception as e:
        print(f"ERROR: Failed to read {json_path}: {e}")
        return 1

    # Find winner submission
    submissions = judging_data.get("submissions", [])
    winner_sub = find_submission_by_claim_id(submissions, args.winner)

    if not winner_sub:
        print(
            f"ERROR: Claim {args.winner} not found in {json_path}. Available claims: {[s.get('claim_id') for s in submissions]}"
        )
        return 1

    # Get bounty metadata
    bounty_id = judging_data.get("bounty_id", "")
    bounty_url = judging_data.get("bounty_url", "")
    bounty_title = judging_data.get("bounty_title", "")
    amount_eth = judging_data.get("amount_eth_at_judging", 0.0)

    # Add amount to winner submission for template
    winner_sub["amount_eth_at_judging"] = amount_eth

    # Build announcement markdown
    try:
        md_content = build_winner_announce_md(
            args.round, bounty_id, winner_sub, bounty_url, bounty_title
        )
    except Exception as e:
        print(f"ERROR: Failed to build announcement: {e}")
        return 1

    # Write markdown
    md_path = REPO_ROOT / f"rounds/r{args.round}/winner-announce.md"
    try:
        md_path.parent.mkdir(parents=True, exist_ok=True)
        with open(md_path, "w") as f:
            f.write(md_content)
        print(f"Wrote {md_path.relative_to(REPO_ROOT)}")
        print(
            f"\nWinner: @{winner_sub.get('fc_handle')} (Claim {args.winner})\nZaal to fill [WHY THEY WON] and review before posting.\n"
        )
        return 0
    except Exception as e:
        print(f"ERROR: Failed to write {md_path}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
