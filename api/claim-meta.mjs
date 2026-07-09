// zpoidh - generic POIDH claim metadata endpoint (GET /api/claim-meta).
//
// POIDH stores a claim's `uri` on-chain and its UI renders the claim by fetching that
// uri and reading {name, description, image} - no IPFS required, any CORS-enabled JSON
// endpoint works (see poidh-app ClaimImageEmbed). This mirrors the same pattern already
// shipped in ZAODEVZ/zabalgames (api/clip-meta.mjs) but generalized: that one is
// YouTube-recording-specific, this one takes any poster image URL directly, for use by
// docs/create-bounty.html (a standalone, non-Farcaster-gated bounty + claim tool).
//
// Stateless by design - everything needed is in the query string, because the uri is
// immutable once written on-chain:
//   GET /api/claim-meta?img=<posterUrl>&c=<submissionUrl>&t=<title>&d=<description>
//   -> { name, description, image, external_url }

export const config = { runtime: 'edge' };

const FALLBACK_IMAGE = 'https://zpoidh.vercel.app/assets/brand-kits/zabal-games/embed-card-gamez.png';

function json(body) {
  return new Response(JSON.stringify(body), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'public, max-age=86400, s-maxage=86400',
    },
  });
}

// Only ever echo back an http(s) URL - never anything else (data:, javascript:, etc).
function safeUrl(s) {
  try {
    const u = new URL(String(s || ''));
    return (u.protocol === 'http:' || u.protocol === 'https:') ? u.href : '';
  } catch (e) {
    return '';
  }
}

export default async function handler(req) {
  const url = new URL(req.url);
  const img = safeUrl(url.searchParams.get('img'));
  const clip = safeUrl(url.searchParams.get('c'));
  const title = (url.searchParams.get('t') || 'POIDH claim').slice(0, 140);
  let desc = (url.searchParams.get('d') || '').slice(0, 1000);

  if (clip && !desc.includes(clip)) desc = (desc ? desc + '\n\n' : '') + 'Submission: ' + clip;

  return json({
    name: title,
    description: desc,
    image: img || FALLBACK_IMAGE,
    external_url: clip || 'https://zpoidh.vercel.app',
  });
}
