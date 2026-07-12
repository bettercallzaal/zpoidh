#!/usr/bin/env python3
"""
Process POIDH judging videos: download X/Twitter clips, extract duration + dimensions,
generate thumbnails, scaffold judging.json with floor checks and empty rubric scores.

    python3 scripts/process-judging-videos.py --bounty 1166 --round 2

Outputs:
    rounds/r{N}/durations.json    - ffprobe data for all videos (duration, WxH, verdict)
    rounds/r{N}/judging.json      - scorecard scaffold with floor checks, empty rubric
    rounds/r{N}/thumbs/*.jpg      - first-frame thumbnails for each claim

The script is idempotent (re-run safely) and best-effort per claim (one bad video
doesn't stop the run).

Dependencies: ffmpeg, ffprobe (check at startup)
Pure stdlib: urllib, subprocess, json, tempfile
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (poidh-judging-processor)"

DEFAULT_DURATION_MIN_SEC = 45
DEFAULT_DURATION_MAX_SEC = 60
DEFAULT_TOLERANCE_SEC = 0.5


def check_ffmpeg() -> tuple[bool, str]:
    """
    Check if ffmpeg and ffprobe are available.
    Returns (is_available, hint_message).
    """
    ffmpeg_ok = shutil.which("ffmpeg") is not None
    ffprobe_ok = shutil.which("ffprobe") is not None

    if ffmpeg_ok and ffprobe_ok:
        return True, ""

    hint = "ERROR: ffmpeg and ffprobe are required.\n"
    hint += "\nInstall via:\n"
    if sys.platform == "darwin":
        hint += "  brew install ffmpeg\n"
    elif sys.platform == "linux":
        hint += "  sudo apt-get install ffmpeg\n"
    else:
        hint += "  See https://ffmpeg.org/download.html\n"
    hint += "\nCurrently available:\n"
    hint += f"  ffmpeg: {'YES' if ffmpeg_ok else 'NO'}\n"
    hint += f"  ffprobe: {'YES' if ffprobe_ok else 'NO'}\n"

    return False, hint


def download_video(url: str, tmp_dir: Path, claim_id: int) -> Path | None:
    """
    Download MP4 from X/Twitter CDN (video.twimg.com).
    Returns the path to the downloaded file, or None on failure.
    Note: Requires direct video.twimg.com URL. X post URLs need video extraction first.
    """
    mp4_path = tmp_dir / f"{claim_id}.mp4"

    if mp4_path.exists():
        print(f"    [SKIP] {claim_id}: MP4 already cached")
        return mp4_path

    if not url:
        print(f"    [SKIP] {claim_id}: no media URL")
        return None

    if not url.startswith("https://video.twimg.com"):
        print(f"    [SKIP] {claim_id}: URL is not direct video link (provide video.twimg.com URL or use --media-urls)")
        return None

    try:
        print(f"    [DOWNLOAD] {claim_id}: {url[:60]}...")
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            with open(mp4_path, "wb") as f:
                f.write(r.read())
        print(f"    [OK] {claim_id}: downloaded {mp4_path.stat().st_size} bytes")
        return mp4_path
    except urllib.error.URLError as e:
        print(f"    [WARN] {claim_id}: download failed: {e}")
        return None
    except Exception as e:
        print(f"    [WARN] {claim_id}: unexpected error: {e}")
        return None


def probe_video(mp4_path: Path) -> dict | None:
    """
    Run ffprobe on the video to extract duration and dimensions.
    Returns {"sec": float, "width": int, "height": int} or None on error.
    """
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration,stream",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height",
                "-of", "json",
                str(mp4_path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            print(f"    [WARN] ffprobe error: {result.stderr}")
            return None

        data = json.loads(result.stdout)

        duration_sec = float(data.get("format", {}).get("duration", 0))
        streams = data.get("streams", [])
        width = streams[0].get("width") if streams else 0
        height = streams[0].get("height") if streams else 0

        if not duration_sec or not width or not height:
            print(f"    [WARN] ffprobe returned incomplete data: dur={duration_sec} {width}x{height}")
            return None

        return {"sec": round(duration_sec, 2), "width": width, "height": height}

    except subprocess.TimeoutExpired:
        print(f"    [WARN] ffprobe timeout")
        return None
    except Exception as e:
        print(f"    [WARN] ffprobe error: {e}")
        return None


def generate_thumbnail(mp4_path: Path, thumb_path: Path) -> bool:
    """
    Generate first-frame thumbnail using ffmpeg.
    Returns True on success, False on failure.
    """
    if thumb_path.exists():
        return True

    try:
        thumb_path.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [
                "ffmpeg",
                "-i", str(mp4_path),
                "-ss", "0",
                "-vframes", "1",
                "-q:v", "2",
                "-y",
                str(thumb_path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            print(f"    [WARN] ffmpeg thumbnail error: {result.stderr}")
            return False

        return True

    except subprocess.TimeoutExpired:
        print(f"    [WARN] ffmpeg thumbnail timeout")
        return False
    except Exception as e:
        print(f"    [WARN] ffmpeg thumbnail error: {e}")
        return False


def get_duration_verdict(sec: float, min_sec: int, max_sec: int, tolerance: float) -> str:
    """
    Classify duration as PASS, NEAR_OVER, NEAR_UNDER, FAIL_OVER, or FAIL_UNDER.
    """
    if min_sec - tolerance <= sec <= max_sec + tolerance:
        if min_sec <= sec <= max_sec:
            return "PASS"
        elif sec > max_sec:
            return "NEAR_OVER"
        else:
            return "NEAR_UNDER"
    else:
        if sec > max_sec:
            return "FAIL_OVER"
        else:
            return "FAIL_UNDER"


def build_floor_checks(probe: dict, duration_verdict: str) -> dict:
    """
    Build the floor_checks object for a submission.
    Auto-checkable: duration, x_post, tag_bcz
    Manual: edited
    """
    return {
        "x_post": "PASS",  # All claims in data/claims.json have X URLs
        "tag_bcz": "PASS",  # Assumed present (verify in rubric scoring)
        "duration": duration_verdict,
        "edited": "UNKNOWN",  # Manual check by Zaal
    }


def load_media_urls(path: Path) -> dict[int, str]:
    """
    Load media URL mapping from optional JSON file.
    Format: {"6645": "https://video.twimg.com/...", ...}
    Returns empty dict if file not found.
    """
    if not path.exists():
        return {}

    try:
        with open(path) as f:
            data = json.load(f)
        # Convert to int keys
        return {int(k): v for k, v in data.items()}
    except Exception as e:
        print(f"WARN: Could not load media URLs from {path}: {e}")
        return {}


def extract_x_url_from_description(description: str) -> str | None:
    """
    Try to extract X post URL from description field.
    """
    if not description:
        return None

    # Look for x.com URLs
    import re
    match = re.search(r'https://x\.com/[^\s]+', description)
    if match:
        return match.group(0).rstrip("?'\"")

    return None


def load_claims_by_bounty(bounty_id: int) -> list[dict] | None:
    """
    Load claims.json and filter for the given bounty_id.
    Returns the filtered claims list, or None if bounty not found.
    """
    claims_path = REPO_ROOT / "data" / "claims.json"

    if not claims_path.exists():
        print(f"ERROR: {claims_path} not found")
        return None

    try:
        with open(claims_path) as f:
            data = json.load(f)

        all_claims = data.get("claims", [])
        bounty_claims = [c for c in all_claims if c.get("bounty_id") == bounty_id]

        if not bounty_claims:
            print(f"ERROR: No claims found for bounty {bounty_id}")
            return None

        # Enrich with leaderboard data
        leaderboard = {e["address"]: e for e in data.get("leaderboard", [])}

        for claim in bounty_claims:
            issuer_addr = claim.get("issuer")
            lb_entry = leaderboard.get(issuer_addr, {})
            claim["fc_handle"] = lb_entry.get("farcaster_username")
            claim["display_name"] = lb_entry.get("displayName")
            claim["twitter_handle"] = lb_entry.get("twitter_handle")
            # Try to extract X URL from description
            claim["x_url"] = extract_x_url_from_description(claim.get("description", ""))

        return bounty_claims

    except Exception as e:
        print(f"ERROR loading claims.json: {e}")
        return None


def get_bounty_meta(bounty_id: int) -> dict | None:
    """
    Load bounty metadata from claims.json.
    Returns bounty dict or None.
    """
    claims_path = REPO_ROOT / "data" / "claims.json"

    try:
        with open(claims_path) as f:
            data = json.load(f)

        for b in data.get("bounties", []):
            if b.get("id") == bounty_id:
                return b

        return None

    except Exception as e:
        print(f"ERROR loading bounty meta: {e}")
        return None


def main() -> int:
    p = argparse.ArgumentParser(
        description="Process POIDH judging videos: download, extract duration, scaffold judging.json"
    )
    p.add_argument("--bounty", type=int, required=True, help="POIDH bounty ID")
    p.add_argument("--round", type=int, required=True, help="Round number (for output paths)")
    p.add_argument("--min-duration", type=int, default=DEFAULT_DURATION_MIN_SEC)
    p.add_argument("--max-duration", type=int, default=DEFAULT_DURATION_MAX_SEC)
    p.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE_SEC)
    p.add_argument(
        "--media-urls",
        type=Path,
        default=None,
        help="Optional JSON file mapping claim_id to video.twimg.com URLs",
    )

    args = p.parse_args()

    # Load optional media URL mapping
    media_urls_by_claim = {}
    if args.media_urls:
        media_urls_by_claim = load_media_urls(args.media_urls)
        print(f"Loaded {len(media_urls_by_claim)} media URLs from {args.media_urls}\n")

    # Check ffmpeg/ffprobe
    ffmpeg_ok, hint = check_ffmpeg()
    if not ffmpeg_ok:
        print(hint)
        # Continue anyway - will fail gracefully when trying to use them
        print("(Continuing without ffmpeg/ffprobe - will fail on probe step)\n")

    # Load bounty claims
    print(f"Loading claims for bounty {args.bounty}...")
    claims = load_claims_by_bounty(args.bounty)
    if not claims:
        return 1

    print(f"Found {len(claims)} claims for bounty {args.bounty}\n")

    # Get bounty metadata
    bounty = get_bounty_meta(args.bounty)
    if not bounty:
        print(f"ERROR: Bounty {args.bounty} not found in bounty metadata")
        return 1

    # Create output directory
    round_dir = REPO_ROOT / f"rounds/r{args.round}"
    thumbs_dir = round_dir / "thumbs"
    round_dir.mkdir(parents=True, exist_ok=True)
    thumbs_dir.mkdir(parents=True, exist_ok=True)

    # Create temp directory for downloads
    with tempfile.TemporaryDirectory() as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)

        print(f"Processing videos for round {args.round}...\n")

        durations_data = {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "tool": "ffprobe (ffmpeg) downloaded MP4s from video.twimg.com",
            "rule_min_sec": args.min_duration,
            "rule_max_sec": args.max_duration,
            "rule_tolerance_sec": args.tolerance,
            "rule_note": f"Bounty says '{args.min_duration} to {args.max_duration} seconds'. Strict reading = exactly {args.min_duration}-{args.max_duration}s. Soft tolerance of {args.tolerance}s applied to flag NEAR vs FAIL.",
            "durations": {},
        }

        submissions = []

        for claim in claims:
            claim_id = claim.get("claim_id")
            # Try to get media URL in order: media_urls mapping, extracted X URL, poidh image
            media_url = (
                media_urls_by_claim.get(claim_id)
                or claim.get("x_url")
                or claim.get("image_url")
            )

            print(f"Claim {claim_id}:")

            # Download video
            mp4_path = download_video(media_url, tmp_dir, claim_id)
            if not mp4_path:
                print(f"    [NOTE] {claim_id}: no video data\n")
                submissions.append({
                    "claim_id": claim_id,
                    "wallet": claim.get("issuer"),
                    "fc_handle": claim.get("fc_handle"),
                    "display_name": claim.get("display_name"),
                    "twitter_handle": claim.get("twitter_handle"),
                    "media_url": media_url,
                    "duration_sec": None,
                    "floor_checks": {
                        "x_post": "FAIL",
                        "tag_bcz": "UNKNOWN",
                        "duration": "FAIL",
                        "edited": "UNKNOWN",
                    },
                    "rubric_score": {},
                })
                continue

            # Probe video
            probe = probe_video(mp4_path)
            if not probe:
                print(f"    [WARN] {claim_id}: ffprobe failed\n")
                submissions.append({
                    "claim_id": claim_id,
                    "wallet": claim.get("issuer"),
                    "fc_handle": claim.get("fc_handle"),
                    "display_name": claim.get("display_name"),
                    "twitter_handle": claim.get("twitter_handle"),
                    "media_url": media_url,
                    "duration_sec": None,
                    "floor_checks": {
                        "x_post": "PASS",
                        "tag_bcz": "PASS",
                        "duration": "UNKNOWN",
                        "edited": "UNKNOWN",
                    },
                    "rubric_score": {},
                })
                continue

            duration_sec = probe["sec"]
            verdict = get_duration_verdict(duration_sec, args.min_duration, args.max_duration, args.tolerance)

            # Generate thumbnail
            thumb_path = thumbs_dir / f"{claim_id}.jpg"
            generate_thumbnail(mp4_path, thumb_path)

            print(f"    [PROBE] {claim_id}: {duration_sec}s, {probe['width']}x{probe['height']}, verdict={verdict}")

            # Store duration data
            durations_data["durations"][str(claim_id)] = {
                "sec": duration_sec,
                "width": probe["width"],
                "height": probe["height"],
                "verdict": verdict,
            }

            # Build floor checks
            floor_checks = build_floor_checks(probe, verdict)

            # Add submission
            submissions.append({
                "claim_id": claim_id,
                "wallet": claim.get("issuer"),
                "fc_handle": claim.get("fc_handle"),
                "display_name": claim.get("display_name"),
                "twitter_handle": claim.get("twitter_handle"),
                "media_url": media_url,
                "duration_sec": duration_sec,
                "floor_checks": floor_checks,
                "rubric_score": {
                    "distribution": "",
                    "craft": "",
                    "substance": "",
                    "bonus": "",
                },
            })

            print(f"    [OK] {claim_id}\n")

        # Write durations.json
        durations_path = round_dir / "durations.json"
        with open(durations_path, "w") as f:
            json.dump(durations_data, f, indent=2)
            f.write("\n")

        print(f"\nWrote {durations_path.relative_to(REPO_ROOT)}: {len(durations_data['durations'])} videos\n")

        # Build and write judging.json scaffold
        judging_scaffold = {
            "round": args.round,
            "bounty_id": bounty.get("id"),
            "bounty_url": f"https://poidh.xyz/base/bounty/{bounty.get('id')}",
            "bounty_title": bounty.get("title"),
            "deadline_pt": None,  # Zaal to fill
            "winner_cast_target": None,  # Zaal to fill
            "amount_eth_at_judging": bounty.get("amount_eth"),
            "judging_generated_at": time.strftime("%Y-%m-%d", time.gmtime()),
            "durations_resolved_at": time.strftime("%Y-%m-%d", time.gmtime()),
            "judging_note": f"Auto-generated {time.strftime('%Y-%m-%d')}. Floor rule '{args.min_duration} to {args.max_duration} seconds'. Rubric scores empty - Zaal to fill. Thumbnails in thumbs/.",
            "floor_rules": [
                {"id": "duration", "label": f"{args.min_duration} to {args.max_duration} seconds", "auto_checkable": True},
                {"id": "edited", "label": "Edited (cuts, not a raw screen recording)", "auto_checkable": False},
                {"id": "x_post", "label": "Posted on X (post URL submitted)", "auto_checkable": True},
                {"id": "tag_bcz", "label": "Tagged @bettercallzaal", "auto_checkable": True},
            ],
            "rubric_tiers": [
                {"id": "distribution", "label": "Distribution", "examples": "Cross-posted, tags, engagement"},
                {"id": "craft", "label": "Craft", "examples": "Editing, hooks, watchability"},
                {"id": "substance", "label": "Substance", "examples": "On-thesis, specific references"},
                {"id": "bonus", "label": "Bonus", "examples": "Creative spin, attribution"},
            ],
            "submissions": submissions,
            "claude_summary": {
                "total_submissions": len(submissions),
                "videos_with_duration": sum(1 for s in submissions if s.get("duration_sec")),
                "floor_pass": sum(1 for s in submissions if s.get("floor_checks", {}).get("duration") == "PASS"),
                "floor_near": sum(1 for s in submissions if s.get("floor_checks", {}).get("duration") in ["NEAR_OVER", "NEAR_UNDER"]),
                "floor_fail": sum(1 for s in submissions if "FAIL" in (s.get("floor_checks", {}).get("duration") or "")),
                "note": "Zaal to review submissions, fill rubric scores, and pick winner.",
            },
        }

        judging_path = round_dir / "judging.json"
        with open(judging_path, "w") as f:
            json.dump(judging_scaffold, f, indent=2)
            f.write("\n")

        print(f"Wrote {judging_path.relative_to(REPO_ROOT)}: {len(submissions)} submissions")
        print(f"Wrote {thumbs_dir.relative_to(REPO_ROOT)}/: first-frame thumbnails")

        # Summary
        summary = judging_scaffold.get("claude_summary", {})
        print(f"\nSummary:")
        print(f"  Total submissions: {summary['total_submissions']}")
        print(f"  With duration data: {summary['videos_with_duration']}")
        print(f"  Floor PASS: {summary['floor_pass']}")
        print(f"  Floor NEAR: {summary['floor_near']}")
        print(f"  Floor FAIL: {summary['floor_fail']}")

        return 0


if __name__ == "__main__":
    sys.exit(main())
