# Running an Evaluation: Operational Runbook

**This is the MANUAL-FIRST version.** Judges + Zaal run evaluations by pasting into Claude directly. No API keys, no scripts. This keeps the PoC simple and lets Zaal iterate the rubric in real-time based on actual submission quality.

## Phase 1: Preparation (30 min)

### Step 1.1 - Gather Submissions

Pick a completed round from `rounds/` that has submissions you want to evaluate:
- **R2 (POIDH Ad):** 8 submissions, real rubric + judging notes already exist - use this for PoC
- **R3 (ZABAL Gamez Ad):** 8 submissions, lightweight rubric
- **R1/R4/R5/R6:** See `rounds/[rX]/judging.json` for submission data

Compile a JSON file with the submissions:

```json
{
  "round": 2,
  "title": "Best 60s POIDH Ad",
  "submissions": [
    {
      "claim_id": 6645,
      "fc_handle": "joeyofdeus",
      "title": "How do we pull money to get things done in the real world?",
      "x_url": "https://x.com/joey_of_deus/status/2057966595029319888",
      "description": "Cites Ep 19 + Kenny. Two-question hook landing permissionless-coordination theme. 59.7s, all tags.",
      "x_text": "How do we pull money to get things done in the real world? On BCZ YapZ Ep 19, @kennyistyping explains how POIDH brings transparent, permissionless coordination to life",
      "x_favs": 9
    },
    {
      "claim_id": 6584,
      "fc_handle": "i-d0-care",
      "title": "Adoption + Gambling",
      "x_url": "https://x.com/KaspaMeta/status/2054990017487880667",
      "description": "Opens with 'We're never gonna have good adoption if all crypto does is gambling.' 59.7s, tags present but no Ep 19 cite.",
      "x_text": "We're never gonna have good adoption if all crypto does is gambling.",
      "x_favs": 4
    }
    [repeat for remaining 6 submissions]
  ]
}
```

**For PoC:** R2 submission data is already in `rounds/r2/judging.json` in this repo. Copy the relevant fields.

### Step 1.2 - Confirm Rubric

Copy your rubric from `rubric-template.md` (or create a new one). Make sure you have:
- 4-6 scoring dimensions
- Weights for each (sum to 100)
- Clear anchors for score levels (1-10)

For the PoC, use the R2 example from `rubric-template.md` (Distribution, Craft, Substance, Bonus).

---

## Phase 2: Batch Evaluation with Claude (60-90 min)

### Step 2.1 - Prepare the Prompt

Copy this template and fill in your round details + submission list + rubric:

```
[PROMPT FOR CLAUDE - COPY AND PASTE INTO CLAUDE]

I am running an evaluation of submissions for: [ROUND TITLE]

RUBRIC:
[Copy the full rubric from rubric-template.md here]

SUBMISSIONS:
[Paste the JSON list of submissions above here]

TASK:
1. Score each submission against the rubric (1-10 for each dimension)
2. Calculate the weighted overall score
3. Generate a per-submission scorecard with:
   - Individual dimension scores
   - Why each score
   - Strengths (2-3 bullet points)
   - Specific improvements (2-3 bullet points)
   - One honest-but-encouraging paragraph the submitter receives
4. Generate a RANKED BOARD (submissions sorted by overall score, top to bottom)
5. Generate a COHORT SYNTHESIS with patterns (what made top scorers different? what gaps did you see?)

OUTPUT FORMAT:
Use the templates from scorecard-template.md and cohort-synthesis-template.md (see those files for exact format).

CALIBRATION:
If you see a submission that reminds you of a rubric anchor, say so. If a submission is hard to score because the rubric is ambiguous, flag that (it tells us the rubric needs refinement).

IMPORTANT:
- This is AI-assisted judging, never "AI decides." These scorecards are drafts for a human judge to review and modify.
- Be specific: reference submission content, not generic phrases.
- Encourage improvement: even low scorers should understand what they did right and what to fix.

Go.
```

### Step 2.2 - Run the Evaluation

1. Paste the prompt into Claude (Web or Claude Code)
2. Let it generate all per-submission scorecards + ranked board + cohort synthesis
3. Copy the output to a file: `rounds/r[X]/claude-eval-[DATE].md`

Expected runtime: Claude will take 30-60 seconds on the analysis, then you read the output (30 min to review quality).

---

## Phase 3: Judge Review & Iteration (30-60 min)

### Step 3.1 - Compare to Actual Picks

If this round already has a winner (e.g., R2 winner was Monksage):

1. Did Claude rank the actual winner in the top 3?
2. Did Claude's reasoning match Zaal's judgment?
3. Did Claude miss something the judge saw?

Example: For R2, Claude scored Monksage 8.95/10 with "cleanest floor pass + all tags + Ep 19 cite". Zaal picked Monksage same reason. **Match = confidence in the rubric.**

### Step 3.2 - Iterate the Rubric

If Claude's scores don't match expectations:

- **Issue:** Claude scored a bad submission too high.
  - Fix: Rubric was too vague. Add more specific anchors (e.g., "Excellent = mentions Ep 19 *by name*, not just 'the episode'").

- **Issue:** Claude scored a good submission too low on one dimension.
  - Fix: Weight that dimension higher, or expand the anchor to clarify what excellence looks like.

- **Issue:** Claude's feedback was generic.
  - Fix: Ask for revised eval with more specific references to submission content.

**Document the changes** in the rubric so the next round learns from this one.

### Step 3.3 - Share Feedback with Submitters

Take the per-submission scorecards and feedback paragraphs from Phase 2 and send to non-winners (winners get a separate announcement from Zaal).

Example to a non-winner:

> You submitted [TITLE] for R2.
>
> Score: 6.5/10
> - Distribution: 5/10 (minimal tags)
> - Craft: 7/10 (tight editing, but pacing drags in middle)
> - Substance: 7/10 (hits the theme but doesn't mention Ep 19 by name)
> - Bonus: 5/10 (straightforward, nothing extra)
>
> Strengths:
> - You clearly understood the permissionless-coordination theme
> - Video pacing is generally tight, cuts feel intentional
>
> What to improve:
> - Next time, tag all three handles (@bettercallzaal, @kennyistyping, @poidhxyz) and include the episode link
> - Reference Ep 19 + Kenny by name in your copy (it shows you actually listened, not just guessed)
>
> Honest take: Your video is solid on craft and substance, but the distribution signals were quiet. Next round, aim to tag the source + amplify across channels. You're close to winning.

This is the retention mechanic - submitters who get real feedback re-submit.

---

## Phase 4: Archive & Iterate (15 min)

### Step 4.1 - Save Results

1. Copy Claude's full output to `rounds/r[X]/claude-eval-[DATE].md`
2. Update the rubric in `rounds/r[X]/rubric.md` if you refined it
3. Note any calibration issues in `rounds/r[X]/README.md`

### Step 4.2 - Metrics to Track (for product decisions)

As you run evals, collect:
- **Time spent:** How long did Phase 2 take? (goal: 60 min for 8 submissions = 7.5 min per submission)
- **Judge agreement:** Did Claude's top picks match Zaal's top picks? (goal: 80%+ in top 3)
- **Feedback quality:** Would a submitter find the feedback helpful? (qualitative: strong/okay/weak)
- **Rubric stability:** Did you need to refine the rubric after this round? (goal: fewer changes over time)

### Step 4.3 - Feedback Loop

After the first 2-3 rounds:
- **If Claude scores match judges 90%+:** Rubric is good. Safe to automate.
- **If Claude scores match 60-70%:** Rubric needs refinement. Keep iterating.
- **If Claude scores match <60%:** Rubric is too vague, or judges disagree on what excellence means. Fix the rubric, not Claude.

---

## PoC Target: R2 Evaluation This Week

### Timeline

- **Day 1 (2-3 hours):**
  - Step 1.1: Extract R2 submission data from `rounds/r2/judging.json` (already done, just reformat JSON)
  - Step 1.2: Copy R2 rubric from `rubric-template.md` example
  - Step 2.1-2.2: Run Claude evaluation prompt
  - Save to `rounds/r2/claude-eval-2026-07-15.md`

- **Day 2 (1-2 hours):**
  - Step 3.1: Compare Claude scores to Zaal's actual picks (Monksage = winner). Does Claude agree?
  - Step 3.2: Note any rubric refinements
  - Step 3.3: Draft feedback for non-winning submitters
  - Slack Zaal: "Claude scored Monksage 8.95/10 for [reasons]. Your actual pick was Monksage for [reasons]. Match?" If yes: confidence in the approach.

### Success Criteria

- Claude's top 3 picks include the actual winner
- Rubric anchors felt natural to apply
- Feedback drafts are specific and actionable (not generic)
- Zaal says: "I would pay for this. Let's run it on [next bounty round]."

---

## Limitations of This Manual Approach

**Pro:** Flexible, iterative, no code needed.  
**Con:** Labor-intensive (90 min per 8 submissions). Next phase: script this.

Once the rubric is stable (3+ rounds of 90%+ accuracy), we automate:
- Batch submission scraper (fetch from zpoidh API)
- Rubric parser (YAML → Claude parameters)
- Evaluation runner (calls Claude with batch, extracts scores)
- Scorecard generator (formats output as CSV + per-submission PDFs)
- Webhook notification (sends feedback to submitters via Telegram/Email)

But that's Phase 2 (the MVP). Phase 1 is proving the concept manually.

---

## Troubleshooting

**Q: Claude's scores seem random.**
A: Rubric is too vague. Go back to Step 3.2 and add more specific anchors. Example: instead of "Excellent = clear CTA", write "Excellent = CTA appears in last 5 seconds, uses action verb like 'submit', references deadline".

**Q: Claude ranked submission A higher than B, but B is clearly better.**
A: Either (a) the rubric doesn't capture what makes B better, or (b) Claude misread the submission. Ask Claude to re-score B and explain its reasoning step-by-step.

**Q: Should Claude see the actual winner before scoring?**
A: No. Score blind first, then compare to actual picks in Phase 3. This tests whether the rubric actually predicts quality, not just parrots the judge's decision.

**Q: What if judges disagree (Zaal picks A, Kenny picks B)?**
A: Use Claude as a tiebreaker. If Claude also scores A higher based on the rubric, the rubric is working. If Claude scores B higher, the rubric may not capture Kenny's judgment lens - adjust it or create a separate "Kenny's lens" rubric.
