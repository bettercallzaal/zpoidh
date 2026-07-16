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
- `score.py` - the eval-runner's deterministic scoring backbone: floor-gating +
  weighted aggregation + ranking + validation (the AI/judge supplies per-criterion
  scores; this does the arithmetic the same way every time). No API keys; run
  `python3 pipeline/score.py --selftest`. Example inputs: `rubric.example.json`,
  `submissions.example.json`.

## Next Steps

1. Run the PoC on R2 submissions
2. Get Zaal's qualitative feedback ("Would you pay?")
3. Iterate the rubric + feedback generation based on real judging context
4. Build MVP (Vercel app with submission form + Fable runner + export)
5. Charge Artizen Fund + POIDH for pilot (target: $300-600 MRR in weeks 3-6)

See doc 1120 for the full business case, market sizing, and 6-month revenue roadmap.
