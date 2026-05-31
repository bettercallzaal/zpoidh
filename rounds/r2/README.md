# R2 - Best 60s POIDH ad from Ep 19 w/ Kenny

POIDH bounty 1166 on Base. Cast May 2026. Closed 2026-05-22. Winner cast 2026-05-27.

## At a glance

- **Bounty:** https://poidh.xyz/base/bounty/1166
- **Source:** BCZ YapZ Ep 19 with Kenny (POIDH founder)
- **Format:** 45-60s edited video clip from Ep 19 as a POIDH ad
- **Prize:** 0.0105 ETH on Base (OPEN bounty)
- **Submissions:** 8 claims / 7 unique editors
- **Winner:** @joeyofdeus / Monksage (claim 6645) - the only strict-floor PASS with all three brand tags + named Ep 19 + Kenny in the post copy
- **Issuer:** BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af`
- **Album:** `wethemmedia`

## Live judging page

https://bettercallzaal.com/poidh-round2-judging.html

Per-submission scorecards with floor checks (X URL + @bettercallzaal tag + duration + edited), rubric scores (Distribution / Craft / Substance / Bonus with + boxes), pros/cons, scenarios, decision matrix, mentor jury picks, ffprobe-confirmed durations.

## Files in this folder

- `judging.html` - the per-submission scorecard page UI
- `judging.json` - per-submission data (mirrored from `bettercallzaal.com/poidh-round2-judging.json`)
- `durations.json` - ffprobe results for all 7 video submissions
- `thumbs/<claim>.jpg` - first-frame thumbnails per submission

## What worked

- First round to ship a per-submission scorecard within 48h of close
- ffprobe duration check made the 45-60s floor binary (no judgment-call ambiguity)
- BAR + RUBRIC structure (5 floor rules + 4 rubric categories) gave editors a clear bar
- Score-by-count ZABAL leaderboard mechanic let losers still earn
- Mentor-jury idea (Zaal + Kenny + Tyler + Iman) added distribution surfaces, though R2 itself was Zaal-only

## What broke (lessons folded into R3)

- 3 of 8 submissions overshot 60s by a lot (Ebuka 91.88s, Akukiwil 66.71s, Dee 60.46s) - they didn't realize duration was a hard binary
- Submissions used random library music under Kenny's voice - dialog got buried
- @kennyiscoding typo in the bounty description (real handle is @kennyistyping) - submitters tagged correct handle anyway
- No public brand kit - editors scraped Ep 19 clips themselves, results varied

## Cohort breakdown (final verdicts)

| Claim | Editor | Duration | Floor | Rubric | Verdict |
|---|---|---|---|---|---|
| 6645 | @joeyofdeus / Monksage | 59.70s | PASS | 11/16 | WINNER |
| 6584 | @i-d0-care / KaspaMeta | 59.70s | PASS | 11/16 | finalist |
| 6585 | @kayhwizard | 57.49s | PASS | 12/16 | finalist (cleanest duration) |
| 6586 | @storm_the_first / Jony | 60.21s | borderline | 8/16 | weak |
| 6608 | @dee-13 | 60.46s | borderline | 15/16 (rubric champion) | borderline-over-cap, off-thesis |
| 6644 | @akukiwil_ | 66.71s | FAIL | 12/16 | floor fail (duration) |
| 6616 | @remixitphotos / Ebuka | 91.88s | FAIL | 12/16 | floor fail - best substance copy, 50% over cap |
| 6634 | @cryptfi-mariano | n/a | FAIL | n/a | floor fail (no X URL submitted, text only) |

## Key lessons that became R3 rules

1. **Audio rule** - "no random library music or melodic pads over spoken dialog" lifted from R2 substance failures
2. **Public brand kit** - R3 ships `assets/zabal-games-brand/` with logo, palette, voiced promo MP3, phrases
3. **Direct asset URLs in description** - editors copy in one click vs. navigate
4. **Per-submission scorecard within 48h** - R2 page set the standard, R3+ inherit the template
5. **Score-by-count compounding** - R2 made it visible; R3 reinforces "submit to all 3 = score 3" pitch

## Reference docs

- ZAO OS V1 Doc 768 - POIDH bounty best practices distilled from R1 + R2

## Related rounds

- [R1 - Hannah Ep 17 clip-up](../r1/)
- [R3 - Best ad for ZABAL Gamez](../r3/)
