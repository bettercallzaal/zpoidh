# Per-Submission Scorecard Template

This template defines the output shape for each submission evaluated by Fable. Use this format when generating scorecards in Phase 2 of the runbook.

---

## Template

```
## [Claim ID] - [Farcaster Handle / Display Name]

**Submission:** [Title]  
**Platform:** [X/FC/etc]  
**Links:** [x_url] / [fc_url]

### Dimension Scores

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| [Dimension 1 Name] | [1-10] | [Why this score - reference the rubric anchor] |
| [Dimension 2 Name] | [1-10] | [Why this score] |
| [Dimension 3 Name] | [1-10] | [Why this score] |
| [Dimension 4 Name] | [1-10] | [Why this score] |

**Overall Score:** [Weighted total, 1-10]  
**Calculation:** (Dim1_score * 0.25 + Dim2_score * 0.25 + Dim3_score * 0.35 + Dim4_score * 0.15) = [total]

### Floor Rules Status
- [Rule 1]: [PASS / FAIL / UNCLEAR]
- [Rule 2]: [PASS / FAIL / UNCLEAR]
- [Rule 3]: [PASS / FAIL / UNCLEAR]

### Strengths
- [Specific strength with reference to submission content]
- [Specific strength]
- [Specific strength]

### Improvements
- [Specific area to improve with suggestion]
- [Specific area to improve]
- [Specific area to improve]

### Feedback for Submitter

[One paragraph, honest but encouraging. Written as if sending directly to the submitter. 2-4 sentences. Include what worked, what didn't, and one thing to focus on next round. End on encouragement.]

---
```

---

## Filled Example: Monksage (R2 Winner, Claim ID 6645)

```
## 6645 - joeyofdeus (Monksage)

**Submission:** How do we pull money to get things done in the real world?  
**Platform:** X  
**Links:** https://x.com/joey_of_deus/status/2057966595029319888

### Dimension Scores

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Distribution | 9 | All three handles tagged (@bettercallzaal, @kennyistyping, @poidhxyz) + poidh.xyz link. Cross-tagged POIDH team itself. 9 likes is high for cohort (engagement signal). Meets all platform distribution criteria in rubric anchor for 9-10. |
| Craft | 8 | Two-question setup (How do we...? → answer) is classic ad structure. 59.7s duration is tight, inside 45-60s window. Video opens with blue title cards matching copy. Edits appear intentional, not a slide show. Slightly below 10 because video posted at 480x270 resolution (desktop crop) rather than mobile-native vertical. |
| Substance | 10 | Directly names "BCZ YapZ Ep 19" + "@kennyistyping explains". Hits the permissionless-coordination thesis exactly ("how POIDH brings transparent, permissionless coordination to life"). Reads as authentic attribution, not generic crypto ad. Perfect anchor match for 10. |
| Bonus | 8 | Question-answer framing is strong copywriting hook. Cross-tag of POIDH team + link to poidh.xyz shows understanding of the audience. Shows creative intentionality beyond minimum brief. Not quite 10 because no unexpected visual flourish or persona spin. |

**Overall Score:** 8.95/10  
**Calculation:** (9 * 0.25 + 8 * 0.25 + 10 * 0.35 + 8 * 0.15) = 2.25 + 2.0 + 3.5 + 1.2 = 8.95

### Floor Rules Status
- Duration (45-60s): PASS (59.7s confirmed via ffprobe)
- Edited (not raw): PASS (title cards + cuts visible)
- Posted on X: PASS (public X post)
- Tagged @bettercallzaal: PASS (mentioned in cross-tags)

### Strengths
- Only submission that names both Ep 19 AND Kenny by name in copy, showing real engagement with source material vs. generic ad spin
- Cleanest floor pass in cohort on duration (59.7s - exactly optimized, not squeezed or padded)
- Full tag set + poidh.xyz link + cross-tag of POIDH team demonstrates platform strategy
- Two-question copy framing lands the episode's central question perfectly: "How do we pull money to get things done in the real world?"

### Improvements
- Posted 32 minutes before deadline, giving little time for organic engagement to grow (current 9 likes probably underrepresents true reach potential)
- Video resolution 480x270 is desktop crop; mobile-native vertical format (9:16) would likely drive more Farcaster engagement

### Feedback for Submitter

You won this round because you were the only submitter who both nailed the floor rules AND clearly attributed the source episode plus Kenny by name in your copy. Your question-answer framing ("How do we...?" leading into the POIDH answer) is textbook ad copywriting and it works perfectly here. The small detail - tagging Ep 19, naming Kenny - is what separates this from generic crypto marketing. Next time: try posting earlier in the submission window so engagement has time to grow naturally, and consider vertical video format for higher mobile engagement on Farcaster. This is pro-level work.

---
```

---

## Filled Example: Non-Winner (Claim ID 6584, Kaspa)

```
## 6584 - i-d0-care (Kaspa)

**Submission:** We're never gonna have good adoption if all crypto does is gambling.  
**Platform:** X  
**Links:** https://x.com/KaspaMeta/status/2054990017487880667

### Dimension Scores

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Distribution | 7 | Tagged @bettercallzaal + @kennyistyping (2/3 required). Posted to X. But no mention of poidh.xyz, no Farcaster cross-post visible. 7 likes is mid-cohort. Meets basic floor rules but lacks the amplification signals of strong distribution. |
| Craft | 7 | Clean opening hook ("We're never gonna have...") lands a sentiment fast. Video is properly edited, not a screencast. 59.7s duration is perfect. However, the hook is a statement, not a call-to-action or question that invites response. Watchable but no strong narrative arc. |
| Substance | 6 | Addresses a real problem in crypto (adoption vs gambling), which is relevant to POIDH's ethos. But does not mention Ep 19, does not cite Kenny, does not clearly connect to the specific episode theme (permissionless coordination). Reads as a general crypto positioning ad, not a response to this round's source material. |
| Bonus | 4 | Straightforward execution, no creative spin. The sentiment is valid but not original (crypto criticism is common). No reference to the source episode or round title. |

**Overall Score:** 6.35/10  
**Calculation:** (7 * 0.25 + 7 * 0.25 + 6 * 0.35 + 4 * 0.15) = 1.75 + 1.75 + 2.1 + 0.6 = 6.2

### Floor Rules Status
- Duration (45-60s): PASS (59.7s)
- Edited (not raw): PASS (intentional cuts)
- Posted on X: PASS
- Tagged @bettercallzaal: PASS

### Strengths
- Strong opening hook ("We're never gonna have good adoption if all crypto does is gambling") lands a sentiment immediately
- Video duration is perfectly optimized at 59.7s
- Addresses a real pain point in crypto adoption, which aligns with POIDH's mission

### Improvements
- Missing Farcaster cross-post and poidh.xyz link - this round values channel amplification, and the submission doesn't show that strategy
- Does not reference Ep 19 or Kenny by name - the winning submission clearly attributed the source, this one doesn't show that engagement
- Opening statement is strong but offers no call-to-action or clear next step for viewers (what should they DO with this insight?)

### Feedback for Submitter

Your instinct is right - adoption vs gambling is a core tension in crypto. Your opening hook lands fast and the message is clear. But this round asked for a response to Ep 19 with Kenny, and you submitted a general crypto positioning ad instead. The winning submission named the episode + Kenny by name, which showed they actually watched/listened. Next round: listen to the source material first, then craft your angle around it. Also, consider cross-posting to Farcaster (where the POIDH community lives) and linking poidh.xyz - distribution amplification is part of the scoring. You're thinking about the right problems; focus next on tying your work to the source and amplifying across channels.

---
```

---

## Output Format Notes

1. **Scores are 1-10, always.** Use half-points if needed (e.g., 7.5), but keep the scale consistent.

2. **Reasoning references the rubric.** When you score 8/10 on Distribution, explain which rubric anchor you're comparing to ("Meets the 7-8 anchor for 'two of three tags + link'").

3. **Strengths are specific.** Not "good production" but "title cards match copy, transition at 15s uses a cut instead of fade, text appears for 3s minimum before cut".

4. **Improvements are actionable.** Not "be more creative" but "add a call-to-action in the final 5s, e.g., 'apply for R4 here'".

5. **Feedback for Submitter is honest but encouraging.** Assume they read it. Start with what worked, note what didn't, end with one clear next step. Avoid generic praise ("great work!") - be specific ("your hook landed because you led with a question, not a statement").

6. **Floor Rules.** If a submission fails a floor rule (e.g., duration too long), it should score lower on Craft dimension. Note the FAIL status, and the submitter should understand why from the feedback.

7. **Overall Score Calculation.** Always show the math. This helps judges verify fairness and catch errors.

---

## Using These Scorecards

1. **For Judge Review:** Print or share these scorecards with the judging panel. They can agree, disagree, or ask Claude for a re-score with updated reasoning.

2. **For Submitter Feedback:** Send the "Feedback for Submitter" paragraph directly to non-winners. It's already written in friendly, actionable tone.

3. **For Archival:** Save the full scorecard to `rounds/r[X]/claude-scorecards-[DATE].md` so next round's judges can see the history.

4. **For Rubric Refinement:** If a scorecard's reasoning feels off (Claude scored a submission high but judges disagree), use that as a signal to refine the rubric anchor for that dimension.
