# ERC20 bounty rewards - PoidhV2 fork

The live POIDH protocol (poidh.xyz) only accepts native ETH as a bounty reward - no
USDC, no arbitrary ERC20 (see the "POIDH on Base = ETH only" lesson in the root README).
To let a bounty be funded and paid out in any ERC20 token (so Zaal could use his own
tokens instead of ETH), we forked the contract itself rather than the poidh-sentinel bot.

## What exists

- **Fork:** [github.com/bettercallzaal/poidh-v2-contracts](https://github.com/bettercallzaal/poidh-v2-contracts)
  (forked from `picsoritdidnthappen/poidh-v2-contracts`, the public MIT-licensed Solidity
  source for `PoidhV2`)
- **PR:** [#1 - Add optional ERC20 bounty rewards to PoidhV2](https://github.com/bettercallzaal/poidh-v2-contracts/pull/1)
- **What it adds:** `Bounty.token` field (`address(0)` = native ETH, unchanged behavior)
  + `createSoloBountyWithToken` / `createOpenBountyWithToken` / `joinOpenBountyWithToken`
  entry points that pull an ERC20 via `transferFrom`. Cancel/withdraw/accept-claim all
  branch internally and pay out via `SafeERC20` for token bounties. 12 new Hardhat tests,
  all pre-existing native-ETH tests still pass unmodified.

## What does NOT exist yet

- **Not deployed anywhere.** This is contract + tests only, on a feature branch in a
  fork. No mainnet or testnet address.
- **No frontend.** poidh.xyz's UI only talks to the official, unmodified `PoidhV2`
  contract - it has no knowledge of this fork or its token functions. Using it today
  means calling the contract directly (ethers.js/cast) after it's deployed, not clicking
  through poidh.xyz.
- **Separate from zpoidh's bounty rounds (R1-R5).** Those all run on the real, official
  POIDH contract on Base and are unaffected by this fork. This fork would only come into
  play if/when Zaal decides to deploy it and fund a bounty in a specific ERC20 (e.g. one
  of his own tokens) rather than ETH.

## Next step (Zaal's call - not done)

Deploy the fork to Base (or wherever), point a script or minimal UI at it, and test
creating + accepting a token-funded bounty end to end before using it for anything real.
