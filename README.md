# zpoidh - BCZ POIDH bounty ops

Source of truth for every BCZ-issued POIDH bounty. Rounds, judging pages, brand kits, leaderboard refresh, the canonical bar, the lessons learned. Everything you need to draft + cast + judge the next round lives here.

**Active bounty:** [Round 3 - Best ad for ZABAL Gamez](https://poidh.xyz/base/bounty/1180) (open through Sun Jun 14, 2026)

**Live surfaces (still on `bettercallzaal.com` during the R3 window):**
- Hub: https://bettercallzaal.com/poidh.html
- Best practices: https://bettercallzaal.com/poidh-bounty-best-practices.html
- R2 judging: https://bettercallzaal.com/poidh-round2-judging.html
- Brand kit: https://bettercallzaal.com/assets/zabal-games-brand/
- EB leaderboard feed: https://bettercallzaal.com/poidh-leaderboard.json

After R3 closes + winner cast, those URLs cut over to redirect into this repo's Vercel deploy.

---

## What this repo holds

```
zpoidh/
├── README.md                        # this file
├── docs/
│   ├── bounty-best-practices.html   # canonical bar (use for every bounty)
│   ├── poidh-hub.html               # the live hub UI source
│   └── RECAP.md                     # resume artifact + history log
├── rounds/
│   ├── _template/                   # starter files for the NEXT round
│   ├── r1/                          # Hannah Ep 17 clip-up (bounty 1151, Apr 2026)
│   ├── r2/                          # Best 60s POIDH ad from Ep 19 (bounty 1166, May 2026)
│   └── r3/                          # Best ad for ZABAL Gamez (bounty 1180, May-Jun 2026)
├── assets/
│   └── brand-kits/
│       └── zabal-games/             # full CC-BY kit (used by R3)
├── data/
│   ├── leaderboard.json             # the EB-pulled feed (`[{address, score}]`)
│   ├── claims.json                  # rich page data
│   ├── audit.json                   # audit trail
│   └── zabal-preview.json           # EB snapshot per submitter
└── scripts/
    └── refresh-poidh-leaderboard.py # canonical refresh script
```

---

## How to draft + cast the next BCZ POIDH bounty (the playbook)

### 1. Pick the subject + the win
- What is the bounty FOR? (an ad, a clip, a recap, a proof-of-attendance, etc.)
- What is the prize? Default = 0.0125 ETH on Base (covers ~$25 worth + 2.5% protocol fee).
- What gets the WINNER beyond ETH? (pinned promo, feature in newsletter, etc.)
- What gets EVERY submitter? Slot 8 of $ZABAL Empire (`0xbB48f19B0494Ff7C1fE5Dc2032aeEE14312f0b07`) - score = count of BCZ POIDH bounties they have entered.

### 2. Decide bounty type
- **OPEN** = others can stack contributions on top + contributor-weighted vote at the end. Use this when you want catalytic momentum (Jesse Pollak / Haberdashery whale pattern). All BCZ rounds so far have been OPEN.
- **SOLO** = you fund + you accept directly, no vote. Use when judging is yours alone and you want fast resolution. Trade-off: no whale-stacking mechanic.

### 3. Write the description
Use [docs/bounty-best-practices.html](docs/bounty-best-practices.html) as the canonical bar. Required sections in order:
1. One-paragraph WHY (link to source episode / event / page)
2. **THE BAR** - 3-5 numbered floor rules ("do these or you are not in the running")
3. **THE RUBRIC** - grouped by Distribution / Craft / Substance / Bonus with `+` checkboxes
4. **THE ASSET KIT** - link to GitHub brand folder + direct download URLs for editors
5. **THE REWARD** - prize + winner-cast distribution + EB ZABAL trail for all submitters
6. **DEADLINE** - exact PT date/time + winner cast date

Floor rules MUST include:
- Tag `@bettercallzaal` on X
- Cross-post in the relevant Farcaster channel (`/zabal`, `/zao`, etc.)
- Submit X URL on POIDH bounty page
- AUDIO rule: official promo MP3 from brand kit OR source-episode audio OR one clear instrumental that does not compete with dialog. Layered melodic music over spoken dialog = floor fail.

Use the existing rounds as reference:
- [rounds/r3/description.md](rounds/r3/description.md) (newest, ZABAL Gamez ad)
- [rounds/r2/judging.json](rounds/r2/judging.json) → has full R2 description + rubric

### 4. Cast it
- POIDH UI → Create → OPEN, Base, title, paste description
- Reward seed: 0.0125 ETH (or your chosen amount + 2.5% buffer)
- Wallet: BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af` (must be EOA, not Smart Wallet - POIDH reverts on contract callers)
- Album: `wethemmedia` (continuity with R1+R2+R3)
- Cast on `/zabal` (or relevant channel) + `/poidh` + `/zao` with the bounty URL as embed
- Pin in the home channel for the bounty window
- Firefly cross-post to X

### 5. Set reminders
- Day 5 of window: reply-cast with "N submissions so far, deadline in X days, gallery: bettercallzaal.com/poidh.html"
- Close date + 1: lock judging
- Close date + 2: cast winner

### 6. Judge
- Use [rounds/_template/judging.json.template](rounds/_template/judging.json.template) as the starter
- Run `ffprobe` on every video to confirm duration vs spec
- Floor-fail per spec; do not inflate to clear the bounty
- Ship per-submission scorecard at `/poidh-round{N}-judging.html` within 48h
- Use the canonical scorecard structure from [rounds/r2/judging.html](rounds/r2/judging.html)

### 7. Post-bounty
- For OPEN bounty: call `submitClaimForVote(bountyId, claimId)` → 48h contributor vote → `resolveVote(bountyId)` → winner withdraws
- Run [scripts/refresh-poidh-leaderboard.py](scripts/refresh-poidh-leaderboard.py) to update the EB feed
- Add winner clip to the hub gallery
- Push final state to GitHub before drafting the next round

---

## The hard audio rule (locked 2026-05-28, evolved from R2 post-mortem)

> No random background music or ambient audio under dialog in any BCZ POIDH bounty submission. If you want non-silence, use the official campaign promo MP3 (e.g. `assets/brand-kits/zabal-games/zabal-gamez-promo.mp3`), original source-episode audio, or one clear instrumental that does not compete with spoken dialog. Layered melodic music over spoken dialog = automatic floor fail.

Why: R2 had submissions where Kenny's voice was buried under cinematic ambient pads - the editor's craft was real but the message disappeared. POIDH ads are watched at 50% volume on Farcaster + X with subtitles on.

This rule lives in every round's description starting from R3.

---

## Score-by-count mechanic (locked 2026-05-27)

Every BCZ POIDH submitter lands on slot 8 of $ZABAL Empire (`POIDH Submitters` leaderboard). Each wallet's `score` = the count of BCZ POIDH bounties they have submitted to. Empire Builder distributes $ZABAL proportional to score every refresh cycle.

- Submitter who entered R1 only = score 1
- Submitter who entered R1 + R2 = score 2
- Submitter who entered R1 + R2 + R3 = score 3 (compounds linearly)

Token Boosters + Reputation Boosters intentionally OFF (cleanest mechanic, no Talent Protocol or token-holder confounders).

Update via `scripts/refresh-poidh-leaderboard.py` - reads POIDH tRPC, aggregates per-wallet counts, writes the strict EB feed at `data/leaderboard.json`. EB pulls from `https://bettercallzaal.com/poidh-leaderboard.json` during the R3 window; after cut-over it pulls from this repo's Vercel deploy.

---

## Round index

| Round | Bounty | Episode / Source | Prize | Winner | Submissions | Doc |
|---|---|---|---|---|---|---|
| R1 | [1151](https://poidh.xyz/base/bounty/1151) | BCZ YapZ Ep 17 (Hannah / Farm Drop clip-up) | 0.0105 ETH | @cryptfi-mariano (claim 6368) | 11 claims / 10 editors | [rounds/r1/](rounds/r1/) |
| R2 | [1166](https://poidh.xyz/base/bounty/1166) | BCZ YapZ Ep 19 (Best 60s POIDH ad w/ Kenny) | 0.0105 ETH | @joeyofdeus / Monksage (claim 6645) | 8 claims / 7 editors | [rounds/r2/](rounds/r2/) |
| R3 | [1180](https://poidh.xyz/base/bounty/1180) | ZABAL Gamez ad (any format) | 0.0125 ETH | OPEN through Sun Jun 14, 2026 | live | [rounds/r3/](rounds/r3/) |

---

## Brand kits

Each campaign gets a CC-BY brand kit under `assets/brand-kits/<campaign>/`. The kit holds the canonical logo, palette, typography spec, voice rules, approved/banned phrases, glossary, and an official 50-second promo audio file editors can use freely.

Current campaigns:
- [`assets/brand-kits/zabal-games/`](assets/brand-kits/zabal-games/) - for R3 (active) and any future ZABAL Gamez bounties

Future campaigns get their own subfolder when launched.

Each kit mirrors a canonical source repo (e.g. `github.com/ZAODEVZ/zabalgames` for ZABAL Gamez). Sync target: weekly during the active campaign. If a kit and its canonical source disagree, the source wins.

---

## Where to go for more

- **Doc 768** (ZAO OS V1) - canonical bounty best practices distillation
- **Doc 769** (ZAO OS V1) - the ZAODEVZ/zabalgames repo audit
- **Doc 786** (ZAO OS V1) - the ZABAL Gamez brand kit rebuild audit
- **Doc 759** (ZAO OS V1) - POIDH history (Kenny + lifetime stats + cohort patterns)
- **Doc 631** (ZAO OS V1) - POIDH x $ZABAL x Sentinel convergence map
- **Doc 625** (ZAO OS V1) - POIDH x ZAO bounty playbook (18 templates)
- **[docs/RECAP.md](docs/RECAP.md)** - resume artifact + ongoing state

---

## License

This repo: MIT.

Brand kits inside `assets/brand-kits/`: CC-BY 4.0 (per each kit's own README). Remix freely - keep the campaign name + canonical URL visible in your final piece.

---

Maintained by Zaal / BetterCallZaal. POIDH bounties are BCZ-issued + Zaal-funded. Issuer wallet: BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af` on Base.
