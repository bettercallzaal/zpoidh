# POIDH bounty ops - resume + history log

Most recent first. Each session entry: what happened + pending items + state of the world.

---

## 2026-05-31 - R3 cast + brand kit rebuild + zpoidh launch + closeout

### Shipped

- **POIDH bounty 1180 LIVE** - "Best ad for ZABAL Gamez", OPEN bounty, 0.0125 ETH on Base, closes 11:59pm PT Sun Jun 14, winner cast Mon Jun 15
- **8 description revisions** (v1 -> v8 final) before cast, including:
  - Solo -> OPEN bounty pivot (whale-stacking enabled)
  - All $25 references swapped to 0.0125 ETH (POIDH on Base = ETH only, no USDC)
  - Binaural beat rule replaced with sanctioned promo MP3 + source-audio + one-clear-instrumental options
  - Kenny caught Sat Jun 14 mismatch (June 14 is Sunday) - fixed
  - @kennyiscoding typo from R2 corrected to @kennyistyping
  - Two Substance beats softened ("embedded-mentor model" -> "mentor model", "live reveal stream" -> "Finals stream")
  - All horizontal-rule dividers stripped (cleaner POIDH render)
  - 6 direct download URLs added to the asset kit section
- **Brand kit fully rebuilt** at `bettercallzaal.com/assets/zabal-games-brand/` - went from 4 stub files (~952 KB) to 13 real files (~3.6 MB):
  - `logo.png` (arcade hero, 1.17 MB) + `logo-gamez.png` (1.04 MB) + `icon.png` (263 KB)
  - `og-card.svg` + `embed-card.svg` + `embed-card-gamez.png` (671 KB)
  - `palette.svg` (site, 13 tokens) + `palette-arcade.svg` (logo, 9 tokens)
  - `zabal-gamez-promo.mp3` (REAL production audio from Zaal, 49.9s, 48kHz stereo, 1.3 MB - replaced earlier synth Samantha VO placeholder)
  - `README.md` (canonical mirror of ZAODEVZ/zabalgames brand-kit-2026-05-28.md)
  - `phrases.md` (10 approved + 8 banned + 20-term glossary)
  - `asset-inventory.md` (social unfurl matrix + per-file use guide)
  - `index.html` (folder landing page so the directory URL doesn't 404 on Vercel)
- **zpoidh repo created** at github.com/bettercallzaal/zpoidh - dedicated home for every BCZ POIDH bounty's rounds + judging + brand kits + scripts + playbook. 47 files initial commit, plus vercel.json + landing index.html. Vercel deploy set up by Zaal.
- **BCZ cross-links to zpoidh** added to nexus.html, poidh.html, poidh-bounty-best-practices.html, and the brand kit README
- **R3 judging scaffold pre-built** at `bettercallzaal.com/poidh-round3-judging.html` + `.json` - empty submissions array ready to populate as R3 closes; page renders the scorecard automatically once JSON is filled
- **ZAODEVZ/zabalgames llms.txt** updated with Active POIDH Bounty section so any LLM reading zabalgamez.com gets full R3 context
- **3 ZAO OS research docs** shipped + merged:
  - Doc 768 - POIDH bounty best practices distillation + R3 draft seed
  - Doc 769 - ZAODEVZ/zabalgames repo state audit
  - Doc 786 - ZABAL Gamez brand kit rebuild audit (this session)

### Lessons logged (folded into future-round defaults)

- **POIDH on Base = ETH only.** No USDC. Convert $ prizes to ETH + 2.5% buffer at current price.
- **No on-chain deadline field.** Description is the only enforcement. Set calendar reminders.
- **Open bounties = 48h contributor vote** before winner can withdraw. Plan winner cast accordingly.
- **EOA only.** Smart Wallets revert with `ContractsCannotCreateBounties()`. Use BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af`.
- **Verify day-of-week against date** before posting. Kenny caught a Sat/Sun mismatch in R3 v5 - now a documented check in the playbook.
- **Handle accuracy matters.** @kennyistyping NOT @kennyiscoding. @yerbearserker NOT @yerbearzerker.
- **Vercel does not auto-list directories.** Any folder URL the bounty links MUST have an index.html or it 404s.
- **Brand kit MUST exist before cast.** Linking to an empty folder kills the bounty's perceived quality.
- **Audio rule:** no random library music or melodic pads under spoken dialog. Use sanctioned campaign promo MP3 OR source-episode audio OR one clear instrumental that does not compete with dialog. Layered = floor fail.

### Pending (post-close handoff items)

- [ ] Day 5 of R3 window (~Jun 5): reply-cast on the bounty thread with submission count + days-left + leaderboard hub link
- [ ] Sun Jun 14 11:00pm PT: lock R3 judging window
- [ ] Mon Jun 15 morning: run `scripts/refresh-poidh-leaderboard.py` with bounty 1180 added to defaults, ffprobe video submissions, populate `rounds/r3/judging.json`, ship judging.html update
- [ ] Pick R3 winner + cast announce + `submitClaimForVote(1180, <claim_id>)` + 48h wait + `resolveVote(1180)`
- [ ] After winner accepts ETH: cut BCZ POIDH URLs over to redirect into zpoidh Vercel deploy
- [ ] Update root README round index with R3 winner + final submission count

### Optional next-round catalytic moves (not done this session)

- DM Kenny, Tyler, Adrian, Jordan privately with `rounds/r3/cast-templates/` catalytic-dm prompts asking for 0.003 ETH public co-fund + amplification. Drafts were prepared but not sent.

---

## 2026-05-27 - R2 winner accepted + score-by-count locked

### Shipped

- R2 winner picked: @joeyofdeus / Monksage (claim 6645)
- BCZ refresh script patched: score = count of BCZ POIDH bounties submitted to (instead of flat 1 per wallet)
- Two-round submitters (Monksage + cryptfi-mariano) compounded to score 2
- BCZ PR #15 merged with the winner + score patch
- v6 winner cast posted with "congrats first + GitHub link to rest of summary" framing per Zaal preference

---

## 2026-05-26 - R2 ffprobe + per-submission scorecard page

### Shipped

- `bettercallzaal.com/poidh-round2-judging.html` shipped within 48h of close
- ffprobe-confirmed durations for all 7 video submissions
- 3 strict-floor PASS (Monksage 59.70s, Kaspa 59.70s, kayhwizard 57.49s), 2 borderline (Jony 60.21s, Dee 60.46s), 2 FAIL (Akukiwil 66.71s, Ebuka 91.88s)
- Top 4 finalists table with rubric scorecards + pros/cons + claude verdicts

---

## 2026-05-22 - R2 (bounty 1166) closed

8 claims / 7 unique editors. Best 60s POIDH ad from BCZ YapZ Ep 19 with Kenny.

---

## 2026-04-late - R1 winner accepted

@cryptfi-mariano won R1 (bounty 1151, BCZ YapZ Ep 17 Hannah / Farm Drop clip-up). Confirmed accepted on-chain 2026-05-26.

---

## Resume prompt (paste into next session)

```
Reading github.com/bettercallzaal/zpoidh/docs/RECAP.md to bootstrap context.
We are picking up BCZ POIDH bounty ops. Active state: R3 (bounty 1180,
Best ad for ZABAL Gamez) LIVE on POIDH through Sun Jun 14 2026.
Brand kit fully shipped at bettercallzaal.com/assets/zabal-games-brand/.
zpoidh repo is canonical home for all rounds + playbook.

Tell me what to work on:
(a) Mid-window reminder cast for R3 (~day 5)
(b) Post-close judging pipeline (Jun 15 morning)
(c) R4 draft / next bounty subject
(d) Migrate BCZ POIDH URLs to redirect into zpoidh deploy
(e) Something else
```
