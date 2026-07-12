#!/usr/bin/env python3
"""
Stage 2: Render judging.json to a shareable HTML page.

Transforms judging.json scaffold into a formatted HTML scorecard for review.
Reuses the stage-1 judging data (floor checks, rubric scores) and renders to
the same structure as rounds/r2/judging.html.

    python3 scripts/render-judging-html.py --round 3 [--output path/to/output.html]

Outputs:
    rounds/r{N}/judging.html  - rendered HTML scorecard (or custom path via --output)

This stage is human-gated: it renders existing judging data, does not modify it.
The rubric scores come FROM stage-1 or manual filling, not FROM this renderer.
"""

import argparse
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_judging_json(round_num: int) -> dict | None:
    """Load judging.json for a given round."""
    judging_path = REPO_ROOT / f"rounds/r{round_num}/judging.json"
    if not judging_path.exists():
        print(f"ERROR: {judging_path} not found")
        return None

    try:
        with open(judging_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading judging.json: {e}")
        return None


def render_html(judging: dict, round_num: int) -> str:
    """Render judging.json to HTML."""

    bounty_id = judging.get("bounty_id", "?")
    bounty_title = judging.get("bounty_title", "POIDH Bounty")
    bounty_url = judging.get("bounty_url", "#")
    submissions = judging.get("submissions", [])
    floor_rules = judging.get("floor_rules", [])
    rubric_tiers = judging.get("rubric_tiers", [])
    deadline_pt = judging.get("deadline_pt", "TBD")
    amount_eth = judging.get("amount_eth_at_judging", 0)
    judging_note = judging.get("judging_note", "")
    summary = judging.get("claude_summary", {})

    # Build floor rules HTML
    floor_rules_html = ""
    for rule in floor_rules:
        floor_rules_html += f"    <li><strong>{rule.get('id', '').upper()}</strong> – {rule.get('label', '')}</li>\n"

    # Build rubric tiers pills
    rubric_pills_html = ""
    for tier in rubric_tiers:
        rubric_pills_html += f"""    <div class="rubric-pill">
      <div class="r-name">{tier.get('label', '')}</div>
      <div class="r-ex">{tier.get('examples', '')}</div>
    </div>
"""

    # Build submissions
    submissions_html = ""
    for sub in submissions:
        claim_id = sub.get("claim_id", "?")
        fc_handle = sub.get("fc_handle") or "user"
        wallet = sub.get("wallet", "")
        display_name = sub.get("display_name") or fc_handle
        x_url = sub.get("x_url", "")
        fc_url = sub.get("fc_url", "")
        title = sub.get("title", "Untitled")
        duration_sec = sub.get("duration_sec")
        floor_checks = sub.get("floor_checks", {})
        rubric_score = sub.get("rubric_score", {})
        winner = sub.get("winner", False)
        accepted = sub.get("accepted", False)

        # Build floor chips
        floor_chips_html = ""
        for check_id, check_val in floor_checks.items():
            if check_val and check_val != "UNKNOWN":
                chip_class = "PASS" if "PASS" in check_val else "FAIL" if "FAIL" in check_val else "UNKNOWN"
                floor_chips_html += f'    <span class="floor-chip {chip_class}">{check_id.upper()}: {check_val}</span>\n'

        # Build rubric scores
        rubric_html = ""
        for tier_id, tier_label in [
            ("distribution", "Distribution"),
            ("craft", "Craft"),
            ("substance", "Substance"),
            ("bonus", "Bonus"),
        ]:
            score_text = rubric_score.get(tier_id, "")
            if score_text:
                rubric_html += f"""    <div class="rl">
      <div class="rl-cat">{tier_label}</div>
      <div class="rl-body">{score_text}</div>
    </div>
"""

        # Meta info
        x_link = f'<a href="{x_url}" target="_blank">X Post</a>' if x_url else "No X URL"
        fc_link = f'<a href="{fc_url}" target="_blank">Farcaster</a>' if fc_url else ""

        # Winner badge
        winner_badge = ""
        if winner:
            winner_badge = '<span class="verdict-badge" style="background: rgba(74,222,128,0.12); color: #4ade80; border-color: rgba(74,222,128,0.4);">WINNER</span>'
        elif accepted:
            winner_badge = '<span class="verdict-badge" style="background: rgba(250,204,21,0.12); color: #facc15; border-color: rgba(250,204,21,0.4);">ACCEPTED</span>'

        # Duration display
        duration_info = f"{duration_sec}s" if duration_sec else "No duration data"

        submissions_html += f"""  <div class="sub-card">
    <div class="sub-head">
      <div class="avatar">{fc_handle[:2].upper()}</div>
      <div class="who">
        <div class="name">{display_name}</div>
        <div class="handles">@{fc_handle} · {wallet[:12]}...</div>
      </div>
      {winner_badge}
    </div>
    <div class="sub-body">
      <div class="analysis">
        <h3>Submission</h3>
        <div class="x-text">{title}</div>
        <div class="meta-row">
          <span><strong>Claim:</strong> {claim_id}</span>
          <span><strong>Duration:</strong> {duration_info}</span>
        </div>
        <div class="meta-row">
          <span>{x_link}</span>
          {fc_link}
        </div>
        <h3 style="margin-top: 1rem;">Floor Checks</h3>
        <div class="floor-checks">
{floor_chips_html}        </div>
        <h3>Rubric Scores</h3>
        <div class="rubric-list">
{rubric_html}        </div>
      </div>
    </div>
  </div>

"""

    # Summary stats
    total = len(submissions)
    with_scores = sum(1 for s in submissions if any(s.get("rubric_score", {}).values()))
    winners = sum(1 for s in submissions if s.get("winner"))

    summary_html = f"""  <div class="summary">
    <div class="stat">
      <strong>{total}</strong>
      Total Submissions
    </div>
    <div class="stat">
      <strong>{with_scores}</strong>
      Scored
    </div>
    <div class="stat strong">
      <strong>{winners}</strong>
      Winner(s)
    </div>
  </div>
"""

    # Final HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>POIDH Round {round_num} (Bounty {bounty_id}) - Submission Judging - BetterCallZaal</title>
  <meta name="description" content="Per-submission judging for POIDH bounty {bounty_id} '{bounty_title}'. Floor checks + rubric scores + verdict.">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="https://bettercallzaal.com/poidh-round{round_num}-judging.html">
  <meta property="og:title" content="POIDH Round {round_num} ({bounty_id}) - Submission Judging">
  <meta property="og:description" content="Floor rules + rubric scores for submissions to bounty {bounty_id}. Floor PASS/FAIL on each; rubric on Distribution/Craft/Substance/Bonus.">
  <meta property="og:url" content="https://bettercallzaal.com/poidh-round{round_num}-judging.html">
  <meta property="og:image" content="https://bettercallzaal.com/assets/icon.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="/assets/icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
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
      --gradient-main: linear-gradient(135deg, #ff6b35, #ff3d6e, #00e5ff);
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
      font-family: 'Outfit', sans-serif;
      font-weight: 400;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
    }}
    body::before {{
      content: '';
      position: fixed; inset: 0; pointer-events: none;
      background:
        radial-gradient(ellipse 800px 600px at 15% -10%, rgba(167,139,250,0.14), transparent 60%),
        radial-gradient(ellipse 700px 500px at 90% 10%, rgba(0,229,255,0.10), transparent 60%),
        radial-gradient(ellipse 600px 400px at 50% 100%, rgba(255,107,53,0.08), transparent 60%);
      z-index: -1;
    }}
    a {{ color: var(--cyan); text-decoration: none; transition: color 0.15s; }}
    a:hover {{ color: var(--orange); }}
    .container {{ max-width: 1140px; margin: 0 auto; padding: 0 1.5rem; }}

    .topnav {{ padding: 1.5rem 0; border-bottom: 1px solid var(--border); }}
    .topnav-inner {{ display: flex; gap: 1.5rem; align-items: center; justify-content: space-between; flex-wrap: wrap; }}
    .topnav a.brand {{ font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.05rem; color: var(--text); letter-spacing: -0.01em; }}

    .hero {{ padding: 3rem 0 2rem; border-bottom: 1px solid var(--border); }}
    .hero h1 {{
      font-family: 'Syne', sans-serif; font-weight: 800;
      font-size: clamp(1.8rem, 4.5vw, 2.6rem); line-height: 1.1; margin: 0.75rem 0 0.5rem;
      background: var(--gradient-main); -webkit-background-clip: text; background-clip: text; color: transparent;
    }}
    .hero p.sub {{ color: var(--text-muted); max-width: 720px; font-size: 1rem; }}
    .hero-meta {{ margin-top: 1rem; display: flex; gap: 1.25rem; flex-wrap: wrap; font-size: 0.85rem; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; }}

    .floor-card {{
      margin: 2rem 0; padding: 1.5rem;
      background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
    }}
    .floor-card h2 {{ font-family: 'Syne', sans-serif; font-size: 1.05rem; margin-bottom: 0.5rem; color: var(--text); }}
    .floor-card ol {{ margin: 0.75rem 0 1rem 1.25rem; }}
    .floor-card ol li {{ margin: 0.25rem 0; }}
    .rubric-grid {{ display: grid; gap: 0.75rem; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); margin-top: 0.75rem; }}
    .rubric-pill {{
      padding: 0.65rem 0.85rem; border: 1px solid var(--border); border-radius: var(--radius);
      background: var(--surface-2);
    }}
    .rubric-pill .r-name {{ font-family: 'Syne', sans-serif; font-weight: 700; color: var(--gold); font-size: 0.85rem; letter-spacing: 0.05em; }}
    .rubric-pill .r-ex {{ font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem; }}

    .summary {{ margin: 1.5rem 0 2.5rem; padding: 1.25rem; background: var(--surface-2); border: 1px solid var(--border-hover); border-radius: var(--radius); display: flex; flex-wrap: wrap; gap: 1rem 2rem; align-items: center; }}
    .summary .stat {{ font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }}
    .summary .stat strong {{ display: block; font-size: 1.4rem; font-family: 'Syne', sans-serif; font-weight: 700; color: var(--cyan); }}
    .summary .stat.strong strong {{ color: var(--green); }}

    section.submissions {{ padding: 0 0 4rem; }}
    .sub-card {{
      background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
      margin-bottom: 1.5rem; overflow: hidden;
    }}
    .sub-head {{
      display: flex; gap: 1rem; padding: 1.25rem 1.5rem; align-items: center; flex-wrap: wrap; border-bottom: 1px solid var(--border);
    }}
    .sub-head .avatar {{
      width: 44px; height: 44px; border-radius: 50%; background: var(--surface-2); flex-shrink: 0;
      display: flex; align-items: center; justify-content: center; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--text-dim);
      border: 1px solid var(--border-hover); overflow: hidden;
    }}
    .sub-head .who {{ flex: 1; min-width: 200px; }}
    .sub-head .who .name {{ font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1rem; color: var(--text); }}
    .sub-head .who .handles {{ font-size: 0.78rem; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; word-break: break-all; }}
    .sub-head .verdict-badge {{
      padding: 0.4rem 0.75rem; border-radius: 999px; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 500;
      border: 1px solid var(--border-hover);
    }}

    .sub-body {{ padding: 1.25rem 1.5rem; display: grid; gap: 1.5rem; }}
    .analysis h3 {{ font-family: 'Syne', sans-serif; font-size: 0.85rem; color: var(--gold); text-transform: uppercase; letter-spacing: 0.1em; margin: 1rem 0 0.5rem; }}
    .analysis h3:first-child {{ margin-top: 0; }}
    .x-text {{
      padding: 0.85rem 1rem; background: var(--surface-2); border-left: 3px solid var(--poidh-blue); border-radius: 4px;
      font-size: 0.9rem; color: var(--text); margin-bottom: 1rem;
    }}
    .meta-row {{ font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 1rem; display: flex; flex-wrap: wrap; gap: 0.75rem 1.25rem; }}
    .meta-row span strong {{ color: var(--text); font-weight: 500; }}

    .floor-checks {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }}
    .floor-chip {{
      padding: 0.35rem 0.7rem; border-radius: 999px; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; letter-spacing: 0.05em;
      border: 1px solid var(--border-hover);
    }}
    .floor-chip.PASS {{ background: rgba(74,222,128,0.1); color: var(--green); border-color: rgba(74,222,128,0.3); }}
    .floor-chip.FAIL {{ background: rgba(248,113,113,0.1); color: var(--red); border-color: rgba(248,113,113,0.3); }}
    .floor-chip.UNKNOWN {{ background: rgba(167,139,250,0.1); color: var(--zabal); border-color: rgba(167,139,250,0.3); }}

    .rubric-list {{ display: grid; gap: 0.6rem; }}
    .rubric-list .rl {{
      padding: 0.65rem 0.85rem; background: var(--surface-2); border-radius: 4px; border: 1px solid var(--border);
    }}
    .rubric-list .rl .rl-cat {{ font-family: 'Syne', sans-serif; font-weight: 700; color: var(--cyan); font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; }}
    .rubric-list .rl .rl-body {{ font-size: 0.85rem; color: var(--text); margin-top: 0.2rem; }}

    .judging-note {{
      margin: 2rem 0; padding: 1rem 1.25rem;
      background: rgba(167,139,250,0.06); border-left: 3px solid var(--zabal); border-radius: var(--radius);
      font-size: 0.85rem; color: var(--text);
    }}
  </style>
</head>
<body>
  <header class="topnav">
    <div class="container">
      <div class="topnav-inner">
        <a href="/" class="brand">BetterCallZaal</a>
        <nav>
          <a href="https://poidh.xyz">POIDH</a>
          <a href="https://bettercallzaal.com/poidh.html">POIDH Hub</a>
        </nav>
      </div>
    </div>
  </header>

  <main class="container">
    <section class="hero">
      <div style="display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap; margin-bottom: 1rem;">
        <span class="badge" style="background: rgba(42,129,213,0.16); border: 1px solid rgba(42,129,213,0.4); color: var(--poidh-blue); font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; padding: 0.25rem 0.625rem; border-radius: 999px;">
          ROUND {round_num}
        </span>
      </div>
      <h1>POIDH Bounty {bounty_id}</h1>
      <p class="sub">{bounty_title}</p>
      <div class="hero-meta">
        <span><strong>Bounty:</strong> <a href="{bounty_url}" target="_blank">{bounty_url}</a></span>
        <span><strong>Deadline:</strong> {deadline_pt}</span>
        <span><strong>Prize:</strong> {amount_eth} ETH</span>
      </div>
    </section>

    <section class="floor-card">
      <h2>Floor Rules</h2>
      <ol>
{floor_rules_html}      </ol>
      <h3 style="margin-top: 1rem; color: var(--text); font-family: 'Syne', sans-serif; font-size: 0.95rem;">Rubric Tiers</h3>
      <div class="rubric-grid">
{rubric_pills_html}      </div>
    </section>

{summary_html}

    {('<div class="judging-note">' + judging_note + '</div>') if judging_note else ''}

    <section class="submissions">
      <h2 style="font-family: 'Syne', sans-serif; font-size: 1.3rem; margin-bottom: 1.5rem; color: var(--text);">Submissions ({total})</h2>
{submissions_html}    </section>
  </main>
</body>
</html>
"""

    return html


def main() -> int:
    p = argparse.ArgumentParser(
        description="Stage 2: Render judging.json to shareable HTML scorecard"
    )
    p.add_argument("--round", type=int, required=True, help="Round number")
    p.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output HTML path (default: rounds/r{N}/judging.html)",
    )

    args = p.parse_args()

    # Load judging.json
    print(f"Loading judging data for round {args.round}...")
    judging = load_judging_json(args.round)
    if not judging:
        return 1

    # Render HTML
    print("Rendering HTML...")
    html = render_html(judging, args.round)

    # Determine output path
    output_path = args.output or (REPO_ROOT / f"rounds/r{args.round}/judging.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write HTML
    try:
        with open(output_path, "w") as f:
            f.write(html)
        print(f"Wrote {output_path.relative_to(REPO_ROOT)}")
        print(f"\nHTML rendered successfully. Open in browser to review.")
        print(f"\nHuman gate check: Rubric scores are FROM the judging.json, not generated by this script.")
        print(f"Review the HTML and verify all floor checks and scores before publishing.")
        return 0
    except Exception as e:
        print(f"ERROR writing HTML: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
