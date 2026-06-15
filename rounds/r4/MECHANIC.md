# R4 mechanic - the open pot split (the one thing to lock before casting)

R1-R3 were single-winner ad bounties. R4 is a new type: **OPEN-SPLIT** - one pot,
many winners, split equally across everyone who clears the floor. POIDH does not do
this natively, so the payout path is a real decision. This doc lays out the options so
we can pick one before the demo Monday.

## The constraint

A POIDH OPEN bounty lets many people contribute ETH to one pot (good - that is exactly
the "anyone adds a dollar a week" mechanic). But resolution is **winner-take-all**:
`submitClaimForVote(bountyId, claimId)` -> 48h contributor vote -> `resolveVote(bountyId)`
sends the **entire** pot to **one** winning claim. There is no native "split across N
claims." So to pay everyone, we have to decide how the pot actually leaves escrow.

Also: PoidhV3 enforces `issuer != claimant`. Zaal funds + issues, so **Zaal cannot be the
winning claim**. The payout has to land on a wallet/contract that is not the issuer.

## Option A - Split contract is the winning claim (trustless, recommended)

1. Run the bounty all July as a normal OPEN pot. Anyone contributes; builders post their
   proof-photo claims.
2. When July closes, take the final list of qualifying wallets and deploy one **0xSplits**
   split contract (or equivalent) with all of them as **equal** recipients.
3. Submit that split contract address as the single "payout" claim (posted by a builder /
   co-host, not the issuer).
4. Contributors vote it through -> `resolveVote` sends the whole pot to the split contract.
5. The split contract fans the ETH out pro-rata; every builder withdraws their equal slice.

- **Pro:** trustless, on-chain, verifiable, no one holds everyone's money. Fits POIDH's
  single-winner constraint exactly.
- **Con:** the split's recipient set is fixed at deploy time, so we build it once after the
  July deadline (which is fine - the window is closed by then). One extra contract deploy.

## Option B - Distributor wallet wins, then disperses (simple, trusted)

1. Same open pot all July.
2. At close, a trusted **distributor wallet** (not the issuer - e.g. a co-host or a fresh
   ops wallet) wins the vote and withdraws the whole pot.
3. That wallet manually sends each qualifying builder an equal share (Disperse.app or a few
   sends).

- **Pro:** zero contract work, dead simple, easy to demo Monday.
- **Con:** requires trusting the distributor to actually fan it out. Less clean for a
  "back the builders" public pot where transparency is the whole pitch.

## Option C - Skip POIDH escrow, POIDH is just the proof gallery

Use the POIDH bounty purely as the **proof-of-participation** surface (the photo claims +
the public gallery), and hold the actual pot in a transparent address / Splits contract
that the community funds directly. At close, the Splits contract is already configured;
contributors funded it directly all month.

- **Pro:** the "split" is native to the funding contract from day one; no resolve gymnastics.
- **Con:** loses POIDH's built-in "stack contributions on the bounty page" UX - backers fund
  a separate address, which is a worse on-ramp than the POIDH contribute button.

## Recommendation

**Option A.** It keeps the POIDH contribute button (the easy "throw a dollar on the pot"
on-ramp the whole idea depends on) AND ends in a trustless equal split. Option B is the
fast path if we want something demo-able Monday without touching a splits contract; we can
demo with B and ship A for the real run.

## Still open (need Zaal's call)

- **Payout path:** A, B, or C?
- **Seed amount:** what does Zaal seed the pot with now, and the weekly top-up size?
- **Min builders floor:** if only 1-2 people ship, do we still split, roll the pot into the
  August curated prize, or hold it for R5?
- **"Real build" judge:** who confirms a submission cleared the effort floor (linkable,
  this-month, actually theirs)? Proposed: Zaal + one co-host, lightweight pass/fail, no
  scoring.
- **Late contributions:** contributions can land after the July deadline (people keep
  tipping). Do post-deadline funds roll into the same split (recompute) or carry to R5?

## Timeline

- Now (mid-June): seed the pot, cast it, pin it. Pot starts growing.
- July 1-31: open build month. Builders ship + post proof claims. Weekly top-ups + community
  stacking. Day-15 and day-25 reminder casts with a running "$X in the pot, N builders in"
  count.
- Fri July 31, 11:59pm PT: submissions close.
- First week of August: finalize qualifying list -> deploy split (Option A) -> vote ->
  resolve -> builders withdraw. Cast the payout + builder count before the Finals.
- Then: run `scripts/refresh-poidh-leaderboard.py` (R4 / bounty id already in defaults once
  the bounty exists - add the real id) to fold R4 submitters into the leaderboard.
