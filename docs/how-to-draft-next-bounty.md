# How to draft + cast the next BCZ POIDH bounty

Step-by-step playbook. Use this with the README round index + the `rounds/_template/` starter files.

---

## 0. Prereqs (one-time setup)

- BCZ Treasury EOA `0x7234c36a71ec237c2ae7698e8916e0735001e9af` connected to POIDH UI (must be EOA, not Smart Wallet)
- ~0.015 ETH on Base in that wallet (prize seed + gas)
- Network switched to Base before hitting Create
- The relevant Farcaster channel exists + you can post in it
- A brand kit exists under `assets/brand-kits/<campaign>/` if the bounty is campaign-tied

---

## 1. Decide the basics

| Field | Decision |
|---|---|
| Subject | What is the bounty FOR (an ad, a clip, a recap, a proof-of-attendance, etc.) |
| Source | Where editors pull material from (episode, event, page, channel) |
| Format gate | Specific format (e.g. 45-60s video) OR open ("any format")? Open ads catch more editors; specific clips force craft. |
| Prize | Default 0.0125 ETH on Base (covers ~$25 worth + 2.5% protocol fee) |
| Bounty type | OPEN (default - lets contributors stack, contributor vote at end) or SOLO (you fund + accept, no vote, faster) |
| Window | Default 14 days. Minimum 7 if event-tied, max 21 for production-heavy asks |
| Home channel | `/zabal` for ZG bounties, `/zao` for general ZAO ops, `/poidh` is always a cross-post |
| Catalytic DMs | If OPEN, decide whether to DM whales (Kenny, Tyler, Adrian, Jordan, Haberdashery) for public 0.003 ETH co-funder drops before cast |

---

## 2. Copy the template

```bash
cd zpoidh
N=4                                                    # next round number
CAMPAIGN=<campaign-slug>                               # e.g. "wavewarz", "zaostock"
cp -r rounds/_template rounds/r$N
```

---

## 3. Write `description.md`

Open `rounds/r$N/description.md`. Replace every `<PLACEHOLDER>`. Mirror the structure of `rounds/r3/description.md` (the v8 R3 description that landed on bounty 1180).

Mandatory:
- THE BAR with 5 numbered floor rules (audio rule = rule 5 always)
- THE RUBRIC grouped by Distribution / Craft / Substance / Bonus
- THE ASSET KIT with both the GitHub folder URL AND 5-8 direct download URLs
- THE REWARD - prize + winner-cast pinned promo + Empire Builder ZABAL trail with score-by-count language
- DEADLINE - exact PT date + day-of-week double-checked (Kenny caught a Sat/Sun mismatch in R3 v5)

Voice rules (per ZABAL Gamez brand kit `phrases.md`):
- No emojis. No em dashes. Hyphens only.
- No "hackathon" - say "Build-A-Thon" or "build event"
- No "pitch competition"
- No crypto/web3 jargon in PUBLIC copy
- "100+" for ZAO member count
- "Build for a real community, not a weekend you forget."
- Use `@kennyistyping` on X NOT `@kennyiscoding` (R2 typo - corrected R3+)

Cite the canonical bar at the end of the asset kit section:
```
Canonical bounty bar:
https://bettercallzaal.com/poidh-bounty-best-practices.html
```

---

## 4. Write `promo-cast.md`

Open `rounds/r$N/promo-cast.md`. Three versions:
- Farcaster long (drops bounty URL first, then context, then CTAs)
- X short (under 280)
- Telegram / GC / Discord (mid-length)

Plus a reply-cast for after the main lands.

---

## 5. Cast it on POIDH

1. POIDH UI -> Create bounty
2. Type = OPEN (default) or SOLO (if no vote needed)
3. Network = Base
4. Title = clean noun phrase (e.g. "Best ad for ZABAL Gamez")
5. Description = paste from `description.md`
6. Reward seed = 0.0125 ETH (or your decided amount)
7. Sign with BCZ Treasury EOA
8. Capture the resulting bounty URL (poidh.xyz/base/bounty/NNNN)

---

## 6. Cast the launch

1. Cast Farcaster long in the home channel (e.g. `/zabal`) with bounty URL as embed
2. Cross-post to `/poidh` (5,594 followers, bounty-curious audience) and `/zao` (83 ZAO members)
3. Firefly cross-post the X short to X
4. Pin the home-channel cast for the bounty window
5. Drop the reply-cast on the thread shortly after main lands

---

## 7. Optional catalytic contributor DMs (OPEN only)

Send `rounds/r$N/cast-templates/catalytic-dm.md` privately to Kenny, Tyler, Adrian, Jordan. Asks them to drop 0.003 ETH each as a public co-funder. Same Jesse-Pollak-on-bounty-906 pattern from POIDH lifetime (per ZAO OS V1 doc 759 + 631). Triggers a submission wave.

---

## 8. Mid-window reminder (day 5)

Reply-cast on the thread with submission count + days-left + leaderboard hub link. Keeps the bounty visible in the timeline.

---

## 9. Judging

After close:

```bash
# Add the new bounty ID to the refresh script defaults
sed -i '' "s/DEFAULT_BOUNTY_IDS = \[.*\]/DEFAULT_BOUNTY_IDS = [1151, 1166, 1180, NEW_ID]/" scripts/refresh-poidh-leaderboard.py

# Run the refresh
python3 scripts/refresh-poidh-leaderboard.py

# Commit updated leaderboard + claims + audit
git add data/ scripts/refresh-poidh-leaderboard.py
git commit -m "refresh: post-close pull for round $N (bounty $NEW_ID)"
```

For video bounties:
```bash
# Download every submission MP4
mkdir -p /tmp/r$N-mp4s && cd /tmp/r$N-mp4s
# (curl each X video URL from claims.json)

# ffprobe every video for duration
for f in *.mp4; do
  ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$f"
done > durations-raw.txt

# Build durations.json + judging.json + ship judging.html
# Reference: rounds/r2/durations.json + rounds/r2/judging.json + rounds/r2/judging.html
```

Floor-fail per spec. Do not inflate verdict to clear the bounty.

Publish per-submission scorecard at `bettercallzaal.com/poidh-round<N>-judging.html` within 48h.

---

## 10. Winner cast + on-chain finalize

1. Pick winner using rubric scores from `judging.json`
2. Cast winner announce (template at `rounds/r$N/cast-templates/winner-announce.md`)
3. For OPEN bounty:
   - Call `submitClaimForVote(bountyId, winningClaimId)` on POIDH
   - Wait 48h for contributor vote
   - Call `resolveVote(bountyId)` after deadline
   - Winner can then call `withdraw()` to pull ETH
4. For SOLO bounty:
   - Call `acceptClaim(bountyId, winningClaimId)` directly - winner can withdraw immediately
5. Reply-cast to winner on the thread with a 1-line credit

---

## 11. Post-round housekeeping

- Update root `README.md` round index table with winner + submission count
- Cast post-mortem learnings + add to next round's description
- DM honorable mentions privately (template at `rounds/r$N/cast-templates/honorable-mention.md` if you add one)
- If a major lesson surfaced (like R2's audio rule), update `docs/bounty-best-practices.html` + `phrases.md` in the brand kit

---

## Where things live

| What | Path |
|---|---|
| Canonical bar | `docs/bounty-best-practices.html` |
| Template for new round | `rounds/_template/` |
| Past rounds | `rounds/r1/`, `rounds/r2/`, `rounds/r3/` |
| Brand kits | `assets/brand-kits/<campaign>/` |
| Live EB feed | `data/leaderboard.json` (also at `bettercallzaal.com/poidh-leaderboard.json` during the cut-over window) |
| Refresh script | `scripts/refresh-poidh-leaderboard.py` |
| Resume + history | `docs/RECAP.md` |

---

## Common gotchas

- **POIDH does not support USDC on Base.** Native ETH only. Convert your $ prize to ETH at current price + 2.5% buffer.
- **EOA only.** Smart Wallets revert with `ContractsCannotCreateBounties()`. Use the BCZ Treasury EOA.
- **No on-chain deadline field.** The DEADLINE you write in the description is convention - POIDH bounties stay open until you accept or cancel. Set a calendar reminder.
- **Open bounty = 48h vote.** Plan the winner cast 48h after `submitClaimForVote`.
- **Date / day-of-week double-check.** Use `python3 -c "import datetime; print(datetime.date(2026,6,14).strftime('%A'))"` to verify before posting. R3 v5 fixed a Sat/Sun mismatch caught by Kenny.
- **Handle accuracy.** @kennyistyping NOT @kennyiscoding. @yerbearserker NOT @yerbearzerker. Check `assets/brand-kits/<campaign>/phrases.md` glossary.
- **Brand kit MUST exist before cast.** Linking to an empty folder kills the bounty. Build the kit first.
- **Folder URL needs `index.html`.** Vercel does not auto-list directories. If the asset kit is at a folder URL, ship an `index.html` in it.
