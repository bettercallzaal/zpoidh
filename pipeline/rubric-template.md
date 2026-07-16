# Submission Rubric Template

## How to Fill This Out

A rubric is the backbone of consistent evaluation. Before running the pipeline:

1. Define 4-6 scoring dimensions (what makes a good submission?)
2. Assign weights (does distribution matter more than craft?)
3. Write anchors for each score level (what does a 3/10 look like? a 9/10?)
4. Examples of real submissions help Fable calibrate

Fable will use this rubric to score every submission uniformly and generate feedback that references specific criteria.

---

## Template (Fill This In)

### Round Info
- **Round Name:** [e.g., "R2 - Best 60s POIDH Ad"]
- **Bounty/Context:** [e.g., "Prize: 0.0105 ETH, deadline May 22"]
- **Submission Count:** [e.g., 7 total, 3 floor-pass]
- **Floor Rules (Auto-Screen):** [e.g., "45-60s duration, posted on X, tagged @bettercallzaal"]

### Scoring Dimensions

#### Dimension 1: [Name]
- **Weight:** [0-100, total should sum to 100]
- **What This Measures:** [e.g., "How well did the submission reach the intended audience?"]
- **Scoring Anchors:**
  - **9-10 (Excellent):** [e.g., "Tagged all required handles + linked source, cross-posted, 10+ engagement"]
  - **7-8 (Strong):** [e.g., "Tagged 2/3 handles, posted on X, some engagement"]
  - **5-6 (Adequate):** [e.g., "Posted but minimal tags or cross-posting"]
  - **3-4 (Weak):** [e.g., "Posted but misses key distribution signals"]
  - **1-2 (Fails):** [e.g., "Not posted or doesn't meet distribution criteria"]

#### Dimension 2: [Name]
- **Weight:** [0-100]
- **What This Measures:** [...]
- **Scoring Anchors:**
  - **9-10 (Excellent):** [...]
  - **7-8 (Strong):** [...]
  - **5-6 (Adequate):** [...]
  - **3-4 (Weak):** [...]
  - **1-2 (Fails):** [...]

[Repeat for each dimension]

### Calculation
```
Overall Score = (Dimension1_Score * Dimension1_Weight + 
                 Dimension2_Score * Dimension2_Weight + 
                 ...) / 100
```

---

## Filled Example: R2 POIDH Ad Evaluation

### Round Info
- **Round Name:** R2 - Best 60s POIDH Ad (Ep 19 w/ Kenny)
- **Bounty/Context:** Prize: 0.0105 ETH, Deadline: May 22 2026, 8 submissions
- **Submission Count:** 8 total, 3 floor-pass (duration correct, X posted, tagged)
- **Floor Rules:** 45-60s duration, edited not raw, posted on X, tagged @bettercallzaal + mention @kennyistyping

### Scoring Dimensions

#### Dimension 1: Distribution
- **Weight:** 25
- **What This Measures:** How well did the submission amplify the message across channels and audiences?
- **Scoring Anchors:**
  - **9-10 (Excellent):** All three handles tagged (@bettercallzaal, @kennyistyping, @poidhxyz) + poidh.xyz link in post. Cross-posted to Farcaster. 10+ engagement (likes/replies). Posted with intention to drive reach.
  - **7-8 (Strong):** Two of three handles tagged + link. Farcaster cross-post implied or done. 5-9 engagement.
  - **5-6 (Adequate):** One or two tags. Posted but minimal cross-platform presence. 1-4 engagement.
  - **3-4 (Weak):** Only X post, minimal or no tags. No links.
  - **1-2 (Fails):** Does not meet floor rule for tagging or posting.

#### Dimension 2: Craft
- **Weight:** 25
- **What This Measures:** Video production quality, pacing, editing, and watchability.
- **Scoring Anchors:**
  - **9-10 (Excellent):** Tight cuts throughout. Hook in first 3 seconds. Clear CTA or call-to-action. Captions sync'd well. Holds attention at 1x speed. Looks intentional, not a screencast.
  - **7-8 (Strong):** Some cuts and pacing. Hook exists but may not be in first 3s. Clear message. Some production intent visible.
  - **5-6 (Adequate):** Mostly watchable. Pacing okay but no strong hook. Minimal editing visible.
  - **3-4 (Weak):** Looks like a slide show or raw screen recording. Pacing drags. Hard to follow.
  - **1-2 (Fails):** Unwatchable, unintelligible, or too long/short.

#### Dimension 3: Substance
- **Weight:** 35
- **What This Measures:** Does the submission hit the POIDH thesis and Episode 19 topic?
- **Scoring Anchors:**
  - **9-10 (Excellent):** Directly cites Ep 19 by name AND Kenny. Captures the permissionless-coordination thesis exactly. Sounds like it was made *because* of the episode, not just a generic ad.
  - **7-8 (Strong):** References the main idea (e.g., "real-world coordination", "no gatekeepers"). Mentions Kenny or POIDH. Coherent but not as precise.
  - **5-6 (Adequate):** Mentions crypto or builders but doesn't clearly land on the Ep 19 angle. Generic POIDH positioning.
  - **3-4 (Weak):** Tangentially related to POIDH but no clear Ep 19 connection. Could be an ad for any DAO.
  - **1-2 (Fails):** No clear connection to Episode 19 or POIDH mission.

#### Dimension 4: Bonus
- **Weight:** 15
- **What This Measures:** Creative spin, originality, or going above the brief.
- **Scoring Anchors:**
  - **9-10 (Excellent):** Unique angle that adds energy (e.g., strong hook, unexpected visual, persona). Attributes source properly. Encourages next bounties.
  - **7-8 (Strong):** Shows some creativity. Clear attribution.
  - **5-6 (Adequate):** Straightforward execution, nothing extra.
  - **3-4 (Weak):** Feels phoned-in.
  - **1-2 (Fails):** No originality.

### Calculation
```
Overall Score = (Distribution_Score * 0.25 + 
                 Craft_Score * 0.25 + 
                 Substance_Score * 0.35 + 
                 Bonus_Score * 0.15)
```

### Example Scoring: Monksage (claim_id 6645, R2 winner)

| Dimension | Score | Why |
|-----------|-------|-----|
| Distribution | 9 | Three handles tagged + poidh.xyz link. Cross-tag of POIDH team itself. 9 likes (high for cohort). |
| Craft | 8 | Two-question setup landing the answer is classic ad structure. Video is tight (59.7s). Needs playback for edit confirmation but indicators are strong. |
| Substance | 10 | Directly names "BCZ YapZ Ep 19" + "@kennyistyping explains". Hits the permissionless-coordination thesis exactly. Reads as authentic attribution, not generic. |
| Bonus | 8 | Two-question framing is a solid copywriting hook. Cross-tag of POIDH team shows understanding of the audience. |
| **Overall** | **8.95** | (9*0.25 + 8*0.25 + 10*0.35 + 8*0.15) = 2.25 + 2 + 3.5 + 1.2 = 8.95 |

**Strengths:** 
- Cleanest floor pass in cohort (59.7s duration)
- Only submission naming both Ep 19 + Kenny + @kennyistyping
- Full tag set + poidh.xyz link
- Three-sentence copy that lands the episode's central question

**Improvements:**
- Posted only 32 min before deadline - little time for engagement
- Video resolution 480x270 is desktop crop, not mobile-native vertical

**Honest Feedback for Monksage:**
You won this round because you were the only submitter who both nailed the floor rules (59.7s, all tags) AND clearly attributed the source episode + Kenny by name in your copy. The question-answer framing (How do we...? On Ep 19, X explains...) is ad-copywriting 101 and it works here. Next time: try posting earlier in the submission window so engagement has time to grow. Also consider vertical format for higher mobile engagement.

---

## Using This Template

1. Copy the "Template" section above
2. Fill in your round-specific dimensions and anchors
3. Run the Fable pipeline with this rubric (see `run-eval.md`)
4. Fable will reference these anchors when scoring each submission
5. Review Fable's scores and per-submission feedback
6. Adjust the rubric for next round based on how well it predicted winner quality
