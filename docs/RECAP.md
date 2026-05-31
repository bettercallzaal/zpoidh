# POIDH x $ZABAL Empire - Session Recap (last updated 2026-05-26)

> Resume artifact. Paste the prompt at the bottom into the next session to bootstrap context.

## 2026-05-26 update (overnight session)

- **Round 1 closed** - claim 6368 (@cryptfi-mariano) ACCEPTED on-chain. Winner paid out 0.0105 ETH.
- **Round 2 (bounty 1166) closed 2026-05-22** - 8 submissions, 7 with X videos + 1 floor-fail text-only.
- **Real durations resolved via ffprobe** - 3 strict-floor PASS (6645=59.70s, 6584=59.70s, 6585=57.49s), 2 NEAR-OVER (6586=60.21s, 6608=60.46s), 2 FAIL-OVER (6644=66.71s, 6616=91.88s).
- **Top pick: claim 6645 (@joeyofdeus / Monksage)** - only clean-floor submission with all three brand tags (@bettercallzaal + @kennyistyping + @poidhxyz) + names BCZ YapZ Ep 19 + Kenny in copy.
- **Painful demote: claim 6616 (@remixitphotos / Ebuka)** - cohort's strongest copy (Seattle trash, healthcare examples from Ep 19), DROPPED to FLOOR_FAIL_DURATION at 91.88s vs 60s cap.
- **Per-submission judging page LIVE at bettercallzaal.com/poidh-round2-judging.html** - per-card pros/cons + scenarios + decision matrix + compare table + cast templates + winner-pick form. Nav links added from /poidh.html + /nexus.html.
- **EB slot 8 leaderboard refreshed** - 10 -> 16 unique submitters. ZABAL distribution flows automatically on next EB refresh cycle.

## What's LIVE right now

- **`bettercallzaal.com/poidh.html`** = canonical UI for $ZABAL Empire slot 8 "POIDH Submitters" leaderboard.
  - Compressed hero, action-led copy ("Make POIDH's next ad - earn ETH + ZABAL").
  - Two scrolling marquees above the fold: handle chips (avatars + @handles + ZABAL totals) and claim image thumbnails.
  - Round 2 LIVE card full-width primary; Round 1 details + 11-card gallery tucked behind a `<details>` collapse.
  - Live leaderboard table with avatars + handles pulled from EB + web3.bio.
  - Round 2 Submissions section with "Be the first ->" empty state.
  - Footer one-liner with lifetime ZABAL distributed total.
  - API hook + "for builders" section deleted.

- **Bounty 1166 LIVE on POIDH** - "Best 60s POIDH ad from Ep 19 w/ Kenny" - 0.006+ ETH open bounty on Base.
  - Album = `wethemmedia`. Closes Fri May 22, 11:59pm PT. Winner cast Sun May 24.
  - Floor + rubric structure (3-line floor; Distribution / Craft / Substance / Bonus tiers).

- **$ZABAL Empire on Empire Builder**
  - Empire ID `0xbB48f19B0494Ff7C1fE5Dc2032aeEE14312f0b07`
  - SmartVault `0xe0faa499d6711870211505bd9ae2105206af1462`
  - Owner: Zaal `0x7234c36a71ec237c2ae7698e8916e0735001e9af`
  - Slot 8 apiLeaderboard "POIDH Submitters" wired to `https://bettercallzaal.com/poidh-leaderboard.json`
  - Leaderboard UUID `7b8e8dfa-529d-48ad-8c9b-bdb45cc35187`
  - 10 unique Round 1 submitters, 13.35 ZABAL distributed lifetime, EB-resolved Farcaster handles for all 10.

- **Refresh script** `scripts/refresh-poidh-leaderboard.py` (stdlib only)
  - Defaults to bounties [1151, 1166] on Base 8453
  - Writes 3 files: `poidh-leaderboard.json` (strict EB feed), `poidh-claims.json` (rich page data), `poidh-audit.json` (verification trail)
  - Uses 3 free APIs no key needed: poidh.xyz tRPC + empirebuilder.world reads + api.web3.bio profiles

## What's PENDING (still owed)

1. **Accept @cryptfi-mariano's claim 6368 on bounty 1151** from issuer wallet `0x7234...e9af`. POIDH protocol does not auto-pay until this tap. Round 1 not closed on-chain yet.
2. **Cast the Round 1 winner announcement** - paste-ready template was in `/tmp/clipboard.html` (regenerable any time from the recap below).
3. **Flip Token Boosters + Reputation Boosters toggles ON for slot 8** via Empire dashboard. Today all 3 booster toggles are OFF; the 3 configured boosters (zaal Zora coin 5x, ZAAL newsletter 5x, Quotient reputation) aren't amplifying anyone yet.
4. **Cast Round 2 kickoff** in /poidh + /zao + X (paste-ready in clipboard).
5. **DM @mr94t3z** courtesy intro after Sentinel fork is live (Day 13 of the 14-day plan; not before).

## Next BIG thing: Sentinel-for-ZAO fork

Decided strategic frame:
- **Bet:** POIDH = ZAO's back-end coordination layer (volume + automation, not flagship narrative).
- **Constraint:** Zaal's own time.
- **Pitch:** "ZAO turns events into payouts via on-chain proof."

Three answers point to one move: ship `@zao-sentinel` autonomous bot ASAP.

- Source: `github.com/0x94t3z/poidh-sentinel` (MIT, ~$0/mo on Vercel + Neon + Neynar free tiers, free LLM via Cerebras/Groq/OpenRouter, free OCR via ocr.space).
- ~80% reusable. Real edits: `src/settings/app-settings.json` (branding), `src/settings/app-images.json` (logo), `src/features/bot/agent.ts` (SYSTEM_PROMPT head + AUTONOMOUS_BOUNTY_IDEAS array).
- **V1 scope:** ZABAL drops stay manual via Empire dashboard. No EB integration in bounty-loop.ts. No co-emperor add tx. No EMPIRE_BUILDER_API_KEY request.
- **Phase 2** (after bot has cleanly resolved 5+ bounties): wire atomic EB `distribute-prepare` in same tick as `acceptClaim`. Snippet preserved in doc 631 Part 3.

14-day plan (next session can resume on Day 1):

| Day | Move |
|---|---|
| 1 | Fork poidh-sentinel on GitHub. Clone. `npm install`. `npm run dev`. |
| 2 | Register `@zao-sentinel` Farcaster FID ($1). Neon free DB. Neynar dev app. Managed signer UUID. |
| 3 | Fill `.env` + `app-settings.json` + `app-images.json` with ZAO branding. New EOA bot wallet funded 0.05 ETH on Base. |
| 4 | Deploy to Vercel. Test webhook + cron. |
| 5-7 | Swap `AUTONOMOUS_BOUNTY_IDEAS` (5 ZAO event templates: fractal Monday, BCZ YapZ clip, COC concert, ZAO Stock photo, real-world connection) + `SYSTEM_PROMPT` head. |
| 8 | First live test: next Fractal Monday (2026-05-18), mention `@zao-sentinel` in /zao. |
| 9-10 | 2-3 more test bounties across event types. Tune prompts. Manual ZABAL drops via Empire dashboard. |
| 11-12 | Buffer for fixes. |
| 13 | Courtesy cast to @mr94t3z with fork link + demo + credit. |
| 14 | Public launch post: "ZAO turns events into payouts via on-chain proof." Pin in /zao + /poidh + X. |

## Reference docs (ZAOOS research library)

| Doc | Topic |
|---|---|
| 625 | POIDH x ZAO bounty playbook (18 templates, prize curves, judging rules) |
| 626 | Empire Builder + ZABAL POIDH airdrop architecture (EB pulls BCZ via apiLeaderboards) |
| 627 | $ZABAL Empire ground truth + EB v3 capabilities (you own it, 11 leaderboard types) |
| 628 | Bounty-writing + integration learnings (Kenny's POIDH framework, multi-hour journey) |
| 629 | Live leaderboard data architecture (3 free APIs: EB + web3.bio + poidh.xyz tRPC) |
| 631 | POIDH x $ZABAL x Sentinel convergence map (14 ideas ranked, 14-day plan, atomic ZABAL snippet preserved) |

## Key URLs / IDs

| Thing | Value |
|---|---|
| Live page | https://bettercallzaal.com/poidh.html |
| EB JSON feed | https://bettercallzaal.com/poidh-leaderboard.json |
| Rich page data | https://bettercallzaal.com/poidh-claims.json |
| Round 2 bounty | https://poidh.xyz/base/bounty/1166 |
| Round 1 bounty | https://poidh.xyz/base/bounty/1151 |
| $ZABAL Empire dashboard | https://empirebuilder.world/empire/0xbB48f19B0494Ff7C1fE5Dc2032aeEE14312f0b07 |
| Empire Builder SKILL | https://www.empirebuilder.world/skill/SKILL.md |
| poidh-sentinel repo | https://github.com/0x94t3z/poidh-sentinel (MIT) |
| BCZ YapZ Ep 19 (Kenny) | https://www.youtube.com/watch?v=IFG_34K7Vig |
| Kenny POIDH framework cast | https://farcaster.xyz/kenny/0xbb5f295f |

## Resume prompt (paste this into next session)

```
Reading /Users/zaalpanthaki/Documents/BetterCallZaal/POIDH-RECAP.md to bootstrap context. We're picking up the POIDH + $ZABAL Empire + Sentinel-for-ZAO work. The live state is in the recap. The pending items are in the recap. The 14-day Sentinel fork plan is in the recap. Confirm what's still pending today (Mariano claim accept, Round 1 winner cast, booster toggles, Round 2 kickoff cast) then ask me which thread to pull on: (a) close out pending items, (b) start Sentinel fork Day 1, (c) Round 2 mid-week nudge, (d) something else. Caveman mode.
```
