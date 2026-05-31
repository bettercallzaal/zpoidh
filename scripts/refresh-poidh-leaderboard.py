#!/usr/bin/env python3
"""
Refresh poidh-leaderboard.json + poidh-claims.json by aggregating data
across one or more BCZ-issued POIDH bounties + the live $ZABAL Empire
POIDH Submitters leaderboard.

    python3 scripts/refresh-poidh-leaderboard.py
    python3 scripts/refresh-poidh-leaderboard.py --bounty 1151 --bounty 1166

Writes three files:

    poidh-leaderboard.json  - Empire Builder API-Sourced feed [{address, score}]
                              (matches the schema EB pulls from this URL)
    poidh-claims.json       - Rich data for poidh.html: bounties + claims +
                              live EB leaderboard with handles + rewards +
                              web3.bio profile supplements (avatar, X handle)
    poidh-audit.json        - Full claim trail for verification

Score = 1 per unique submitter wallet across the whole bounty set. Issuer
wallets are excluded (PoidhV3 enforces issuer != claimant on-chain).

Data sources (all free, no API keys):
    - poidh.xyz tRPC: bounties.fetch, claims.fetchBountyClaims
    - empirebuilder.world API: GET /api/leaderboards/<uuid> (handles + rewards)
    - api.web3.bio: GET /profile/<address> (avatar, X handle, bio)
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_BOUNTY_IDS = [1151, 1166]
DEFAULT_CHAIN_ID = 8453
ZABAL_EMPIRE_ID = "0xbB48f19B0494Ff7C1fE5Dc2032aeEE14312f0b07"
POIDH_LEADERBOARD_UUID = "7b8e8dfa-529d-48ad-8c9b-bdb45cc35187"
REPO_ROOT = Path(__file__).resolve().parent.parent

POIDH_BASE = "https://poidh.xyz/api/trpc"
EB_BASE = "https://www.empirebuilder.world/api"
WEB3_BIO_BASE = "https://api.web3.bio"

UA = "Mozilla/5.0 (poidh-leaderboard-refresh)"


def http_get(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def trpc(proc: str, payload: dict) -> dict:
    inp = urllib.parse.quote(json.dumps({"0": {"json": payload}}))
    return http_get(f"{POIDH_BASE}/{proc}?batch=1&input={inp}")[0]["result"]["data"]["json"]


def fetch_eb_leaderboard() -> dict:
    try:
        return http_get(f"{EB_BASE}/leaderboards/{POIDH_LEADERBOARD_UUID}", timeout=15)
    except Exception as e:
        print(f"  WARN: EB leaderboard fetch failed: {e}")
        return {"success": False, "leaderboard": None, "entries": []}


def fetch_web3_bio(address: str) -> dict | None:
    try:
        d = http_get(f"{WEB3_BIO_BASE}/profile/{address}", timeout=10)
        if isinstance(d, list) and d:
            for row in d:
                if row.get("platform") == "farcaster":
                    return row
            return d[0]
        return None
    except Exception:
        return None


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--bounty", type=int, action="append", default=None)
    p.add_argument("--chain", type=int, default=DEFAULT_CHAIN_ID)
    p.add_argument("--skip-web3bio", action="store_true", help="Skip web3.bio profile fetches (faster but no avatars/X)")
    args = p.parse_args()

    bounty_ids = args.bounty if args.bounty else DEFAULT_BOUNTY_IDS

    issuers: set[str] = set()
    seen: set[str] = set()
    unique_order: list[str] = []
    bounty_meta: list[dict] = []
    all_claims: list[dict] = []
    total_eth = 0.0
    total_claims = 0
    # Track which bounties each address submitted to (for score = bounty count)
    bounties_by_addr: dict[str, set[int]] = {}

    for bid in bounty_ids:
        b = trpc("bounties.fetch", {"id": bid, "chainId": args.chain})
        issuer = b["issuer"].lower()
        issuers.add(issuer)
        amount_eth = int(b.get("amount", "0") or 0) / 1e18
        total_eth += amount_eth

        claims_resp = trpc(
            "claims.fetchBountyClaims",
            {"bountyId": bid, "chainId": args.chain, "limit": 100},
        )
        items = claims_resp["items"]
        total_claims += len(items)

        print(f"Bounty {bid}: '{b['title'][:60]}' - {len(items)} claims, {amount_eth:.4f} ETH")

        for c in items:
            addr = c["issuer"].lower()
            if addr != issuer:
                bounties_by_addr.setdefault(addr, set()).add(bid)
                if addr not in seen:
                    seen.add(addr)
                    unique_order.append(addr)
            all_claims.append({
                "bounty_id": bid,
                "claim_id": c["id"],
                "issuer": addr,
                "title": (c.get("title") or ""),
                "description": (c.get("description") or ""),
                "image_url": c.get("url") or "",
                "accepted": bool(c.get("isAccepted")),
                "on_chain_id": c.get("onChainId"),
            })

        bounty_meta.append({
            "id": bid,
            "chainId": args.chain,
            "title": b["title"],
            "description": (b.get("description") or "")[:500],
            "issuer": issuer,
            "album": b.get("extra", {}).get("album"),
            "amount_eth": amount_eth,
            "in_progress": bool(b.get("inProgress")),
            "is_voting": bool(b.get("isVoting")),
            "is_canceled": bool(b.get("isCanceled")),
            "claims_count": sum(1 for c in all_claims if c["bounty_id"] == bid),
        })

    # Score = number of distinct BCZ bounties this wallet submitted to
    # (capped at len(bounty_ids), so e.g. submitting twice to one bounty still = 1
    # but submitting to both R1 + R2 = 2). Per Zaal 2026-05-27.
    def addr_score(addr: str) -> int:
        return len(bounties_by_addr.get(addr, set())) or 1

    leaderboard_feed = [{"address": a, "score": addr_score(a)} for a in unique_order]

    print(f"\nFetching live EB leaderboard...")
    eb = fetch_eb_leaderboard()
    eb_entries = eb.get("entries") or []
    eb_by_addr = {e["address"].lower(): e for e in eb_entries}
    print(f"  EB entries: {len(eb_entries)}, total ZABAL distributed so far: "
          f"{sum(e.get('totalRewards', 0) for e in eb_entries):.2f}")

    print(f"\nResolving submitter profiles via web3.bio...")
    profiles: dict[str, dict] = {}
    if not args.skip_web3bio:
        for addr in unique_order:
            row = fetch_web3_bio(addr)
            if row:
                profiles[addr] = {
                    "handle": row.get("identity"),
                    "displayName": row.get("displayName"),
                    "avatar": row.get("avatar"),
                    "description": row.get("description"),
                    "fid": (row.get("social") or {}).get("uid"),
                    "follower": (row.get("social") or {}).get("follower"),
                    "farcaster_url": (row.get("links", {}).get("farcaster") or {}).get("link"),
                    "twitter_handle": (row.get("links", {}).get("twitter") or {}).get("handle"),
                    "twitter_url": (row.get("links", {}).get("twitter") or {}).get("link"),
                }
                print(f"  {addr[:10]}... -> @{profiles[addr]['handle']}")
            else:
                profiles[addr] = {}
            time.sleep(0.15)

    enriched_leaderboard: list[dict] = []
    for addr in unique_order:
        eb_e = eb_by_addr.get(addr, {})
        prof = profiles.get(addr, {})
        enriched_leaderboard.append({
            "address": addr,
            "score": addr_score(addr),
            "rank": eb_e.get("rank"),
            "farcaster_username": eb_e.get("farcaster_username") or prof.get("handle"),
            "displayName": prof.get("displayName"),
            "avatar": prof.get("avatar"),
            "twitter_handle": prof.get("twitter_handle"),
            "twitter_url": prof.get("twitter_url"),
            "fid": prof.get("fid"),
            "boost": eb_e.get("boost"),
            "totalRewards": eb_e.get("totalRewards"),
            "follower": prof.get("follower"),
        })
    enriched_leaderboard.sort(key=lambda e: (e.get("rank") or 999, e["address"]))

    feed_path = REPO_ROOT / "poidh-leaderboard.json"
    claims_path = REPO_ROOT / "poidh-claims.json"
    audit_path = REPO_ROOT / "poidh-audit.json"

    feed_path.write_text(json.dumps(leaderboard_feed, indent=2) + "\n")

    claims_path.write_text(json.dumps({
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "empire": {
            "token_address": ZABAL_EMPIRE_ID,
            "leaderboard_uuid": POIDH_LEADERBOARD_UUID,
            "leaderboard_name": (eb.get("leaderboard") or {}).get("name"),
            "leaderboard_url": f"https://empirebuilder.world/empire/{ZABAL_EMPIRE_ID}",
            "last_eb_refresh": (eb.get("leaderboard") or {}).get("last_refreshed_at"),
            "apply_boosters": (eb.get("leaderboard") or {}).get("apply_boosters", False),
            "apply_reputation_boosters": (eb.get("leaderboard") or {}).get("apply_reputation_boosters", False),
            "apply_staking_boosters": (eb.get("leaderboard") or {}).get("apply_staking_boosters", False),
        },
        "totals": {
            "bounties": len(bounty_meta),
            "claims": total_claims,
            "unique_submitters": len(enriched_leaderboard),
            "total_eth_escrow": round(total_eth, 6),
            "total_zabal_distributed": round(sum(e.get("totalRewards", 0) or 0 for e in eb_entries), 4),
        },
        "bounties": bounty_meta,
        "leaderboard": enriched_leaderboard,
        "claims": all_claims,
    }, indent=2) + "\n")

    audit_path.write_text(json.dumps({
        "bounty_ids": bounty_ids,
        "chainId": args.chain,
        "issuers": sorted(issuers),
        "total_claims": total_claims,
        "submitter_count": len(enriched_leaderboard),
        "total_eth_escrow": round(total_eth, 6),
        "bounties": bounty_meta,
        "claims": all_claims,
    }, indent=2) + "\n")

    print(f"\nWrote {feed_path.relative_to(REPO_ROOT)} (EB feed): {len(leaderboard_feed)} entries")
    print(f"Wrote {claims_path.relative_to(REPO_ROOT)} (rich page data): {len(enriched_leaderboard)} submitters, {total_claims} claims")
    print(f"Wrote {audit_path.relative_to(REPO_ROOT)} (audit trail)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
