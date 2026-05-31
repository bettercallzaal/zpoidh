# ZABAL Gamez Brand Kit (canonical)

Mirror of the canonical brand kit from `github.com/ZAODEVZ/zabalgames` (`docs/brand-kit-2026-05-28.md` + `docs/brand-context.md`), bundled here so editors can lift assets for BCZ POIDH bounty submissions, mentor outreach, social posts, sponsor pitches, and anything else.

Source of truth: https://github.com/ZAODEVZ/zabalgames (docs/ + assets/). If this kit and the source disagree, the source wins. Re-sync target: weekly during the campaign.

Maintainer: Zaal / BetterCallZaal. Last sync: 2026-05-31. Logo reveal: 2026-05-28. CC-BY 4.0.

---

## What ZABAL Gamez is (one paragraph)

ZABAL Gamez is The ZAO's 3-month Build-A-Thon. June workshops, July open build-a-thon, August Finals with ZAO mentors embedded as teammates. Three tracks (artist, builder, creator). Free to join. Anyone welcome. The 100+ member ZAO community is the real audience.

- Landing: https://zabalgamez.com
- Lead signup: https://zabalgamez.com/lead.html
- Farcaster channel: https://farcaster.xyz/~/channel/zabal
- Repo + every document: https://github.com/ZAODEVZ/zabalgames
- Lu.ma calendar: https://luma.com/ZABALgames

---

## Visual direction

**Arcade-meets-builder.** Retro arcade cabinet hero + modern minimalist site chrome. The logo carries the retro energy. The chrome stays sleek. The pairing reads as "playful builder space," not "novelty arcade site."

Logo composition (per `brand-kit-2026-05-28.md`):
- Chunky 3D letter forms (yellow "ZABAL" / red "Z" / cyan "GAMES")
- "INSERT COIN" pixel font caption
- Rainbow pixel-art border (tetris-style multi-color blocks)
- Joystick + button graphics on either side
- CRT scan-line dark navy background

---

## Site palette (the dark theme - use for UI work)

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#070709` | Page background |
| `--surface` | `#111115` | Cards, modals |
| `--surface-2` | `#16161c` | Hovered cards, nested surfaces |
| `--text` | `#e4e2dd` | Primary text |
| `--text-muted` | `#8a8895` | Secondary text |
| `--text-dim` | `#4e4c57` | Tertiary text, captions |
| `--border` | `#1f1e26` | Card borders |
| `--border-hover` | `#2f2d3a` | Card borders on hover |
| `--orange` | `#ff6b35` | Primary accent (CTAs, "Build" path) |
| `--cyan` | `#00e5ff` | Secondary accent, links, "Watch" path |
| `--gold` | `#f5c842` | Tertiary accent, "Learn" path, eyebrows |
| `--pink` | `#ff3d6e` | Spot accent, fix-state, decision callout |
| `--zabal` | `#a78bfa` | ZABAL token, deep accent, workshop accent |

See `palette.svg` for the swatch card.

## Arcade palette (the logo - use for collateral that matches the hero)

For cabinet skins, stream overlays, merch, motion graphics that should match the hero exactly:

| Token | Hex | What it is in the logo |
|---|---|---|
| `arcade-red` | `#E53935` | The "Z" + the right button |
| `arcade-amber` | `#FFA000` | ZABAL letter mid-tone |
| `arcade-yellow` | `#FFC107` | ZABAL letter highlight |
| `arcade-cyan` | `#00BCD4` | GAMES mid-tone |
| `arcade-cyan-bright` | `#00E5FF` | GAMES highlight (matches `--cyan`) |
| `arcade-magenta` | `#E91E63` | GAMES outline + pixel-border accent |
| `arcade-green` | `#66BB6A` | Joystick ring + pixel-border accent |
| `arcade-navy` | `#1A1B5E` | Background base |
| `pixel-white` | `#FAFAFA` | "INSERT COIN" + sparkles |

See `palette-arcade.svg` for the swatch card.

---

## Typography

### Site (web stack via Google Fonts)

- **Headings:** Syne 700-800
- **Body:** Outfit 300-600
- **Numbers, code, mono:** JetBrains Mono 400-500

### System fallback

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Asset design (optional layer for arcade-feel collateral)

- **Pixel display font:** Press Start 2P or VT323 - sparingly, for "INSERT COIN" treatment only
- **Chunky 3D titles:** Bungee or Russo One for ZABAL/GAMES feel
- Body still Outfit for legibility

Do NOT use a pixel font in body copy. It reads ironic + hurts legibility. Save it for hero-graphic treatments only.

---

## Voice

- Direct, warm, builder-energy
- "We learn it together" not "trust us"
- Drop articles when terse helps ("Sign up. Insert coin." NOT "You should sign up by inserting a coin.")
- "Insert coin" is the spirit-totem callback - use it sparingly + intentionally (one moment per surface max)
- No emojis. No em dashes. (Global ZAO rule.)
- "Build for a real community, not a weekend you forget."
- "Build event, not a video-game contest."
- Use "100+ members" never specific count.

See `phrases.md` for the approved + banned phrase lists.

---

## Files in this folder

| File | What |
|---|---|
| `README.md` | This file |
| `phrases.md` | Approved phrases + banned phrases + brand glossary (correct spellings) |
| `asset-inventory.md` | Where each asset goes (OG, Twitter, Telegram, Mini App, etc) |
| `palette.svg` | Site palette swatch card |
| `palette-arcade.svg` | Arcade-logo palette swatch card |
| `logo.png` | Arcade hero logo, 1024x1024, ~1.2 MB. OG image, Mini App splash, t-shirts, stream overlays |
| `logo-gamez.png` | Wider variant with the "GAMEZ" emphasis, ~1.0 MB |
| `logo-wordmark.svg` | Clean SVG wordmark for tight spaces (light/dark adaptive) |
| `icon.png` | Clean Z favicon mark, 1024x1024 (browser scales) |
| `og-card.svg` | SVG OG card fallback (text + minimal graphics) |
| `embed-card.svg` | 1200x630 SVG embed card (Farcaster + X + general) |
| `embed-card-gamez.png` | 1200x630 raster embed card |
| `zabal-gamez-promo.mp3` | 50-second ZABAL Gamez promo audio (1.3 MB, 48kHz stereo, 212 kbps) - drop as intro / outro / full ambient bed under your edit |

Pending (TODO):
- `b-roll-channel-walkthrough.mp4` - 10-15s screen capture of /zabal Farcaster channel
- `b-roll-magnetiq-portal.mp4` - 10-15s screen capture of Magnetiq portal (coordinate with Tyler)
- `b-roll-workshop-1.mp4` - 10-15s screen capture of a recorded workshop (after first workshop drops)
- `prize-card-eth.png` - "0.0125 ETH wins" social card
- `prize-card-tracks.png` - "Artist / Builder / Creator - pick your lane" social card
- `og-card.png` - 1200x630 raster of the OG card for clients that don't unfurl SVG

---

## Audio rule (for BCZ POIDH bounty submissions)

If your ad has audio, choose ONE of:

1. The `zabal-gamez-promo.mp3` in this folder (sanctioned brand audio - drop as intro/outro tag or loop under your edit at low volume)
2. Original source-episode audio (always fine)
3. One clear instrumental track that does not compete with spoken dialog

Random library music or melodic pads over dialog = automatic floor fail on any BCZ POIDH bounty.

---

## License

CC-BY 4.0. Remix, mash up, recolor, re-time, re-voice freely. Attribution: keep "ZABAL Gamez" or "zabalgamez.com" visible in the final piece.

If you build something with this kit, post it in `/zabal` on Farcaster + tag `@bettercallzaal` so we can boost it.

---

## Where this kit's canonical copy lives

- `github.com/ZAODEVZ/zabalgames/docs/brand-kit-2026-05-28.md` - the canonical Season 1 brand spec
- `github.com/ZAODEVZ/zabalgames/docs/brand-context.md` - the 7-brand ZAO ecosystem spine
- `github.com/ZAODEVZ/zabalgames/docs/logo-brief-2026-05-26.md` - logo design brief
- `github.com/ZAODEVZ/zabalgames/docs/media-kit-2026-05-26.md` - press / media pull
- `github.com/ZAODEVZ/zabalgames/docs/magnetiq-mementos-zao-brands-2026-05-28.md` - Magnetiq mementos catalog

This BCZ folder is a working mirror. Update by re-syncing the docs + re-copying the assets when the canonical changes.
