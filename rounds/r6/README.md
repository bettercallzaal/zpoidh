# R6 - Unlock Protocol clipping bounty (ZABAL Gamez workshop) - RECURRING

Not cast yet. First real use of the standalone [docs/create-bounty.html](../../docs/create-bounty.html)
tool (PR #17) - Zaal connects his own browser wallet and casts this directly, no
Farcaster app required.

## At a glance

- **Source:** [ZABAL Gamez workshop w/Ceci Sakura (Unlock Protocol)](https://zabalgamez.com/recordings/32),
  recorded 2026-06-30 - Ceci deploys a certification live on Base and demos memberships/tickets/token-gated access
- **Format:** clip-up (any format showing what Unlock does)
- **Deadline:** auto-computed as cast-date + 7 days by the tool, 11:59pm PT
- **Judge:** single judge (Zaal)
- **Issuer:** whichever wallet Zaal connects in the tool (BCZ Treasury EOA recommended for continuity with R1-R4, but the tool works with any connected wallet)

## This is a recurring series, not a one-off

Per Zaal's request: once this round completes, the exact same bounty can be run again
with only the version number changing - v2 the second time, v3 the third, etc. No new
round folder needed for each re-run; this one file (`description.md`) is the template
for the whole series.

How the versioning actually works, live, with no manual bookkeeping:

1. `docs/create-bounty.html` fetches this folder's `description.md` as the canonical
   copy template (between the `---POIDH-DESCRIPTION-START/END---` sentinels).
2. It queries POIDH's live bounty feed (`bounties.fetchAll`, same cursor-pagination
   approach as `scripts/scan-poidh-deadlines.py`), filters to bounties issued by the
   connected wallet whose title starts with "Unlock Protocol Clipping Bounty", and
   counts them.
3. Next version = that count + 1. v1 gets no suffix (matches Zaal's spec: "once
   completed a second one can be run with the same, just adding a v2 in the text, or
   v3 if it's the third"). v2+ gets " v{n}" appended to the title and a one-line round
   note injected into the description body.
4. The deadline and winner-cast date are computed fresh each time from the actual
   cast date (today + 7 days, today + 8 days) - not hardcoded, so this stays correct
   no matter which week it's actually run in. This avoids the exact mistake Kenny
   caught in R3 (a hardcoded day-of-week that drifted out of sync with the date).

## Relationship to R5

[R5](../r5/) is the separate, still-unlocked pitch to co-fund this with Unlock DAO
directly (via trigs/Kenny, referencing the July 8 fireside collectible instead of this
workshop). R6 is the version Zaal can cast solo, right now, from his own wallet,
pointed at a real recording that already exists. They can both run - R5 stays open as
a bigger future ask; R6 is the immediate, testable one.

## Files in this folder

- `description.md` - the recurring template + the versioning/date-substitution markers
  the tool fills in at cast time

## Post-cast checklist (fill in once cast)

- [ ] Record the bounty ID + tx hash here
- [ ] Update this README's "At a glance" with the real deadline date once cast
- [ ] After close: judge, cast winner, run `scripts/refresh-poidh-leaderboard.py`
  with the new bounty ID added
- [ ] When re-running as v2: no new folder, no new file - just click through the
  tool again, it derives everything live

## Related rounds

- [R1 - Hannah Ep 17 clip-up](../r1/)
- [R2 - Best 60s POIDH ad from Ep 19](../r2/)
- [R3 - Best ad for ZABAL Gamez](../r3/)
- [R4 - ZABAL Gamez open pot](../r4/)
- [R5 - Unlock Protocol clip bounty (Unlock-DAO-funded pitch, separate track)](../r5/)
