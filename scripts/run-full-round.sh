#!/bin/bash

set -e

###############################################################################
# POIDH Round Automation Orchestrator (Stages 1-5)
#
# Chains the safe/data steps with HUMAN-GATE pauses.
# HARD GATES that never automate:
#   - Rubric scoring / winner selection
#   - Social posting
#   - On-chain accept/vote/payout
#
# Usage:
#   bash scripts/run-full-round.sh 2 1166
#   (Round number, Bounty ID)
#
# Full sequence:
#   1. [DONE] Stage 1: process-judging-videos (ffprobe + scaffold)
#   2. [AUTO] Stage 2: build-judging-html (render HTML)
#   3. [HUMAN] Zaal fills rubric scores, picks winner
#   4. [AUTO] Stage 3: validate-bounty-description (if doing a new bounty)
#   5. [AUTO] Stage 4: prepare-winner-announcement (scaffold cast templates)
#   6. [HUMAN] Zaal reviews and posts winner announcement
#   7. [HUMAN] Zaal submits on-chain vote, waits vote resolution, payout
#
###############################################################################

ROUND="${1:-}"
BOUNTY_ID="${2:-}"

if [ -z "$ROUND" ] || [ -z "$BOUNTY_ID" ]; then
  echo "Usage: bash scripts/run-full-round.sh ROUND BOUNTY_ID"
  echo "Example: bash scripts/run-full-round.sh 2 1166"
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

set +e

echo "================================================================================"
echo "POIDH Round $ROUND Automation (Bounty $BOUNTY_ID)"
echo "================================================================================"
echo ""

# Stage 1 - already done (process-judging-videos)
echo "[STAGE 1] Process judging videos - (already done, or run manually)"
echo "Command: python3 scripts/process-judging-videos.py --bounty $BOUNTY_ID --round $ROUND"
echo "Outputs: rounds/r$ROUND/durations.json, rounds/r$ROUND/judging.json, rounds/r$ROUND/thumbs/"
echo ""
echo "If Stage 1 is NOT complete, run it now:"
echo "  python3 scripts/process-judging-videos.py --bounty $BOUNTY_ID --round $ROUND"
echo ""

# Stage 2 - build-judging-html (auto)
echo "================================================================================"
echo "[STAGE 2] Build judging HTML from judging.json"
echo "================================================================================"
echo ""

if [ ! -f "rounds/r$ROUND/judging.json" ]; then
  echo "ERROR: rounds/r$ROUND/judging.json not found"
  echo "Run Stage 1 first: python3 scripts/process-judging-videos.py --bounty $BOUNTY_ID --round $ROUND"
  exit 1
fi

python3 scripts/build-judging-html.py --round "$ROUND"

if [ $? -ne 0 ]; then
  echo "ERROR: Stage 2 (build-judging-html) failed"
  exit 1
fi

echo "OK: Generated rounds/r$ROUND/judging.html"
echo ""

# HUMAN GATE 1 - Rubric scoring and winner selection
echo "================================================================================"
echo "[HUMAN GATE 1] Zaal fills rubric scores + picks winner"
echo "================================================================================"
echo ""
echo "REQUIRED: Edit rounds/r$ROUND/judging.json manually:"
echo "  1. For each submission, fill rubric_score fields (distribution, craft, substance, bonus)"
echo "  2. Add/update claude_verdict field per submission (STRONG_CANDIDATE, BORDERLINE_DURATION, etc.)"
echo "  3. Set winner: true on the winning submission"
echo "  4. Fill [optional] why_pick, why_skip, key_unknowns, claude_notes fields"
echo ""
echo "Then run the next stage."
echo ""
echo "STOP: Press Enter to continue once Zaal has updated judging.json"
read -p ">> "

# Validate that winner is set
WINNER_CLAIM=$(python3 -c "
import json
try:
  with open('rounds/r$ROUND/judging.json') as f:
    data = json.load(f)
  for sub in data.get('submissions', []):
    if sub.get('winner'):
      print(sub.get('claim_id'))
      break
except:
  pass
" 2>/dev/null)

if [ -z "$WINNER_CLAIM" ]; then
  echo "WARNING: No winner found in judging.json (winner: true not set on any submission)"
  echo "Continuing anyway - Stage 4 will prompt for --winner"
  echo ""
fi

echo ""

# Stage 3 - validate-bounty-description (optional, auto, warnings only)
echo "================================================================================"
echo "[STAGE 3] Validate bounty description (optional)"
echo "================================================================================"
echo ""

if [ -f "rounds/r$ROUND/description.md" ]; then
  python3 scripts/validate-bounty-description.py --round "$ROUND"
  echo ""
else
  echo "SKIP: rounds/r$ROUND/description.md not found (not a bounty launch round)"
  echo ""
fi

# Stage 4 - prepare-winner-announcement (auto)
echo "================================================================================"
echo "[STAGE 4] Prepare winner announcement scaffolds"
echo "================================================================================"
echo ""

if [ -z "$WINNER_CLAIM" ]; then
  echo "ERROR: No winner found in judging.json"
  echo "Set winner: true on the winning submission in judging.json, then re-run this script"
  exit 1
fi

python3 scripts/prepare-winner-announcement.py --round "$ROUND" --winner "$WINNER_CLAIM"

if [ $? -ne 0 ]; then
  echo "ERROR: Stage 4 (prepare-winner-announcement) failed"
  exit 1
fi

echo "OK: Generated rounds/r$ROUND/winner-announce.md"
echo ""

# HUMAN GATE 2 - Review and post winner announcement + on-chain finalize
echo "================================================================================"
echo "[HUMAN GATE 2] Zaal reviews + posts winner announcement + on-chain finalize"
echo "================================================================================"
echo ""
echo "REQUIRED: Manual steps Zaal performs (do NOT automate):"
echo ""
echo "1. REVIEW winner announcement:"
echo "   - Edit rounds/r$ROUND/winner-announce.md"
echo "   - Fill [WHY THEY WON] section (1-2 sentences max)"
echo "   - Review all cast templates (Farcaster, X, TG)"
echo ""
echo "2. CAST the winner announcement:"
echo "   - Post Farcaster version in /poidh + /zao + X (via Firefly)"
echo "   - Reply with thread version"
echo "   - Do NOT auto-post - copy from winner-announce.md and post manually"
echo ""
echo "3. ON-CHAIN FINALIZE (for OPEN bounty type):"
echo "   - Call submitClaimForVote(bountyId=$BOUNTY_ID, winningClaimId=$WINNER_CLAIM) on POIDH UI"
echo "   - Wait ~48 hours for contributor vote to close"
echo "   - Call resolveVote(bountyId=$BOUNTY_ID) on POIDH UI"
echo "   - Winner can then call withdraw() to receive ETH"
echo ""
echo "   OR for SOLO bounty type:"
echo "   - Call acceptClaim(bountyId=$BOUNTY_ID, winningClaimId=$WINNER_CLAIM) directly"
echo "   - Winner can withdraw immediately"
echo ""
echo "NEVER:"
echo "   - Auto-post to Farcaster / X / TG (always manual via Firefly + copy-paste)"
echo "   - Auto-do submitClaimForVote / acceptClaim / resolveVote (always manual on POIDH UI)"
echo "   - Auto-do payout or on-chain transactions"
echo ""
echo "STOP: Press Enter once all manual steps are complete"
read -p ">> "

echo ""
echo "================================================================================"
echo "[DONE] Round $ROUND automation complete"
echo "================================================================================"
echo ""
echo "Outputs:"
echo "  - rounds/r$ROUND/judging.json (with winner marked)"
echo "  - rounds/r$ROUND/judging.html (scorecard)"
echo "  - rounds/r$ROUND/winner-announce.md (scaffold)"
echo ""
echo "Zaal completed (manual):"
echo "  - Rubric scoring + winner selection"
echo "  - Winner announcement posts (Farcaster, X, TG)"
echo "  - On-chain vote + resolution"
echo "  - Winner payout (withdraw)"
echo ""

exit 0
