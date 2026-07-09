# R3 - Best ad for ZABAL Gamez

POIDH bounty 1180 on Base. Cast 2026-05-31. Closed 2026-06-14. **WINNER ACCEPTED ON-CHAIN.**

Correction 2026-07-08: a live re-pull (`scripts/refresh-poidh-leaderboard.py`) shows claim
6749 (femmie, "ZABALGAMEZ.COM AD") already carries `isAccepted: true` - the same field that
flags the confirmed R1 and R2 winners in this repo's data. That means `submitClaimForVote`
already ran for this claim, most likely by Zaal outside a tracked session. Whether the 48h
vote has resolved and the winner has withdrawn isn't confirmed from this read-only data pull.
See [judging.json](judging.json) for the full claim list + what's still open.

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
- [ ] Confirm `resolveVote(1180)` has run + femmie withdrew (needs an on-chain read, not done this session)
- [ ] Draft + post winner-announce cast (femmie) - see `cast-templates/winner-announce-femmie.md`
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
