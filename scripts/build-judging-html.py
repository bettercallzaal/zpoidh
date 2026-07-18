#!/usr/bin/env python3
"""
Build per-round judging.html from judging.json using a reusable template.

    python3 scripts/build-judging-html.py --round 2
    python3 scripts/build-judging-html.py --round 3 --json-file rounds/r3/judging.json

Reads:
    rounds/rN/judging.json     - Full scaffold with submissions, rubric scores, verdicts

Writes:
    rounds/rN/judging.html     - Deterministic HTML scorecard for the round

The script is idempotent: re-run safely to regenerate from updated judging.json.
Pure stdlib: json, argparse, pathlib.
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def escape_html(s: str) -> str:
    """Escape HTML special characters."""
    if not s:
        return ""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def render_floor_checks_html(floor_checks: dict) -> str:
    """Render floor check chips as HTML."""
    chips = []
    for key, val in floor_checks.items():
        status_class = val if val in ["PASS", "FAIL", "UNKNOWN", "LIKELY"] else "UNKNOWN"
        chips.append(
            f'<span class="floor-chip {status_class}">{key.upper().replace("_", " ")} {status_class}</span>'
        )
    return "\n      ".join(chips)


def render_rubric_scores_html(rubric_score: dict) -> str:
    """Render rubric scores as HTML."""
    rubric_items = []
    for key, val in rubric_score.items():
        label = key.replace("_", " ").title()
        rubric_items.append(
            f'''<div class="rl">
        <div class="rl-cat">{label}</div>
        <div class="rl-body">{escape_html(val)}</div>
      </div>'''
        )
    return "\n      ".join(rubric_items)


def render_submission_card(sub: dict, idx: int) -> str:
    """Render a single submission card HTML."""
    claim_id = sub.get("claim_id", "")
    fc_handle = escape_html(sub.get("fc_handle", "unknown"))
    display_name = escape_html(sub.get("display_name", fc_handle))
    duration_sec = sub.get("duration_sec")
    verdict = escape_html(sub.get("claude_verdict", "UNKNOWN"))
    winner = sub.get("winner", False)

    # Media block
    media_mp4 = sub.get("media_mp4")
    media_thumb = sub.get("media_thumb")
    media_html = ""
    if media_mp4:
        media_html = f'''<div class="media-block">
      <video controls poster="{escape_html(media_thumb)}">
        <source src="{escape_html(media_mp4)}" type="video/mp4">
      </video>
      <div class="media-cap"><span>Claim {claim_id}</span><span>{duration_sec}s</span></div>
    </div>'''
    elif media_thumb:
        media_html = f'''<div class="media-block">
      <img src="{escape_html(media_thumb)}" alt="Claim {claim_id}" />
      <div class="media-cap"><span>Claim {claim_id}</span></div>
    </div>'''
    else:
        media_html = f'''<div class="media-block no-media">
      No media available
      <div class="media-cap"><span>Claim {claim_id}</span></div>
    </div>'''

    # Floor checks
    floor_checks = sub.get("floor_checks", {})
    floor_checks_html = render_floor_checks_html(floor_checks)

    # Rubric scores
    rubric_score = sub.get("rubric_score", {})
    rubric_html = render_rubric_scores_html(rubric_score) if rubric_score else ""

    # X text if available
    x_text = escape_html(sub.get("x_text", ""))
    x_text_html = f'<div class="x-text">{x_text}</div>' if x_text else ""

    # Winner badge
    winner_badge = " WINNER" if winner else ""

    # Claude notes
    claude_notes = sub.get("claude_notes", "")
    claude_notes_html = (
        f'''<div class="claude-notes">
      <span class="cn-label">Claude Notes</span>
      {escape_html(claude_notes)}
    </div>'''
        if claude_notes
        else ""
    )

    return f'''<div class="sub-card verdict-{verdict}" id="claim-{claim_id}">
    <div class="sub-head">
      <div class="avatar">{claim_id}</div>
      <div class="who">
        <div class="name">{display_name}{winner_badge}</div>
        <div class="handles">@{fc_handle}</div>
      </div>
      <span class="verdict-badge {verdict}">{verdict}</span>
    </div>
    <div class="sub-body">
      {media_html}
      <div class="analysis">
        <h3>Summary</h3>
        {x_text_html}
        <div class="floor-checks">
          {floor_checks_html}
        </div>
        <div class="rubric-list">
          {rubric_html}
        </div>
        {claude_notes_html}
      </div>
    </div>
  </div>

'''


def build_html(judging_data: dict, round_num: int) -> str:
    """Build complete HTML from judging.json data."""
    bounty_id = judging_data.get("bounty_id", "")
    bounty_title = escape_html(judging_data.get("bounty_title", ""))
    bounty_url = escape_html(judging_data.get("bounty_url", ""))

    # Floor rules
    floor_rules = judging_data.get("floor_rules", [])
    floor_list_html = "\n    ".join(
        [f"<li>{escape_html(r.get('label', ''))}</li>" for r in floor_rules]
    )

    # Rubric tiers
    rubric_tiers = judging_data.get("rubric_tiers", [])
    rubric_grid_html = "\n      ".join(
        [
            f'''<div class="rubric-pill">
      <div class="r-name">{escape_html(r.get('label', ''))}</div>
      <div class="r-ex">{escape_html(r.get('examples', ''))}</div>
    </div>'''
            for r in rubric_tiers
        ]
    )

    # Summary stats
    summary = judging_data.get("claude_summary", {})
    summary_html = f'''<div class="stat strong">
    <strong>{summary.get('floor_pass', 0)}</strong>
    Floor PASS
  </div>
  <div class="stat weak">
    <strong>{summary.get('floor_near', 0)}</strong>
    Floor NEAR
  </div>
  <div class="stat fail">
    <strong>{summary.get('floor_fail', 0)}</strong>
    Floor FAIL
  </div>'''

    # Submissions
    submissions = judging_data.get("submissions", [])
    submissions_html = "".join(
        [render_submission_card(sub, i) for i, sub in enumerate(submissions)]
    )

    # Meta info
    judging_generated_at = escape_html(judging_data.get("judging_generated_at", ""))
    deadline_pt = escape_html(judging_data.get("deadline_pt", ""))
    amount_eth = judging_data.get("amount_eth_at_judging", 0)

    hero_meta_html = ""
    if deadline_pt:
        hero_meta_html += f'<span><strong>Deadline (PT):</strong> {deadline_pt}</span>'
    if amount_eth:
        hero_meta_html += f'<span><strong>Prize:</strong> {amount_eth} ETH</span>'
    if judging_generated_at:
        hero_meta_html += f'<span><strong>Judged:</strong> {judging_generated_at}</span>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>POIDH Round {round_num} (Bounty {bounty_id}) - Submission Judging - BetterCallZaal</title>
  <meta name="description" content="Per-submission judging for POIDH bounty {bounty_id} '{bounty_title}'. Floor checks + rubric scores.">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="https://bettercallzaal.com/poidh-round{round_num}-judging.html">
  <meta property="og:title" content="POIDH Round {round_num} ({bounty_id}) - Submission Judging">
  <meta property="og:description" content="Floor rules + rubric scores for all submissions to bounty {bounty_id}. Floor PASS/FAIL on each; rubric on Distribution/Craft/Substance/Bonus.">
  <meta property="og:url" content="https://bettercallzaal.com/poidh-round{round_num}-judging.html">
  <meta property="og:image" content="https://bettercallzaal.com/assets/icon.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="/assets/icon.png">
  <style>
    *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
    :root {{
      --bg: #070709;
      --surface: #111115;
      --surface-2: #16161c;
      --orange: #ff6b35;
      --cyan: #00e5ff;
      --gold: #f5c842;
      --pink: #ff3d6e;
      --poidh-blue: #2a81d5;
      --zabal: #a78bfa;
      --green: #4ade80;
      --yellow: #facc15;
      --red: #f87171;
      --text: #e4e2dd;
      --text-muted: #8a8895;
      --text-dim: #4e4c57;
      --border: #1f1e26;
      --border-hover: #2f2d3a;
      --radius: 8px;
    }}
    html {{ scroll-behavior: smooth; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-weight: 400;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
    }}
    a {{ color: var(--cyan); text-decoration: none; }}
    .container {{ max-width: 1140px; margin: 0 auto; padding: 0 1.5rem; }}
    .topnav {{ padding: 1.5rem 0; border-bottom: 1px solid var(--border); }}
    .topnav-inner {{ display: flex; gap: 1.5rem; align-items: center; justify-content: space-between; flex-wrap: wrap; }}
    .topnav a.brand {{ font-weight: 800; font-size: 1.05rem; color: var(--text); }}
    .topnav nav {{ display: flex; gap: 1.25rem; flex-wrap: wrap; }}
    .topnav nav a {{ color: var(--text-muted); font-size: 0.9rem; }}
    .hero {{ padding: 3rem 0 2rem; border-bottom: 1px solid var(--border); }}
    .badge {{ display: inline-block; padding: 0.25rem 0.625rem; border-radius: 999px; font-size: 0.7rem; text-transform: uppercase; background: rgba(42,129,213,0.16); border: 1px solid rgba(42,129,213,0.4); color: var(--poidh-blue); }}
    .hero h1 {{ font-weight: 800; font-size: clamp(1.8rem, 4.5vw, 2.6rem); line-height: 1.1; margin: 0.75rem 0 0.5rem; color: var(--cyan); }}
    .hero p.sub {{ color: var(--text-muted); max-width: 720px; font-size: 1rem; }}
    .hero-meta {{ margin-top: 1rem; display: flex; gap: 1.25rem; flex-wrap: wrap; font-size: 0.85rem; color: var(--text-muted); }}
    .hero-meta strong {{ color: var(--text); font-weight: 500; }}
    .floor-card {{ margin: 2rem 0; padding: 1.5rem; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); }}
    .floor-card h2 {{ font-size: 1.05rem; margin-bottom: 0.5rem; color: var(--text); }}
    .floor-card .floor-note {{ color: var(--text-dim); font-size: 0.8rem; font-style: italic; }}
    .floor-card ol {{ margin: 0.75rem 0 1rem 1.25rem; }}
    .floor-card ol li {{ margin: 0.25rem 0; }}
    .rubric-grid {{ display: grid; gap: 0.75rem; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); margin-top: 0.75rem; }}
    .rubric-pill {{ padding: 0.65rem 0.85rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--surface-2); }}
    .rubric-pill .r-name {{ font-weight: 700; color: var(--gold); font-size: 0.85rem; }}
    .rubric-pill .r-ex {{ font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem; }}
    .summary {{ margin: 1.5rem 0 2.5rem; padding: 1.25rem; background: var(--surface-2); border: 1px solid var(--border-hover); border-radius: var(--radius); display: flex; flex-wrap: wrap; gap: 1rem 2rem; align-items: center; }}
    .summary .stat {{ font-size: 0.85rem; }}
    .summary .stat strong {{ display: block; font-size: 1.4rem; font-weight: 700; color: var(--cyan); }}
    .summary .stat.fail strong {{ color: var(--red); }}
    .summary .stat.strong strong {{ color: var(--green); }}
    .summary .stat.weak strong {{ color: var(--yellow); }}
    section.submissions {{ padding: 0 0 4rem; }}
    .sub-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); margin-bottom: 1.5rem; overflow: hidden; }}
    .sub-card.verdict-STRONG_CANDIDATE {{ border-left: 4px solid var(--green); }}
    .sub-card.verdict-FLOOR_PASS_WEAK_RUBRIC {{ border-left: 4px solid var(--yellow); }}
    .sub-card.verdict-BORDERLINE_DURATION {{ border-left: 4px solid var(--yellow); }}
    .sub-card.verdict-FLOOR_FAIL {{ border-left: 4px solid var(--red); opacity: 0.78; }}
    .sub-card.verdict-FLOOR_FAIL_DURATION {{ border-left: 4px solid var(--red); opacity: 0.85; }}
    .sub-head {{ display: flex; gap: 1rem; padding: 1.25rem 1.5rem; align-items: center; flex-wrap: wrap; border-bottom: 1px solid var(--border); }}
    .sub-head .avatar {{ width: 44px; height: 44px; border-radius: 50%; background: var(--surface-2); flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; color: var(--text-dim); border: 1px solid var(--border-hover); }}
    .sub-head .who {{ flex: 1; min-width: 200px; }}
    .sub-head .who .name {{ font-weight: 700; font-size: 1rem; color: var(--text); }}
    .sub-head .who .handles {{ font-size: 0.78rem; color: var(--text-muted); word-break: break-all; }}
    .sub-head .verdict-badge {{ padding: 0.4rem 0.75rem; border-radius: 999px; font-size: 0.7rem; text-transform: uppercase; font-weight: 500; border: 1px solid var(--border-hover); }}
    .verdict-badge.STRONG_CANDIDATE {{ background: rgba(74,222,128,0.12); color: var(--green); border-color: rgba(74,222,128,0.4); }}
    .verdict-badge.FLOOR_PASS_WEAK_RUBRIC {{ background: rgba(250,204,21,0.12); color: var(--yellow); border-color: rgba(250,204,21,0.4); }}
    .verdict-badge.BORDERLINE_DURATION {{ background: rgba(250,204,21,0.12); color: var(--yellow); border-color: rgba(250,204,21,0.4); }}
    .verdict-badge.FLOOR_FAIL {{ background: rgba(248,113,113,0.12); color: var(--red); border-color: rgba(248,113,113,0.4); }}
    .verdict-badge.FLOOR_FAIL_DURATION {{ background: rgba(248,113,113,0.12); color: var(--red); border-color: rgba(248,113,113,0.4); }}
    .sub-body {{ padding: 1.25rem 1.5rem; display: grid; gap: 1.5rem; grid-template-columns: minmax(0, 1fr); }}
    @media (min-width: 800px) {{ .sub-body {{ grid-template-columns: 260px 1fr; }} }}
    .media-block {{ background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; align-self: start; }}
    .media-block video, .media-block img {{ width: 100%; display: block; aspect-ratio: 16/9; object-fit: cover; background: #000; }}
    .media-block.no-media {{ padding: 2rem 1rem; text-align: center; color: var(--text-dim); font-size: 0.78rem; }}
    .media-block .media-cap {{ padding: 0.5rem 0.75rem; font-size: 0.72rem; color: var(--text-muted); display: flex; justify-content: space-between; gap: 0.5rem; flex-wrap: wrap; }}
    .analysis h3 {{ font-size: 0.85rem; color: var(--gold); text-transform: uppercase; margin: 0 0 0.5rem; }}
    .analysis .x-text {{ padding: 0.85rem 1rem; background: var(--surface-2); border-left: 3px solid var(--poidh-blue); border-radius: 4px; font-size: 0.9rem; color: var(--text); margin-bottom: 1rem; font-style: italic; }}
    .floor-checks {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }}
    .floor-chip {{ padding: 0.35rem 0.7rem; border-radius: 999px; font-size: 0.7rem; border: 1px solid var(--border-hover); }}
    .floor-chip.PASS {{ background: rgba(74,222,128,0.1); color: var(--green); border-color: rgba(74,222,128,0.3); }}
    .floor-chip.FAIL {{ background: rgba(248,113,113,0.1); color: var(--red); border-color: rgba(248,113,113,0.3); }}
    .floor-chip.UNKNOWN {{ background: rgba(167,139,250,0.1); color: var(--zabal); border-color: rgba(167,139,250,0.3); }}
    .floor-chip.LIKELY {{ background: rgba(245,200,66,0.1); color: var(--gold); border-color: rgba(245,200,66,0.3); }}
    .rubric-list {{ display: grid; gap: 0.6rem; }}
    .rubric-list .rl {{ padding: 0.65rem 0.85rem; background: var(--surface-2); border-radius: 4px; border: 1px solid var(--border); }}
    .rubric-list .rl .rl-cat {{ font-weight: 700; color: var(--cyan); font-size: 0.78rem; text-transform: uppercase; }}
    .rubric-list .rl .rl-body {{ font-size: 0.85rem; color: var(--text); margin-top: 0.2rem; }}
    .claude-notes {{ margin-top: 1rem; padding: 0.85rem 1rem; background: rgba(167,139,250,0.06); border-left: 3px solid var(--zabal); border-radius: 4px; font-size: 0.85rem; color: var(--text); }}
    .claude-notes .cn-label {{ font-size: 0.7rem; text-transform: uppercase; color: var(--zabal); display: block; margin-bottom: 0.25rem; }}
    footer {{ padding: 2rem 0; border-top: 1px solid var(--border); text-align: center; color: var(--text-muted); font-size: 0.85rem; }}
  </style>
</head>
<body>
  <div class="topnav">
    <div class="container topnav-inner">
      <a class="brand" href="/">BetterCallZaal</a>
      <nav>
        <a href="/nexus.html">Nexus</a>
        <a href="/poidh.html">POIDH Hub</a>
        <a href="{bounty_url}" target="_blank" rel="noopener">Bounty {bounty_id}</a>
      </nav>
    </div>
  </div>

  <header class="hero">
    <div class="container">
      <span class="badge">Round {round_num} - Judging</span>
      <h1>Bounty {bounty_id} Judging</h1>
      <p class="sub">Floor checks + rubric scores for every submission. Auto-verified what could be auto-verified; flagged the rest for manual playback.</p>
      <div class="hero-meta">
        {hero_meta_html}
      </div>
    </div>
  </header>

  <div class="container">
    <div class="floor-card">
      <h2>The bar (floor rules)</h2>
      <p class="floor-note">Miss any of these and you are not in the running. Auto-checks done on URL + tags; duration + edit quality need manual playback.</p>
      <ol>
        {floor_list_html}
      </ol>
      <h2 style="margin-top:1rem">Rubric (more boxes ticked = stronger judging weight)</h2>
      <div class="rubric-grid">
        {rubric_grid_html}
      </div>
    </div>

    <div class="summary">
      {summary_html}
    </div>
  </div>

  <section class="submissions">
    <div class="container">
      {submissions_html}
    </div>
  </section>

  <footer>
    <div class="container">
      Generated by Claude from rounds/r{round_num}/judging.json. Zaal confirms final verdict.
    </div>
  </footer>
</body>
</html>
"""

    return html


def main() -> int:
    p = argparse.ArgumentParser(
        description="Build judging.html from judging.json using a template"
    )
    p.add_argument("--round", type=int, required=True, help="Round number")
    p.add_argument(
        "--json-file",
        type=Path,
        default=None,
        help="Path to judging.json (default: rounds/rN/judging.json)",
    )

    args = p.parse_args()

    # Determine JSON path
    if args.json_file:
        json_path = args.json_file
    else:
        json_path = REPO_ROOT / f"rounds/r{args.round}/judging.json"

    if not json_path.exists():
        print(f"ERROR: {json_path} not found")
        return 1

    # Load judging.json
    try:
        with open(json_path) as f:
            judging_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse {json_path}: {e}")
        return 1
    except Exception as e:
        print(f"ERROR: Failed to read {json_path}: {e}")
        return 1

    # Build HTML
    try:
        html_content = build_html(judging_data, args.round)
    except Exception as e:
        print(f"ERROR: Failed to build HTML: {e}")
        return 1

    # Write HTML
    html_path = REPO_ROOT / f"rounds/r{args.round}/judging.html"
    try:
        html_path.parent.mkdir(parents=True, exist_ok=True)
        with open(html_path, "w") as f:
            f.write(html_content)
        print(f"Wrote {html_path.relative_to(REPO_ROOT)}: {len(html_content)} bytes")
        return 0
    except Exception as e:
        print(f"ERROR: Failed to write {html_path}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
