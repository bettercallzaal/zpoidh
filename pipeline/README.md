# Fable Submission Evaluation Pipeline

AI-powered evaluation for submissions and applications using Claude Fable 5.

## What This Is

A proof-of-concept scaffold for an evaluation pipeline that:

1. **Scores every submission** against a customizable rubric with weighted criteria
2. **Generates personalized feedback for every submitter** - not just winners. This is the market gap - most tools only rank winners; we improve losers for next round.
3. **Creates ranked judging boards** with per-criterion scores and comparative analysis
4. **Synthesizes cohort patterns** to identify what differentiates winners from non-winners

The core business logic: feedback is the retention mechanism. Losers who get real, actionable feedback re-submit next round. Winners attract more submissions through word-of-mouth.

## Why Fable 5

Fable's multi-file context window (200K tokens) reads an entire submission batch simultaneously and spots patterns humans miss:

- One API call scores 50 submissions + generates feedback for all 50
- Identifies "what made winners different" at cohort scale
- Cost: $0.10-$0.50 per submission in API spend
- Selling price: $1-$5 per detailed feedback

See doc 1093 (referenced in doc 1120 business case) for detailed Fable capability comparison.

## PoC Plan

**Target: Run ONE past POIDH round through the pipeline this week.**

1. Pick round R2 or R3 (has submission metadata + actual winning scores in `rounds/r2/judging.json` or `rounds/r3/judging.json`)
2. Extract submissions + existing rubric
3. Run Fable evaluation:
   - Score each submission against rubric (4-5 dimensions, weighted)
   - Generate per-submission feedback draft (strengths, specific improvements, one encouraging-but-honest paragraph)
   - Generate ranked board (top to bottom with scores)
   - Generate cohort synthesis (patterns, standouts, gaps)
4. Compare Claude's scoring to Zaal's actual picks - was the logic sound?
5. Demo to Zaal: "Would you pay for this service?"

**Why R2 specifically:** 8 submissions, detailed rubric (distribution, craft, substance, bonus), clear winner (Monksage/joeyofdeus), real feedback comments already in the source data to compare against.

## Important Guardrail

**AI-ASSISTED judging, never "AI decides."**

Risks documented in the research (doc 1120, Part 5):
- LLM judges can hallucinate scores if rubric is vague
- Gaming risk: submitters learn to "write for Claude" instead of authentic work
- Bias: Fable may over-value certain content types (e.g., highly polished production)

The moat is **trust + outcome data**, not speed. Judges always review Fable's feedback before publishing, and we iterate the rubric based on real outcomes (did the feedback help winners repeat? Did non-winners improve next round?).

The product succeeds only if:
1. Fable's per-submission feedback is more helpful than manual rubrics
2. The cohort synthesis reveals patterns judges didn't see before
3. Judges feel supported, not replaced

## Files in This Directory

- `README.md` (this file) - product overview
- `rubric-template.md` - fill-in rubric template + example for R2 (POIDH ad evaluation)
- `run-eval.md` - step-by-step operational runbook (manual-first, no API keys)
- `scorecard-template.md` - per-submitter output shape + example
- `cohort-synthesis-template.md` - cohort-level patterns + example

## Eval Runner (`eval-runner.mjs`)

Automated Node.js runner that scores a past POIDH round's submissions against the doc-1120 rubric and generates per-submitter scorecards + cohort synthesis.

### Features

- **Rubric-driven scoring**: 4 dimensions (distribution, craft, substance, spec_compliance) + overall score (0-10 each)
- **Per-submission feedback**: Personalized paragraph written TO the submitter (constructive, specific, actionable)
- **Spec compliance check**: Hard floor rules from the round's description.md auto-checked
- **Cohort synthesis**: Average scores, floor-pass rate, standout submissions, emerging patterns
- **Dry-run mode**: Full validation and schema checking WITHOUT an API key
- **Ground-truth verification**: Both `node --check` syntax + `npx tsc --noEmit --allowJs --checkJs` type checks pass
- **Secret hygiene**: No API keys, tokens, or private keys written to any generated files or git history

### Installation

```bash
cd pipeline
npm install
```

### Usage

```bash
# Score a full round (dry run, no API key needed)
node eval-runner.mjs --round r3 --dry-run

# Score a full round (requires ANTHROPIC_API_KEY env var)
ANTHROPIC_API_KEY=sk-ant-... node eval-runner.mjs --round r3

# Score one submission in a round
ANTHROPIC_API_KEY=sk-ant-... node eval-runner.mjs --round r3 --claim 6749

# Verify syntax without SDK installed
node --check pipeline/eval-runner.mjs
```

### Output

Per-submission scorecards written to `data/scorecards/<round>/<claimId>.json`:

```json
{
  "claimId": "6749",
  "round": "r3",
  "wallet": "0xc143cf8515b87ea88d8db8a9892639b5046cf81c",
  "fcHandle": "femmie",
  "submissionUrl": "https://x.com/femmie/status/...",
  "model": "claude-opus-4-8",
  "generatedAt": "2026-07-16T...",
  "score": {
    "distribution": 9,
    "craft": 8,
    "substance": 10,
    "spec_compliance": 9,
    "overall": 9,
    "floor_pass": true,
    "feedback": "You scored high on clarity and cross-posting reach. Next round, try posting earlier for engagement time.",
    "next_round": [
      "Post 1 week before deadline for engagement",
      "Consider vertical format for mobile"
    ]
  }
}
```

Cohort synthesis written to `data/scorecards/<round>/_synthesis.json`:

```json
{
  "round": "r3",
  "submissionCount": 8,
  "averageScores": {
    "distribution": 6.2,
    "craft": 6.1,
    "substance": 6.8,
    "spec_compliance": 7.9,
    "overall": 6.5
  },
  "floorPassRate": "5/8",
  "standouts": [
    {
      "claim_id": "6749",
      "reason": "Highest overall score with excellent cross-platform reach and authentic attribution"
    }
  ],
  "patterns": [
    "Video submitted at exact 60s = optimal craft signal",
    "Cross-posted all channels = distribution multiplier"
  ],
  "model": "claude-opus-4-8",
  "generatedAt": "2026-07-16T..."
}
```

### In-App Integration

Scorecards are intended for rendering in the web UI (NOT sent as Zaal DMs or Telegram notifications). The web UI can:

1. Display per-submitter scorecard on their profile or after submission
2. Show dimension breakdown (distribution, craft, substance, spec_compliance)
3. Render the personalized feedback paragraph
4. Suggest next-round actions

### Rubric (doc-1120)

Dimensions are defined in RUBRIC_SYSTEM_PROMPT. For R3 (ZABAL Gamez ad):

- **Distribution**: Cross-posting reach, handle tags (@bettercallzaal, @poidhxyz, etc.), multi-platform presence
- **Craft**: Production value, editing, timing, captions, hook in first 3 seconds
- **Substance**: Clarity (understand in 3s), originality, thesis capture (free + 3-month + real community + tracks)
- **Spec Compliance**: Hard floor rules from rounds/r3/description.md (format, tagging, audio rules, length)

### Model & Cost

- Model: `claude-opus-4-8` via Anthropic TypeScript SDK
- Tokens per submission: ~500-800 (prompt + response)
- Cost per round (8 submissions): ~$0.08-$0.15 API spend (input: $3/M, output: $15/M)
- Cohort synthesis: ~800-1000 tokens

### Dry-Run Behavior

`--dry-run` mode:

1. Loads all files and builds prompts
2. Validates schemas with stub data
3. Generates placeholder scorecards (won't call Anthropic API)
4. Writes stub scores + feedback to `data/scorecards/<round>/`
5. Exits with code 0 (success)

Use dry-run to:
- Verify the runner works without an API key
- Check data loading and schema validation
- Preview output file structure
- Test in CI/CD without spending API budget

### Requirements Met

- Ground-truth verification: `node --check` + `npx tsc --noEmit --allowJs` ✓
- Manual-first / keyless dry-run ✓
- Per-submitter feedback in-app (data files for UI) ✓
- No Telegram/DM code ✓
- Node/JavaScript using Anthropic TypeScript SDK ✓
- Model: claude-opus-4-8 ✓
- Secret hygiene: no keys/tokens in output ✓
- PR-only (no merge to main) ✓

## Next Steps

1. Run the PoC on R2 or R3 submissions via `eval-runner.mjs`
2. Get Zaal's qualitative feedback on scoring + feedback quality
3. Iterate the rubric + feedback generation based on real judging context
4. Build MVP (Vercel app with submission form + Fable runner + export)
5. Charge Artizen Fund + POIDH for pilot (target: $300-600 MRR in weeks 3-6)

See doc 1120 for the full business case, market sizing, and 6-month revenue roadmap.
