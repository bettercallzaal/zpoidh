# QR-bid-per-submission reward - design

**Status:** Design only. The bid spend is Zaal-gated (on-chain, his hand) - nothing here spends or bids.
**Board task:** `zabal-submissions-sparkz` (P1, 2026-07-16) - "Zaal is willing to pay ONE QR bid per actively-submitted ZABAL project."
**Why:** Reward without a token = pure Sparkz energy-first. A submission earns *attention*, not a coin.

## The idea in one line

For each **actively-submitted** ZABAL Gamez project, The ZAO wins one day of the QR coin auction and points the (never-changing) QR code at that project's link - 24 hours of accumulating on-chain + offline traffic, as the reward.

## QR coin auction - verified mechanics

Verified 2026-07-16 (sources below):

- **What it is:** `qrcoin.fun` runs a **daily auction on Base**. The winner chooses where a single, never-changing QR code points for the next 24 hours. Because the QR is physically and digitally static, its accumulated audience compounds over time.
- **Currency:** bids are in **USDC**.
- **Outbid = refunded:** if your bid is beaten, the funds are returned immediately - no lock-up loss.
- **Permissionless:** fully on-chain smart contracts on Base; the auction settles without an intermediary.
- **Winners announce:** the daily winner is posted by `@qrcoindotfun` on X and Farcaster, and the QR then routes traffic to the winner's URL (past winners pointed it at X profiles, token contracts, charity links, project promos).

Implication for us: winning one day gives a submitted project a full day of the QR's audience, pointed at (e.g.) its POIDH claim, its `zabalgamez.com` page, or its live build - real, measurable attention with no token issuance.

## What counts as "actively submitted"

The reward must be earnable but not gameable. A project qualifies as **actively submitted** when ALL of:

1. It has a **POIDH claim on the open ZABAL Gamez round** (currently Round 4, bounty 1249) - i.e. it entered through the existing spine, not a side channel.
2. The claim has a **working public link** (live build, demo, video, or repo) - the thing the QR would point at must resolve 200.
3. It is **non-duplicate** - one reward per distinct project, not per claim/resubmission.
4. It is **from a real participant** (not the round host) and clears the round's basic eligibility bar.

Rationale: anchoring to the POIDH claim reuses the spine that already exists (`rounds/`), keeps the on-chain record as the source of truth, and means "actively submitted" is a verifiable state, not a judgment call.

## The mechanic

```
submission (POIDH claim, live link, non-dup)
        │
        ▼
  eligible queue  ──►  one QR-auction day scheduled per project
        │                        │
        │                        ▼
        │             Zaal bids (gated) up to MAX_BID on a chosen day
        │                        │
        │             win ──► QR points at the project link for 24h
        │                        │              │
        │             outbid ──► funds refunded, re-queue for another day
        ▼
   logged: project, day, bid, win/lose, traffic delta
```

Design choices:

- **One bid per project, not per claim.** Resubmissions do not earn extra days.
- **Scheduled, not simultaneous.** Projects take the QR on different days (one QR/day exists), so the queue drains over time. This naturally rate-limits cost.
- **Off-peak scheduling.** Bids are cheaper on low-demand days; the queue should target those to control spend.
- **The link is the project's, not ours.** The reward is the project getting the attention, not The ZAO. (Optional: a lightweight interstitial on `zpoidh` that credits ZABAL Gamez then forwards - decide later; the simplest v1 points straight at the project.)
- **Announce the win** so the participant sees the reward land (X/Farcaster), reinforcing energy-first.

## Cost exposure (the part Zaal flagged as "may not be easy")

- Bids are **market-driven and variable.** Historically they have ranged from small amounts up to **~$3,500 USDC** at peak demand (mid-2025). Off-peak days are far cheaper.
- **Winning is not guaranteed.** A given day may be unaffordable; the design must treat "lost the auction" as normal (re-queue), not as owing the participant anything.
- **Controls (all Zaal-set, gated):**
  - `MAX_BID` per project - a hard ceiling; never chase a bidding war.
  - **Monthly budget cap** across all rewards - the queue pauses when hit.
  - **Target off-peak days** to maximize wins per dollar.
  - **Guaranteed-attention fallback:** if the QR is too expensive in a period, the same "reward" can be delivered through cheaper ZAO-owned surfaces (feature on `zpoidh` leaderboard, a cast from the main accounts, newsletter mention) so a submission still earns attention even when a QR day is out of budget.

Net: exposure is bounded by `MAX_BID x wins`, capped monthly, and degrades gracefully to $0-cost attention when the auction runs hot.

## Open questions (for Zaal)

1. **MAX_BID and monthly cap** - the two numbers that bound all spend. (Design leaves these blank; only Zaal sets them.)
2. **Point-at target** - straight to the project link, or through a credited `zpoidh` interstitial?
3. **Selection when the queue > available cheap days** - FIFO, judge-ranked, or leaderboard-energy-ranked (fits Sparkz "energy-first")?
4. **Who executes the bid** - Zaal by hand each time (fully gated), or a prepared bid that Zaal one-tap approves (ZOL could *watch + queue*, never *bid* - see the P2 ZOL-watcher task)?

## How this fits the spine

- **Reuses** the POIDH-claim-on-round flow already in `rounds/` - no new submission channel.
- **Feeds** the P2 task "ZOL: track + push ZABAL Gamez submissions through QR coin" - ZOL watches the eligible queue and surfaces bid-ready days; the actual bid stays human-gated.
- **Energy-first / tokenless-empire:** every submission earns real attention with zero token issuance, which is exactly the "each submission = a future Spark, not necessarily a token" framing.

## Sources

- QR coin overview + auction model: [blockspot.io/coin/qr-coin](https://blockspot.io/coin/qr-coin/), [gate.com QRcoin explainer](https://www.gate.com/learn/articles/qrcoin-how-this-base-ecosystem-newcomer-is-revolutionizing-on-chain-auctions-with-qr-codes/9619)
- "On-chain attention machine" + ~$3,500 peak bids: [techbuzz.ai](https://www.techbuzz.ai/articles/the-on-chain-attention-machine), [bankless.com](https://www.bankless.com/read/a-new-onchain-attention-machine)
- Mechanics + never-changing QR thesis: [panewslab.com](https://www.panewslab.com/en/articles/3h4w89xw), [okx.com news](https://www.okx.com/en-gb/news/article/does-qrcoin-new-favourite-base-ecosystem-use-qr-codes-play-chain-auctions-46662521004064)
- Official: [qrcoin.fun](https://www.qrcoin.fun/), [@qrcoindotfun](https://x.com/qrcoindotfun)
