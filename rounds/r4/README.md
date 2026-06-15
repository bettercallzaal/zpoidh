# R4 - The ZABAL Gamez open pot (OPEN-SPLIT) - DRAFT

POIDH bounty TBD on Base. **Not yet cast.** Drafted 2026-06-15 for review + Monday demo.

A new bounty type: **OPEN-SPLIT**. One pot, split equally across every builder who ships a
real project during ZABAL Gamez July open build month and posts a POIDH proof photo. Not a
single-winner ad bounty - the participation reward for the whole July cohort.

## At a glance

- **Type:** OPEN-SPLIT (open contributions all month + equal split across all qualifiers)
- **Campaign:** ZABAL Gamez Season 1 - July open build month
- **Claim:** a photo of you at your computer/phone with your build up + a link to the build
- **Prize:** the whole pot, split equally across every qualifying builder (in ETH on Base)
- **Pot:** seeded by Zaal now, topped up weekly, OPEN so anyone can stack contributions
- **Issuer:** BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af`
- **Window:** build + submit July 1-31, 2026
- **Closes:** 11:59pm PT, Friday July 31, 2026
- **Payout:** first week of August, before the Finals
- **Relationship to August:** the curated August prize goes to a picked few; this pot goes
  to everyone who participated, picked or not

## Files in this folder

- `description.md` - the POIDH Description field, paste-ready (DRAFT)
- `MECHANIC.md` - **read this first** - how the split actually pays out + the open decisions
- `promo-cast.md` - launch cast (Farcaster + X + Telegram) + reminder casts

## Why this is different from R1-R3

| | R1-R3 (ad bounties) | R4 (open pot) |
|---|---|---|
| Winners | one | everyone who qualifies |
| Judging | scorecard, best wins | pass/fail floor, no ranking |
| Reward | fixed prize to winner | whole pot split equally |
| Pot growth | OPEN (others can stack) | OPEN (others can stack) - core to the idea |
| Claim | the ad asset | proof photo + link to the build |
| Point | best promo for the campaign | reward participation in the build month |

## Before this can be cast (open decisions in MECHANIC.md)

- [x] Payout path - **LOCKED: Option B, distributor disperses** (2026-06-15)
- [ ] Name the distributor wallet (non-issuer; wins the vote + sends the equal shares)
- [ ] Set seed amount + weekly top-up size
- [ ] Decide the min-builders floor (what if only 1-2 ship)
- [ ] Name the pass/fail "real build" checker (proposed: Zaal + one co-host)
- [ ] Decide how post-deadline contributions are handled (recompute split vs roll to R5)

## Cast checklist (once decisions are locked)

- [ ] POIDH UI -> Create OPEN bounty on Base + paste `description.md`
- [ ] Seed the pot with the agreed amount (BCZ Treasury EOA)
- [ ] Album: `wethemmedia` (continuity with R1-R3)
- [ ] Cast `promo-cast.md` on /zabal + /poidh + /zao with the bounty URL as embed
- [ ] Pin in /zabal for the whole window
- [ ] Firefly cross-post to X
- [ ] Weekly: top up the pot + reply-cast the running "$X in pot, N builders in" count
- [ ] Fri Jul 31: close. First week of Aug: finalize qualifiers -> distributor wallet wins
      the vote + withdraws -> disperse equal shares -> cast the payout + tx hashes
- [ ] Add the real bounty id to `scripts/refresh-poidh-leaderboard.py` defaults + refresh

## Related rounds

- [R1 - Hannah Ep 17 clip-up](../r1/)
- [R2 - Best 60s POIDH ad from Ep 19](../r2/)
- [R3 - Best ad for ZABAL Gamez](../r3/)
