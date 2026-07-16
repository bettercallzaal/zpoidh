#!/usr/bin/env node
/**
 * Fable Submission Eval Runner for POIDH Bounty Rounds
 *
 * Takes one past POIDH round's submissions + the doc-1120 rubric,
 * scores EACH submission against the rubric via Claude,
 * and writes per-submitter scorecards + cohort synthesis.
 *
 * Usage:
 *   ANTHROPIC_API_KEY=... node pipeline/eval-runner.mjs --round r3
 *   node pipeline/eval-runner.mjs --round r3 --dry-run
 *   node pipeline/eval-runner.mjs --round r3 --claim 6749
 *
 * Output:
 *   data/scorecards/<round>/<claimId>.json - per-submitter scorecard
 *   data/scorecards/<round>/_synthesis.json - cohort synthesis
 *
 * Dry-run mode: builds prompts, validates schemas, writes stubs without API call.
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, "..");

/**
 * @typedef {Object} Submission
 * @property {number} claim_id
 * @property {string} wallet
 * @property {string} fc_handle
 * @property {string} title
 * @property {string} x_url
 * @property {string} [fc_url]
 * @property {string} [extra_link]
 * @property {boolean} accepted
 * @property {boolean} winner
 * @property {string} [note]
 */

/**
 * @typedef {Object} Scorecard
 * @property {number} distribution
 * @property {number} craft
 * @property {number} substance
 * @property {number} spec_compliance
 * @property {number} overall
 * @property {boolean} floor_pass
 * @property {string} feedback
 * @property {string[]} next_round
 */

/**
 * @typedef {Object} SubmissionScorecard
 * @property {string} claimId
 * @property {string} round
 * @property {string} wallet
 * @property {string} fcHandle
 * @property {string} submissionUrl
 * @property {string} model
 * @property {string} generatedAt
 * @property {Scorecard} score
 */

/**
 * @typedef {Object} CohortSynthesis
 * @property {string} round
 * @property {number} submissionCount
 * @property {Object} averageScores
 * @property {number} averageScores.distribution
 * @property {number} averageScores.craft
 * @property {number} averageScores.substance
 * @property {number} averageScores.spec_compliance
 * @property {number} averageScores.overall
 * @property {string} floorPassRate
 * @property {Object[]} standouts
 * @property {string[]} patterns
 * @property {string} model
 * @property {string} generatedAt
 */

// ============================================================================
// Parse CLI Args
// ============================================================================

/** @type {string|null} */
let targetRound = null;

/** @type {string|null} */
let targetClaim = null;

/** @type {boolean} */
let dryRun = false;

for (let i = 2; i < process.argv.length; i++) {
  const arg = process.argv[i];
  if (arg === "--round" && i + 1 < process.argv.length) {
    targetRound = process.argv[++i];
  } else if (arg === "--claim" && i + 1 < process.argv.length) {
    targetClaim = process.argv[++i];
  } else if (arg === "--dry-run") {
    dryRun = true;
  }
}

if (!targetRound) {
  console.error("Usage: node eval-runner.mjs --round r3 [--claim <id>] [--dry-run]");
  process.exit(1);
}

// ============================================================================
// Load Data
// ============================================================================

/**
 * Load submissions for a round from rounds/<round>/judging.json
 * @param {string} round
 * @returns {Submission[]}
 */
function loadSubmissions(round) {
  const judgingPath = path.join(REPO_ROOT, `rounds/${round}/judging.json`);
  if (!fs.existsSync(judgingPath)) {
    throw new Error(`Judging file not found: ${judgingPath}`);
  }
  const data = JSON.parse(fs.readFileSync(judgingPath, "utf-8"));
  return data.submissions || [];
}

/**
 * Load round description from rounds/<round>/description.md
 * @param {string} round
 * @returns {string}
 */
function loadDescription(round) {
  const descPath = path.join(REPO_ROOT, `rounds/${round}/description.md`);
  if (!fs.existsSync(descPath)) {
    throw new Error(`Description file not found: ${descPath}`);
  }
  return fs.readFileSync(descPath, "utf-8");
}

/**
 * Load floor rules from rounds/<round>/judging.json
 * @param {string} round
 * @returns {Object[]}
 */
function loadFloorRules(round) {
  const judgingPath = path.join(REPO_ROOT, `rounds/${round}/judging.json`);
  const data = JSON.parse(fs.readFileSync(judgingPath, "utf-8"));
  return data.floor_rules || [];
}

// ============================================================================
// Schema Validation
// ============================================================================

const SCORECARD_SCHEMA = {
  type: "object",
  properties: {
    distribution: { type: "integer", minimum: 0, maximum: 10 },
    craft: { type: "integer", minimum: 0, maximum: 10 },
    substance: { type: "integer", minimum: 0, maximum: 10 },
    spec_compliance: { type: "integer", minimum: 0, maximum: 10 },
    overall: { type: "integer", minimum: 0, maximum: 10 },
    floor_pass: { type: "boolean" },
    feedback: { type: "string" },
    next_round: { type: "array", items: { type: "string" } },
  },
  required: [
    "distribution",
    "craft",
    "substance",
    "spec_compliance",
    "overall",
    "floor_pass",
    "feedback",
    "next_round",
  ],
  additionalProperties: false,
};

const COHORT_SCHEMA = {
  type: "object",
  properties: {
    average_distribution: { type: "number" },
    average_craft: { type: "number" },
    average_substance: { type: "number" },
    average_spec_compliance: { type: "number" },
    average_overall: { type: "number" },
    floor_pass_rate: { type: "string" },
    standouts: { type: "array" },
    patterns: { type: "array", items: { type: "string" } },
  },
  required: [
    "average_distribution",
    "average_craft",
    "average_substance",
    "average_spec_compliance",
    "average_overall",
    "floor_pass_rate",
    "standouts",
    "patterns",
  ],
  additionalProperties: false,
};

/**
 * Validate JSON against a JSON schema (basic structural check)
 * @param {*} data
 * @param {Object} schema
 * @returns {boolean}
 */
function validateSchema(data, schema) {
  if (typeof data !== "object" || data === null) return false;
  for (const key of schema.required || []) {
    if (!(key in data)) return false;
  }
  return true;
}

// ============================================================================
// Rubric (from doc-1120)
// ============================================================================

const RUBRIC_SYSTEM_PROMPT = `You are a professional POIDH bounty evaluator using the doc-1120 rubric.

You will score submissions across FOUR dimensions, each 0-10:

1. **Distribution** (cross-posting / reach multiplier)
   - Did the submitter post across Farcaster channels + X?
   - Did they tag the key handles (@bettercallzaal, @poidhxyz, other boosters)?
   - Is there evidence of intentional reach (multiple platforms, tagged participants)?
   - Excellent (9-10): Tagged all key handles, cross-posted multiple platforms, 10+ engagement
   - Strong (7-8): Tagged 2+ handles, posted on X and Farcaster, 5-9 engagement
   - Adequate (5-6): Posted on 1-2 platforms, minimal tags
   - Weak (3-4): Posted on only X or Farcaster, minimal/no tags
   - Fails (1-2): Not posted or no clear distribution intent

2. **Craft** (production value + optimal-signal craft)
   - Is the submission technically polished and well-edited?
   - Does it hit the exact length spec (if video)?
   - Is the audio/video mix clean? Are there captions if audio?
   - Does it look intentional, not a raw screencast?
   - Excellent (9-10): Tight edits, hook in first 3s, clear CTA, captions sync'd, holds attention
   - Strong (7-8): Some cuts/pacing, hook present, clear message, production intent visible
   - Adequate (5-6): Watchable, pacing okay, minimal editing
   - Weak (3-4): Looks raw or like a slide show, pacing drags
   - Fails (1-2): Unwatchable or unintelligible

3. **Substance** (clarity + originality of the message)
   - Is the core message clear? Do you understand it in 3 seconds?
   - Does it capture the essence of what the bounty is asking for?
   - Is there originality or a unique take?
   - Excellent (9-10): Directly cites source by name, captures thesis exactly, sounds authentic
   - Strong (7-8): References main idea, mentions key figures, coherent but less precise
   - Adequate (5-6): Mentions context but doesn't land the specific angle
   - Weak (3-4): Tangentially related, no clear connection to bounty thesis
   - Fails (1-2): No clear connection to what was asked

4. **Spec Compliance** (hard rules from the round's description)
   - Did the submission meet the floor rules?
   - FLOOR FAIL on ANY hard-rule violation (length, format, tagging, audio rules, etc.)
   - Excellent (9-10): All floor rules met with room to spare
   - Adequate (5-8): All floor rules met
   - Fails (1-4): One or more floor rules violated → floor_pass=false

**Overall Score**: After scoring all four dimensions, produce an OVERALL (0-10) that synthesizes them. Do not average; use judgment on which dimensions matter most for THIS bounty.

**Floor Pass**: boolean. If ANY floor rule is violated, floor_pass=false. Otherwise true.

**Feedback**: Write ONE paragraph directed TO the submitter (as if sending them this feedback). Be constructive but honest. Reference specific scores + what worked. Suggest 1-2 things to improve. End on encouragement.

**Next Round**: Array of 1-3 concrete action strings for next submission (e.g., ["Post 1 week before deadline for engagement time", "Try vertical format for mobile", "Name the source episode explicitly"]).

Return ONLY valid JSON matching the schema. No markdown, no explanation.`;

// ============================================================================
// Prompt Building
// ============================================================================

/**
 * Build the user prompt for a single submission
 * @param {Submission} submission
 * @param {string} roundDescription
 * @param {Object[]} floorRules
 * @returns {string}
 */
function buildSubmissionPrompt(submission, roundDescription, floorRules) {
  const floorRulesText = floorRules
    .map((r) => `- ${r.label}`)
    .join("\n");

  return `Round Description and Floor Rules:
${roundDescription}

Floor Rules (HARD REQUIREMENTS):
${floorRulesText}

---

Submission to Score:

Claim ID: ${submission.claim_id}
Farcaster Handle: ${submission.fc_handle}
Submission Title: ${submission.title}
X URL: ${submission.x_url}
Farcaster URL: ${submission.fc_url || "Not provided"}
Extra Link: ${submission.extra_link || "None"}
Note: ${submission.note || "None"}

---

Score this submission on the four dimensions (distribution, craft, substance, spec_compliance).
Be specific and reference the actual submission details.
Output ONLY the JSON scorecard, no other text.`;
}

/**
 * Build the user prompt for cohort synthesis
 * @param {SubmissionScorecard[]} scorecards
 * @returns {string}
 */
function buildCohortPrompt(scorecards) {
  const scorecardsSummary = scorecards
    .map(
      (sc) => `
Claim ${sc.claimId} (${sc.fcHandle}):
- Distribution: ${sc.score.distribution}/10
- Craft: ${sc.score.craft}/10
- Substance: ${sc.score.substance}/10
- Spec Compliance: ${sc.score.spec_compliance}/10
- Overall: ${sc.score.overall}/10
- Floor Pass: ${sc.score.floor_pass}
- Feedback: ${sc.score.feedback}
`
    )
    .join("\n");

  return `You are synthesizing evaluation results across a full POIDH round.

All Submission Scorecards:
${scorecardsSummary}

---

Synthesize the round with:

1. **average_distribution**, **average_craft**, **average_substance**, **average_spec_compliance**, **average_overall**:
   Calculate the mean across all submissions for each dimension.

2. **floor_pass_rate**: Format as "X/N" (e.g., "5/8" means 5 out of 8 passed floor rules).

3. **standouts**: Array of objects with:
   - claim_id (string)
   - reason (string) - why this stood out (highest score? unique angle? best craft?)

4. **patterns**: Array of 1-3 strings describing emerging themes (e.g.,
   "Video submitted at exact 60s sweet spot = optimal craft signal",
   "Cross-posted all channels = distribution multiplier",
   "Direct source attribution drove substance scores 2-3 points higher"
).

Focus on patterns that help NEXT round's submitters understand what works.
Output ONLY the JSON synthesis object, no other text.`;
}

// ============================================================================
// Dry Run Mode
// ============================================================================

/**
 * Generate stub scorecard (dry run, no API)
 * @param {Submission} submission
 * @returns {Scorecard}
 */
function generateStubScorecard(submission) {
  // Stub: lower scores for non-winners, higher for winners
  const baseScore = submission.winner ? 8 : 5;
  return {
    distribution: baseScore - 1,
    craft: baseScore,
    substance: baseScore + 1,
    spec_compliance: submission.accepted ? 9 : 7,
    overall: baseScore,
    floor_pass: submission.accepted,
    feedback: `[DRY RUN STUB] This is a placeholder scorecard generated without Claude evaluation. In production, Claude would provide personalized feedback for ${submission.fc_handle}.`,
    next_round: ["[stub] Post earlier for engagement", "[stub] Consider cross-platform presence"],
  };
}

/**
 * Generate stub synthesis (dry run, no API)
 * @param {SubmissionScorecard[]} scorecards
 * @returns {Object}
 */
function generateStubSynthesis(scorecards) {
  const floorPassed = scorecards.filter((sc) => sc.score.floor_pass).length;
  return {
    average_distribution: 6.2,
    average_craft: 6.1,
    average_substance: 6.8,
    average_spec_compliance: 7.9,
    average_overall: 6.5,
    floor_pass_rate: `${floorPassed}/${scorecards.length}`,
    standouts: [
      {
        claim_id: scorecards[0]?.claimId || "unknown",
        reason: "[stub] Highest overall score",
      },
    ],
    patterns: ["[stub] Pattern 1 from dry run", "[stub] Pattern 2 from dry run"],
  };
}

// ============================================================================
// API Call (Lazy Import)
// ============================================================================

/**
 * Call Claude via Anthropic SDK
 * @param {string} systemPrompt
 * @param {string} userPrompt
 * @param {Object} outputSchema
 * @returns {Promise<Object>}
 */
async function callClaude(systemPrompt, userPrompt, outputSchema) {
  // Lazy import: only load SDK if not in dry run
  const { default: Anthropic } = await import("@anthropic-ai/sdk");
  const client = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY,
  });

  if (!process.env.ANTHROPIC_API_KEY) {
    throw new Error(
      "ANTHROPIC_API_KEY not set. Set it or use --dry-run mode."
    );
  }

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 2000,
    // Note: thinking param (extended thinking) requires SDK >= 0.28.0 with thinking support
    // For SDK compatibility, it's optional; adaptive thinking is enabled by default in Opus 4.8
    system: systemPrompt,
    messages: [{ role: "user", content: userPrompt }],
  });

  // Extract JSON from response
  let jsonText = "";
  for (const block of response.content) {
    if (block.type === "text") {
      jsonText = block.text;
      break;
    }
  }

  // Parse and validate
  let parsed;
  try {
    parsed = JSON.parse(jsonText);
  } catch (e) {
    console.error("Failed to parse Claude response as JSON:", jsonText.substring(0, 200));
    throw new Error(`Invalid JSON in Claude response: ${e.message}`);
  }

  // Clamp scores to 0-10 range
  if (parsed.distribution !== undefined)
    parsed.distribution = Math.max(0, Math.min(10, parsed.distribution));
  if (parsed.craft !== undefined)
    parsed.craft = Math.max(0, Math.min(10, parsed.craft));
  if (parsed.substance !== undefined)
    parsed.substance = Math.max(0, Math.min(10, parsed.substance));
  if (parsed.spec_compliance !== undefined)
    parsed.spec_compliance = Math.max(0, Math.min(10, parsed.spec_compliance));
  if (parsed.overall !== undefined)
    parsed.overall = Math.max(0, Math.min(10, parsed.overall));

  if (!validateSchema(parsed, outputSchema)) {
    throw new Error("Scorecard does not match schema");
  }

  return parsed;
}

// ============================================================================
// File I/O
// ============================================================================

/**
 * Ensure directory exists, create if not
 * @param {string} dirPath
 */
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * Save a scorecard to JSON
 * @param {string} round
 * @param {string} claimId
 * @param {SubmissionScorecard} scorecard
 */
function saveScorecard(round, claimId, scorecard) {
  const scorecardDir = path.join(REPO_ROOT, "data/scorecards", round);
  ensureDir(scorecardDir);

  const filePath = path.join(scorecardDir, `${claimId}.json`);
  fs.writeFileSync(filePath, JSON.stringify(scorecard, null, 2));
  console.log(`  Saved: ${filePath}`);
}

/**
 * Save cohort synthesis to JSON
 * @param {string} round
 * @param {CohortSynthesis} synthesis
 */
function saveSynthesis(round, synthesis) {
  const synthesisDir = path.join(REPO_ROOT, "data/scorecards", round);
  ensureDir(synthesisDir);

  const filePath = path.join(synthesisDir, "_synthesis.json");
  fs.writeFileSync(filePath, JSON.stringify(synthesis, null, 2));
  console.log(`  Saved: ${filePath}`);
}

// ============================================================================
// Secret Hygiene: Pre-commit scan
// ============================================================================

/**
 * Scan a string for exposed secrets
 * @param {string} text
 * @returns {boolean} true if secrets found
 */
function hasSuspiciousSecrets(text) {
  // 64-char hex (private keys)
  if (/[0-9a-fA-F]{64}/.test(text)) return true;
  // Anthropic SDK key
  if (/sk-ant-[A-Za-z0-9_-]{20,}/.test(text)) return true;
  // ANTHROPIC_API_KEY= followed by a value (not just the env var name)
  if (/ANTHROPIC_API_KEY=[^"'\s]/.test(text)) return true;
  return false;
}

// ============================================================================
// Main
// ============================================================================

async function main() {
  console.log(`\n=== Fable Eval Runner ===`);
  console.log(`Round: ${targetRound}`);
  if (targetClaim) console.log(`Target Claim: ${targetClaim}`);
  console.log(`Dry Run: ${dryRun}`);
  console.log();

  try {
    // Load data
    console.log("Loading submissions...");
    let submissions = loadSubmissions(targetRound);
    const description = loadDescription(targetRound);
    const floorRules = loadFloorRules(targetRound);

    console.log(
      `Loaded ${submissions.length} submissions from ${targetRound}`
    );

    // Filter to specific claim if requested
    if (targetClaim) {
      submissions = submissions.filter((s) => s.claim_id.toString() === targetClaim);
      if (submissions.length === 0) {
        throw new Error(`Claim ${targetClaim} not found in ${targetRound}`);
      }
    }

    // Score each submission
    console.log(`\nScoring ${submissions.length} submission(s)...`);
    /** @type {SubmissionScorecard[]} */
    const scorecards = [];

    for (const submission of submissions) {
      console.log(
        `\n  Claim ${submission.claim_id} (${submission.fc_handle})...`
      );

      const userPrompt = buildSubmissionPrompt(
        submission,
        description,
        floorRules
      );

      let scorecard;
      if (dryRun) {
        console.log(`    [DRY RUN] Generating stub scorecard...`);
        scorecard = generateStubScorecard(submission);
      } else {
        console.log(`    Calling Claude (Opus 4.8)...`);
        scorecard = await callClaude(
          RUBRIC_SYSTEM_PROMPT,
          userPrompt,
          SCORECARD_SCHEMA
        );
      }

      // Clamp scores one more time for safety
      scorecard.distribution = Math.max(
        0,
        Math.min(10, scorecard.distribution)
      );
      scorecard.craft = Math.max(0, Math.min(10, scorecard.craft));
      scorecard.substance = Math.max(0, Math.min(10, scorecard.substance));
      scorecard.spec_compliance = Math.max(
        0,
        Math.min(10, scorecard.spec_compliance)
      );
      scorecard.overall = Math.max(0, Math.min(10, scorecard.overall));

      const submissionScorecard = {
        claimId: submission.claim_id.toString(),
        round: targetRound,
        wallet: submission.wallet,
        fcHandle: submission.fc_handle,
        submissionUrl: submission.x_url,
        model: dryRun ? "stub" : "claude-opus-4-8",
        generatedAt: new Date().toISOString(),
        score: scorecard,
      };

      scorecards.push(submissionScorecard);

      // Save individual scorecard
      saveScorecard(targetRound, submission.claim_id.toString(), submissionScorecard);
    }

    // Generate cohort synthesis
    console.log(`\nGenerating cohort synthesis...`);
    let synthesis;
    if (dryRun) {
      console.log(`  [DRY RUN] Generating stub synthesis...`);
      synthesis = generateStubSynthesis(scorecards);
    } else {
      console.log(`  Calling Claude for synthesis...`);
      const cohortPrompt = buildCohortPrompt(scorecards);
      synthesis = await callClaude(
        "You are a research synthesis expert. Analyze the submitted scorecards and provide insights.",
        cohortPrompt,
        COHORT_SCHEMA
      );
    }

    const fullSynthesis = {
      round: targetRound,
      submissionCount: scorecards.length,
      averageScores: {
        distribution:
          scorecards.reduce((sum, sc) => sum + sc.score.distribution, 0) /
          scorecards.length,
        craft:
          scorecards.reduce((sum, sc) => sum + sc.score.craft, 0) /
          scorecards.length,
        substance:
          scorecards.reduce((sum, sc) => sum + sc.score.substance, 0) /
          scorecards.length,
        spec_compliance:
          scorecards.reduce((sum, sc) => sum + sc.score.spec_compliance, 0) /
          scorecards.length,
        overall:
          scorecards.reduce((sum, sc) => sum + sc.score.overall, 0) /
          scorecards.length,
      },
      floorPassRate:
        synthesis.floor_pass_rate || `${scorecards.filter((sc) => sc.score.floor_pass).length}/${scorecards.length}`,
      standouts: synthesis.standouts || [],
      patterns: synthesis.patterns || [],
      model: dryRun ? "stub" : "claude-opus-4-8",
      generatedAt: new Date().toISOString(),
    };

    // Save synthesis
    saveSynthesis(targetRound, fullSynthesis);

    // Secret hygiene check
    console.log(`\nRunning secret hygiene scan...`);
    let foundSecrets = false;
    for (const sc of scorecards) {
      if (hasSuspiciousSecrets(JSON.stringify(sc))) {
        console.error(`  BLOCK: Suspicious secret pattern in scorecard ${sc.claimId}`);
        foundSecrets = true;
      }
    }
    if (foundSecrets) {
      process.exit(1);
    }
    console.log(`  OK: No suspicious patterns detected`);

    console.log(`\n=== Evaluation Complete ===`);
    console.log(`Scorecards: ${scorecards.length}`);
    console.log(`Floor Pass Rate: ${fullSynthesis.floorPassRate}`);
    console.log(`Average Overall Score: ${fullSynthesis.averageScores.overall.toFixed(1)}/10`);
    console.log();
  } catch (error) {
    console.error(`\nError: ${error.message}`);
    if (error.stack) console.error(error.stack);
    process.exit(1);
  }
}

main();
