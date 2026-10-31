#!/usr/bin/env node

import fs from "node:fs";
import {pathToFileURL} from "node:url";

const TYPE_TREATMENTS = new Set([
  "identity_lockup",
  "hero_field",
  "thesis_build",
  "editorial_note",
  "support_overlay",
]);
const JOBS = new Set([
  "identity",
  "transformation",
  "thesis",
  "comparison",
  "evidence",
  "quote",
  "annotation",
  "utility",
  "atmosphere",
]);
const TYPE_ROLES = new Set([
  "attention",
  "identity",
  "editorial",
  "annotation",
  "utility",
]);
const SCALES = new Set(["support", "feature", "environmental"]);
const DEPTHS = new Set(["front", "rear", "mixed", "screen"]);
const READABILITY = new Set(["full", "recoverable", "decorative"]);
const EDGE_POLICIES = new Set(["contain", "intentional_crop"]);
const FULL_READ_JOBS = new Set(["identity", "evidence", "utility"]);
const SEMANTIC_JOBS = new Set([
  "identity",
  "transformation",
  "thesis",
  "comparison",
  "evidence",
  "quote",
  "utility",
]);
const DEVANAGARI = /[\u0900-\u097f]/u;

const requireEnum = (failures, beatId, design, field, allowed) => {
  const value = design?.[field];
  if (!allowed.has(value)) {
    failures.push(
      `beat ${beatId}: design.${field} '${String(value)}' is invalid; expected one of ${[
        ...allowed,
      ].join(", ")}`,
    );
  }
};

const validateTypeBeat = (beat, failures) => {
  const beatId = beat.id ?? "<no-id>";
  const treatment = beat.content?.treatment;
  if (!TYPE_TREATMENTS.has(treatment)) {
    failures.push(
      `beat ${beatId}: unknown type treatment '${String(treatment)}'; expected one of ${[
        ...TYPE_TREATMENTS,
      ].join(", ")}`,
    );
  }

  const design = beat.design;
  if (!design || typeof design !== "object") {
    failures.push(`beat ${beatId}: render type_treatment requires a design object`);
    return;
  }

  requireEnum(failures, beatId, design, "job", JOBS);
  requireEnum(failures, beatId, design, "type_role", TYPE_ROLES);
  requireEnum(failures, beatId, design, "scale", SCALES);
  requireEnum(failures, beatId, design, "depth", DEPTHS);
  requireEnum(failures, beatId, design, "readability", READABILITY);
  requireEnum(failures, beatId, design, "edge_policy", EDGE_POLICIES);

  if (FULL_READ_JOBS.has(design.job) && design.readability !== "full") {
    failures.push(
      `beat ${beatId}: ${design.job} text requires design.readability 'full', received '${String(
        design.readability,
      )}'`,
    );
  }
  if (SEMANTIC_JOBS.has(design.job) && design.readability === "decorative") {
    failures.push(
      `beat ${beatId}: semantic job '${design.job}' cannot use decorative readability`,
    );
  }
  if (
    design.edge_policy === "intentional_crop" &&
    (design.scale !== "environmental" || design.readability !== "recoverable")
  ) {
    failures.push(
      `beat ${beatId}: intentional_crop requires environmental scale and recoverable readability`,
    );
  }
  if (design.depth === "mixed") {
    const layers = new Set(
      (beat.content?.lines ?? []).map((line) => line?.layer).filter(Boolean),
    );
    if (!layers.has("rear") || !layers.has("front")) {
      failures.push(
        `beat ${beatId}: mixed depth requires explicit rear and front text pieces`,
      );
    }
  }
};

const treatmentSignature = (beat) => {
  if (beat.render !== "type_treatment") return null;
  const design = beat.design ?? {};
  return [
    beat.content?.treatment,
    design.type_role,
    design.scale,
    design.depth,
  ].join("|");
};

const validateRepetition = (beats, warnings) => {
  let run = [];
  let signature = null;

  const flush = () => {
    if (signature && run.length >= 3) {
      warnings.push(
        `repeated treatment signature '${signature}' across nearby beats ${run
          .map((beat) => beat.id)
          .join(", ")}; director must confirm the repetition is intentional`,
      );
    }
    run = [];
    signature = null;
  };

  for (const beat of beats) {
    const nextSignature = treatmentSignature(beat);
    const previous = run.at(-1);
    const nearby =
      previous && Number(beat.start_s) - Number(previous.end_s) <= 30;
    if (!nextSignature || nextSignature !== signature || !nearby) {
      flush();
    }
    if (nextSignature) {
      signature = nextSignature;
      run.push(beat);
    }
  }
  flush();
};

const validateCaptions = (captions, failures, warnings) => {
  const words = captions?.words;
  if (!Array.isArray(words)) {
    failures.push("captions.words must be an array");
    return;
  }

  for (let index = 0; index < words.length; index += 1) {
    const word = words[index] ?? {};
    const label = `caption word ${index} '${String(word.w ?? "")}'`;
    const start = Number(word.t);
    const end = Number(word.e);
    if (!Number.isFinite(start) || !Number.isFinite(end)) {
      failures.push(`${label}: t and e must be finite numbers`);
      continue;
    }
    if (end < start) {
      failures.push(`${label}: end ${end} precedes start ${start}`);
      continue;
    }
    if (DEVANAGARI.test(String(word.w ?? ""))) {
      failures.push(`${label}: contains Devanagari; rendered Hindi must be Hinglish`);
    }

    const duration = end - start;
    const durationMessage = `${label}: duration ${duration.toFixed(3)}s (${start.toFixed(
      3,
    )}–${end.toFixed(3)})`;
    if (duration > 6) {
      failures.push(`${durationMessage} exceeds the 6.000s impossible-word limit`);
    } else if (duration > 3) {
      warnings.push(`${durationMessage} exceeds the 3.000s suspicion threshold`);
    }

    if (index === 0) continue;
    const previous = words[index - 1];
    const previousStart = Number(previous.t);
    const previousEnd = Number(previous.e);
    if (start < previousStart) {
      failures.push(
        `${label}: timings are not sorted (${start.toFixed(3)} < ${previousStart.toFixed(
          3,
        )})`,
      );
    }
    if (Number.isFinite(previousEnd) && previousEnd - start > 0.05) {
      failures.push(
        `${label}: overlaps previous word by ${(previousEnd - start).toFixed(
          3,
        )}s, above the 0.050s limit`,
      );
    }
  }
};

export const validateEditData = ({edit, captions}) => {
  const failures = [];
  const warnings = [];
  const beats = edit?.beats;
  if (!Array.isArray(beats) || beats.length === 0) {
    failures.push("edit.beats must be a non-empty array");
  } else {
    for (const beat of beats) {
      if (beat?.render === "type_treatment") {
        validateTypeBeat(beat, failures);
      }
    }
    validateRepetition(beats, warnings);
  }
  validateCaptions(captions, failures, warnings);
  return {failures, warnings};
};

const loadJson = (path) => JSON.parse(fs.readFileSync(path, "utf8"));

const main = () => {
  const [editPath, captionsPath] = process.argv.slice(2);
  if (!editPath || !captionsPath) {
    console.error(
      "usage: node scripts/check-edit-data.mjs <beat-map.json> <captions.json>",
    );
    process.exit(2);
  }

  let edit;
  let captions;
  try {
    edit = loadJson(editPath);
    captions = loadJson(captionsPath);
  } catch (error) {
    console.error(`ERROR: ${error instanceof Error ? error.message : String(error)}`);
    process.exit(2);
  }

  const result = validateEditData({edit, captions});
  console.log(
    `edit-data preflight: ${editPath} + ${captionsPath}`,
  );
  for (const warning of result.warnings) console.log(`WARN: ${warning}`);
  for (const failure of result.failures) console.error(`FAIL: ${failure}`);
  console.log(
    result.failures.length
      ? `RESULT: FAIL (${result.failures.length} failure(s), ${result.warnings.length} warning(s))`
      : `RESULT: PASS (${result.warnings.length} warning(s))`,
  );
  process.exit(result.failures.length ? 1 : 0);
};

if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(process.argv[1]).href
) {
  main();
}
