#!/usr/bin/env python3
"""Fable eval-runner - deterministic scoring backbone.

The Fable pipeline (see README.md) scores submissions against a weighted rubric,
gates them on floor rules, and produces a ranked board. The *scoring* judgement
(per-criterion numbers + prose feedback) is the AI-assisted / judge step and is
an INPUT here - this module does the deterministic part: enforce floor rules,
aggregate weighted scores, rank, and validate. That keeps the "AI-assisted, never
AI-decides" guardrail (README) honest: a human or Fable supplies the per-criterion
scores; this runner just does the arithmetic the same way every time, and it is
fully testable with no API keys (matching run-eval.md's manual-first ethos).

    python3 pipeline/score.py --rubric pipeline/rubric.example.json \\
                              --submissions <scores.json>
    python3 pipeline/score.py --selftest      # no network, no files

Input shapes
------------
rubric.json:
    {
      "round": 2,
      "criteria": [
        {"key": "distribution", "label": "Distribution", "weight": 0.35, "max": 10},
        ...   # weights must sum to 1.0
      ],
      "floor_rules": ["x_post", "tag_bcz", "duration"]   # each must be PASS
    }
submissions.json:
    {
      "submissions": [
        {"id": 6645, "handle": "joeyofdeus",
         "floor_checks": {"x_post": "PASS", "tag_bcz": "PASS", "duration": "PASS"},
         "scores": {"distribution": 9, "craft": 8, "substance": 9, "bonus": 8}},
        ...
      ]
    }
"""

import argparse
import json
import sys

WEIGHT_EPS = 1e-6


class RubricError(ValueError):
    """The rubric itself is invalid (weights, criteria)."""


def validate_rubric(rubric: dict) -> list[dict]:
    criteria = rubric.get("criteria") or []
    if not criteria:
        raise RubricError("rubric has no criteria")
    total_w = 0.0
    seen = set()
    for c in criteria:
        for field in ("key", "weight", "max"):
            if field not in c:
                raise RubricError(f"criterion {c!r} missing '{field}'")
        if c["key"] in seen:
            raise RubricError(f"duplicate criterion key '{c['key']}'")
        seen.add(c["key"])
        if c["max"] <= 0:
            raise RubricError(f"criterion '{c['key']}' has non-positive max {c['max']}")
        if c["weight"] < 0:
            raise RubricError(f"criterion '{c['key']}' has negative weight")
        total_w += c["weight"]
    if abs(total_w - 1.0) > WEIGHT_EPS:
        raise RubricError(f"criterion weights sum to {total_w}, must sum to 1.0")
    return criteria


def floor_failed(sub: dict, floor_rules: list[str]) -> list[str]:
    """Return the list of floor rules this submission did NOT pass (PASS only)."""
    checks = sub.get("floor_checks", {})
    return [r for r in floor_rules if str(checks.get(r, "")).upper() != "PASS"]


def weighted_score(sub: dict, criteria: list[dict]) -> float:
    """Normalized 0-100 weighted score. Raises if a score is out of [0, max]."""
    scores = sub.get("scores", {})
    total = 0.0
    for c in criteria:
        raw = scores.get(c["key"])
        if raw is None:
            raise ValueError(f"submission {sub.get('id')} missing score for '{c['key']}'")
        if not (0 <= raw <= c["max"]):
            raise ValueError(
                f"submission {sub.get('id')} score {raw} for '{c['key']}' out of [0, {c['max']}]"
            )
        total += (raw / c["max"]) * c["weight"]
    return round(total * 100, 2)


def score_round(rubric: dict, submissions: list[dict]) -> dict:
    """Gate on floor rules, weight-score the survivors, rank them. Pure."""
    criteria = validate_rubric(rubric)
    floor_rules = rubric.get("floor_rules", [])
    ranked, disqualified = [], []
    for sub in submissions:
        missed = floor_failed(sub, floor_rules)
        if missed:
            disqualified.append({"id": sub.get("id"), "handle": sub.get("handle"),
                                 "reason": "floor_fail", "failed_rules": missed})
            continue
        ranked.append({
            "id": sub.get("id"),
            "handle": sub.get("handle"),
            "weighted": weighted_score(sub, criteria),
            "per_criterion": {c["key"]: sub.get("scores", {}).get(c["key"]) for c in criteria},
        })
    # Deterministic order: score desc, then id asc as a stable tiebreak.
    ranked.sort(key=lambda e: (-e["weighted"], e["id"] if e["id"] is not None else 0))
    for i, e in enumerate(ranked, 1):
        e["rank"] = i
    return {"round": rubric.get("round"), "ranked": ranked, "disqualified": disqualified}


def render_board(result: dict) -> str:
    lines = [f"# Round {result.get('round')} - ranked board", ""]
    for e in result["ranked"]:
        crit = ", ".join(f"{k}={v}" for k, v in e["per_criterion"].items())
        lines.append(f"{e['rank']}. @{e['handle']} - {e['weighted']}/100  ({crit})")
    if result["disqualified"]:
        lines += ["", "## Did not pass floor rules"]
        for d in result["disqualified"]:
            lines.append(f"- @{d['handle']}: failed {', '.join(d['failed_rules'])}")
    return "\n".join(lines)


def _selftest() -> int:
    """Network-free proof of floor-gating, weighted ranking, and validation.
    Run: python3 pipeline/score.py --selftest"""
    # distribution is heavily weighted, so it decides the ranking even though
    # bravo is stronger on the other two criteria (unweighted, bravo would win).
    rubric = {
        "round": 2,
        "criteria": [
            {"key": "distribution", "label": "Distribution", "weight": 0.7, "max": 10},
            {"key": "craft", "label": "Craft", "weight": 0.15, "max": 10},
            {"key": "substance", "label": "Substance", "weight": 0.15, "max": 10},
        ],
        "floor_rules": ["x_post", "duration"],
    }
    subs = [
        # Maxes the high-weight criterion -> should rank #1 despite weak craft/substance.
        {"id": 1, "handle": "alpha", "floor_checks": {"x_post": "PASS", "duration": "PASS"},
         "scores": {"distribution": 10, "craft": 2, "substance": 2}},
        # Stronger on the two low-weight criteria; unweighted it would win, weighted it does not.
        {"id": 2, "handle": "bravo", "floor_checks": {"x_post": "PASS", "duration": "PASS"},
         "scores": {"distribution": 5, "craft": 10, "substance": 10}},
        # Top scores but OVER on duration (the real R2 FAIL-OVER case) -> disqualified.
        {"id": 3, "handle": "charlie", "floor_checks": {"x_post": "PASS", "duration": "FAIL"},
         "scores": {"distribution": 10, "craft": 10, "substance": 10}},
    ]
    res = score_round(rubric, subs)
    checks = []

    order = [e["handle"] for e in res["ranked"]]
    checks.append(("floor gate disqualifies over-duration even with all-10s",
                   [d["handle"] for d in res["disqualified"]] == ["charlie"]))
    checks.append(("high-weight criterion decides the ranking (alpha over bravo)",
                   order == ["alpha", "bravo"]))
    checks.append(("alpha weighted = 76.0", res["ranked"][0]["weighted"] == 76.0))
    checks.append(("bravo weighted = 65.0", res["ranked"][1]["weighted"] == 65.0))
    checks.append(("ranks are 1..N", [e["rank"] for e in res["ranked"]] == [1, 2]))

    # weights must sum to 1.0
    try:
        validate_rubric({"criteria": [{"key": "a", "weight": 0.5, "max": 10}]})
        checks.append(("bad weights rejected", False))
    except RubricError:
        checks.append(("bad weights rejected", True))

    # out-of-range score rejected
    try:
        weighted_score({"id": 9, "scores": {"distribution": 99}}, rubric["criteria"][:1])
        checks.append(("out-of-range score rejected", False))
    except ValueError:
        checks.append(("out-of-range score rejected", True))

    fails = 0
    for label, ok in checks:
        fails += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    print(f"selftest: {len(checks) - fails}/{len(checks)} passed")
    return 1 if fails else 0


def main() -> int:
    p = argparse.ArgumentParser(description="Fable eval-runner - deterministic scoring backbone")
    p.add_argument("--selftest", action="store_true", help="run the network-free self-test and exit")
    p.add_argument("--rubric", help="path to rubric.json")
    p.add_argument("--submissions", help="path to submissions.json")
    p.add_argument("--json", action="store_true", help="emit the ranked result as JSON instead of a board")
    args = p.parse_args()

    if args.selftest:
        return _selftest()

    if not args.rubric or not args.submissions:
        p.error("--rubric and --submissions are required (or use --selftest)")

    rubric = json.load(open(args.rubric))
    submissions = json.load(open(args.submissions)).get("submissions", [])
    try:
        result = score_round(rubric, submissions)
    except (RubricError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2) if args.json else render_board(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
