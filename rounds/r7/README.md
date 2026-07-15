# R7 - ZABAL Gamez bug fixes bounty

First CODE bounty in the series. R1-R6 were clip/content bounties (Unlock clipping, etc.);
R7 crowdsources real bug fixes for the ZABAL Gamez platform. Submissions are pull requests,
not clips.

## At a glance

- **Source:** [zabalgamez.com](https://zabalgamez.com) - the build-a-thon platform (workshops, portal, submissions, season quest, wins page)
- **Format:** bug fix - a public PR (or a clear patch + writeup if the fixer cannot PR) that fixes a real bug
- **Deadline:** cast-date + 14 days, 11:59pm PT (code takes longer than clips, so a 2-week window vs the usual 7)
- **Judge:** single judge (Zaal)
- **Issuer:** BCZ Treasury EOA / whichever wallet Zaal connects in [docs/create-bounty.html](../../docs/create-bounty.html)
- **Reward:** seeded by Zaal at create time. NOT winner-take-all - multiple strong fixes can each be paid, because the point is making ZABAL Gamez better.

## Why this one is different

R1-R6 judged clips. R7 judges code: impact (does it fix a real user-blocking bug) plus craft
(clean, minimal diff that does not break anything else). Best fixes get merged. This is also
the trust-ladder first step for ZOL toward money actions - a controlled, human-funded bounty
ZOL can help scope + judge without ever holding funds.

## Files in this folder

- `description.md` - the POIDH Description field, paste-ready (between the sentinel lines)
- `promo-cast.md` - launch Farcaster cast + X cross-post

## Workflow checklist

- [ ] Confirm reward seed with Zaal
- [ ] POIDH UI (or docs/create-bounty.html) -> Create OPEN bounty on Base with this description
- [ ] Cast `promo-cast.md` with the bounty URL as embed; pin in the ZABAL Gamez channel
- [ ] Firefly cross-post to X
- [ ] Day 7: reply-cast with submission count + days-left
- [ ] Close + review PRs; merge the strong ones; pay each qualifying fix
- [ ] Update the main `README.md` round index
