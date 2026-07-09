# R3 - Best ad for ZABAL Gamez

POIDH bounty 1180 on Base. Cast 2026-05-31. Closed 2026-06-14. **FULLY RESOLVED, PAID OUT.**

Confirmed 2026-07-09: pulled the raw `claims.fetchBountyClaims` record for claim 6749
(femmie, "ZABALGAMEZ.COM AD") directly from POIDH's tRPC. Its `owner` field is
`0x7234c36a71ec237c2ae7698e8916e0735001e9af` - the BCZ Treasury issuer wallet - while every
other (non-accepted) claim on 1180 still shows `owner: 0x5555fa78...` (the POIDH contract's
own escrow address). Per the PoidhV2 contract's own code
(`poidhV2Nft.safeTransfer(address(this), bounty.issuer, claimId, '')` inside
`_acceptClaim`), the claim NFT only moves to the issuer wallet as part of the same
transaction that pays the claimant 97.5% of the bounty and the treasury the 2.5% fee - there
is no separate withdraw step in this contract. So the NFT sitting in the treasury wallet
*is* proof the full accept-and-payout sequence already ran on-chain: femmie has been paid,
the fee has been collected. This isn't a guess from off-chain data anymore - it's read
straight from the claim record.

Still open: the winner cast was never drafted with real reasoning (still a placeholder) and
never posted - that's the one remaining step, and it's a public-posting action for Zaal, not
something this session does. See [judging.json](judging.json) for the full claim list.

## At a glance

- **Bounty:** https://poidh.xyz/base/bounty/1180
- **Source:** zabalgamez.com (the campaign itself - ZABAL Gamez Season 1)
- **Format:** ANY format ad - image, video, meme, motion, cast, poster, audio drop. No format gate.
- **Prize:** 0.0125 ETH on Base (OPEN bounty)
- **Issuer:** BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af`
- **Album:** `wethemmedia`
- **Brand kit:** [bettercallzaal.com/assets/zabal-games-brand/](https://bettercallzaal.com/assets/zabal-games-brand/) (mirrored in [assets/brand-kits/zabal-games/](../../assets/brand-kits/zabal-games/))
- **Closes:** 11:59pm PT, Sunday June 14, 2026
- **Winner cast:** end of day Monday June 15, 2026

## Files in this folder

- `description.md` - the v8 description that landed on the bounty (paste-ready)
- `promo-cast.md` - the launch cast (Farcaster long + X short + Telegram)
- `cast-templates/` - winner / catalytic DM / mid-window reminder templates

## What's new in R3 vs R2

1. **ANY format** (not just video) - opens the door to designers, meme-makers, motion artists, audio editors
2. **Public brand kit at known URL** - `bettercallzaal.com/assets/zabal-games-brand/` ships logo + palette + 50s promo MP3 + phrases + glossary, all CC-BY
3. **Audio rule baked in** - no random library music under spoken dialog; use the official promo MP3 OR source audio OR one clear instrumental
4. **Score-by-count visible** - description explicitly tells submitters their $ZABAL drop compounds across R1+R2+R3
5. **Direct asset download URLs** - 6 direct links in the description body so editors copy in one click
6. **Mentor-jury implicit** - POIDH's open-bounty contributor-vote handles the jury layer; no jury writeup in description
7. **Date rigor** - day-of-week + date double-checked (Kenny caught a Sat/Sun mismatch in v5)
8. **Handle accuracy** - @kennyistyping (not @kennyiscoding which was a R2 typo)

## Live distribution surfaces

- Hub: https://bettercallzaal.com/poidh.html
- Brand kit landing: https://bettercallzaal.com/assets/zabal-games-brand/
- Best practices: https://bettercallzaal.com/poidh-bounty-best-practices.html
- Empire Builder leaderboard: https://www.empirebuilder.world/empire/0xbb48f19b0494ff7c1fe5dc2032aeee14312f0b07
- Farcaster channel: https://farcaster.xyz/~/channel/zabal

## Pre-cast prep that landed

- BCZ PR #16 - R3 prep folder + best-practices page + binaural beat MP3 (MERGED)
- BCZ PR #17 - replaced binaural with synth promo MP3 (MERGED - superseded by #18)
- BCZ PR #18 - real production promo MP3 + full brand kit rebuild (MERGED)
- BCZ PR #19 - index.html for folder URL so kit folder doesn't 404 (open at write-time)
- ZAOOS PR #718 - Doc 768 bounty best practices (MERGED)
- ZAOOS PR #724 - Doc 769 ZAODEVZ repo audit (MERGED)
- ZAOOS PR #761 - Doc 786 brand kit rebuild audit (MERGED)
- ZAODEVZ/zabalgames PR #33 - llms.txt R3 bounty section (open)

## Post-bounty checklist (after close)

- [x] Run `scripts/refresh-poidh-leaderboard.py` to pull final submission list (2026-07-08, 8 claims)
- [x] Build `judging.json` documenting the claim list + the on-chain accepted claim
- [x] Winner already selected on-chain - claim 6749 (femmie, ZABALGAMEZ.COM AD), `isAccepted: true`
- [x] Confirmed resolved + paid: claim NFT owner is the treasury wallet, proving accept+payout completed (2026-07-09)
- [ ] Fill in the real why-she-won reasoning in `cast-templates/winner-announce-femmie.md` (still a placeholder) and post it - Zaal's call, not automated here
- [ ] Ship `judging.html` (copy from `rounds/r2/judging.html`, swap JSON path) - optional now that winner is locked
- [ ] Update root `README.md` round index with winner + submission count
- [ ] Cast post-mortem learnings + add to R4/R5 description

## Reference docs

- ZAO OS V1 Doc 768 - bounty best practices + R3 draft seed
- ZAO OS V1 Doc 769 - ZAODEVZ/zabalgames repo audit
- ZAO OS V1 Doc 786 - ZABAL Gamez brand kit rebuild audit

## Related rounds

- [R1 - Hannah Ep 17 clip-up](../r1/)
- [R2 - Best 60s POIDH ad from Ep 19](../r2/)
- R4 - TBD
