# Round N - <campaign name>

Copy this folder to `rounds/r{N}/` and fill in the placeholders for the next bounty.

## Files

- `description.md` - the POIDH Description field, paste-ready
- `promo-cast.md` - the launch Farcaster cast + X cross-post
- `cast-templates/` - winner announce / thanks-to-all / honorable mentions / catalytic DMs
- `judging.json` - per-submission scorecard data (build after deadline)
- `judging.html` - per-submission scorecard UI (copy from `rounds/r2/judging.html`, swap the JSON path)
- `durations.json` - ffprobe results per submission video (if video bounty)
- `thumbs/` - first-frame thumbnails per submission (if video bounty)

## Workflow checklist

- [ ] Confirm subject + prize + win-mechanic with stakeholders
- [ ] Draft `description.md` using `docs/bounty-best-practices.html` as the bar
- [ ] Confirm asset kit exists at `assets/brand-kits/<campaign>/` (mirror from canonical source if needed)
- [ ] POIDH UI -> Create OPEN bounty on Base with description + reward seed
- [ ] Cast `promo-cast.md` content with bounty URL as embed
- [ ] Pin in home channel
- [ ] Firefly cross-post to X
- [ ] Optional: catalytic DMs to whale contributors (cast-templates/catalytic-dm.md)
- [ ] Day 5: reply-cast with submission count + days-left
- [ ] Close + 1 day: ffprobe all videos -> `durations.json`, build `judging.json`
- [ ] Close + 2 days: ship `judging.html` + winner cast
- [ ] `submitClaimForVote` on POIDH -> 48h vote -> `resolveVote` -> winner withdraws
- [ ] Run `scripts/refresh-poidh-leaderboard.py` with new bounty ID added to defaults
- [ ] Update the main `README.md` round index
- [ ] Cast post-mortem learnings + add to the next round's description
