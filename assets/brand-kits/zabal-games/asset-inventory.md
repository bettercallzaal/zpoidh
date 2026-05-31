# ZABAL Gamez Asset Inventory

Where each asset belongs in the unfurl + design pipeline.

## Social card unfurl matrix

| Platform | Meta tag | File |
|---|---|---|
| Twitter / X | `<meta name="twitter:image">` | `logo.png` |
| Open Graph (FB, LinkedIn, iMessage, Slack, Discord) | `<meta property="og:image">` | `logo.png` |
| Telegram | `<meta name="telegram:image">` | `logo.png` |
| Farcaster Mini App | `imageUrl` + `splashImageUrl` | `logo.png` |
| Browser tab | `<link rel="icon">` | `icon.png` (NOT logo) |

## Where each file goes

| File | Use for | Don't use for |
|---|---|---|
| `logo.png` (1024x1024, 1.2 MB) | OG image, Twitter card, Telegram preview, Mini App splash, social posts, t-shirts, stream overlays, hero graphics at rest | favicon (use icon.png); tiny avatar contexts where INSERT COIN is unreadable |
| `logo-gamez.png` (1.0 MB) | Wider variant emphasizing GAMEZ wordmark | same exclusions as logo.png |
| `logo-wordmark.svg` | Lower-third overlays, dark-bg tight spaces needing vector scale | hero contexts (use logo.png) |
| `icon.png` (1024x1024, 263 KB) | Favicon, browser tab, tiny avatars, Slack channel icon, app launcher | hero contexts (use logo.png) |
| `og-card.svg` | SVG-aware unfurl clients | bulk social (use embed-card-gamez.png) |
| `embed-card.svg` (1200x630) | Vector embed card | clients that reject SVG |
| `embed-card-gamez.png` (1200x630, 670 KB) | Bulk 1200x630 raster social unfurl | the OG hero (that's logo.png) |
| `zabal-gamez-promo.mp3` (50s, 1.3 MB, 48kHz stereo 212 kbps) | Full promo audio - use as intro / outro / full ambient bed under your edit | replacement for source-episode dialog |
| `palette.svg` | Designer reference for site-UI colors | hero collateral (use palette-arcade.svg) |
| `palette-arcade.svg` | Designer reference for arcade-logo collateral | site UI work (use palette.svg) |

## When something doesn't fit

If the arcade hero looks weird at small size (tiny avatar contexts where the "INSERT COIN" caption is unreadable), drop down to `icon.png` (clean Z). Logo is for at-rest hero use; icon is for small-context.

## Pending / TODO

| File | Why we need it | Blocker |
|---|---|---|
| `b-roll-channel-walkthrough.mp4` | 10-15s screen capture of /zabal Farcaster channel | Self-record; Zaal or Iman |
| `b-roll-magnetiq-portal.mp4` | 10-15s screen capture of Magnetiq portal | Coordinate with Tyler Stambaugh |
| `b-roll-workshop-1.mp4` | 10-15s screen capture of a recorded workshop | After first workshop drops on Lu.ma |
| `prize-card-eth.png` | "0.0125 ETH wins" social card 1080x1080 | Design pass |
| `prize-card-tracks.png` | "Artist / Builder / Creator - pick your lane" 1080x1080 | Design pass |
| `og-card.png` | 1200x630 raster of OG card for clients that don't unfurl SVG | TODO W11 in ZAODEVZ/zabalgames repo (5-min screenshot job) |
