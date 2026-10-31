import assert from "node:assert/strict";
import test from "node:test";

import {validateEditData} from "./check-edit-data.mjs";

const validCaptions = {
  words: [
    {t: 0, e: 0.3, w: "one"},
    {t: 0.36, e: 0.7, w: "two"},
  ],
};

const legacyBeat = {
  id: "legacy",
  start_s: 0,
  end_s: 2,
  spatial_mode: "overlay",
  presenter_role: "anchor",
  render: "overlay_accent",
  camera_template_id: null,
  is_effect_moment: true,
  plate: "legacy",
  content: {
    lines: [{text: "LEGACY", at: 0.2}],
  },
  reason: "Legacy compatibility fixture",
};

const designDefaults = {
  job: "thesis",
  type_role: "attention",
  scale: "feature",
  depth: "front",
  readability: "full",
  edge_policy: "contain",
};

const typeBeat = (design = {}, treatment = "thesis_build") => ({
  id: "type",
  start_s: 0,
  end_s: 2,
  spatial_mode: "overlay",
  presenter_role: "cutout",
  render: "type_treatment",
  camera_template_id: null,
  is_effect_moment: true,
  plate: "type",
  cutout: "type",
  design: {...designDefaults, ...design},
  content: {
    treatment,
    lines: [{text: "A THESIS", at: 0.2}],
  },
  reason: "Role-aware typography fixture",
});

const editWith = (...beats) => ({
  edit_slug: "fixture",
  fps: 30,
  width: 1920,
  height: 1080,
  beats: beats.map((beat, index) => ({
    ...beat,
    start_s: index * 2,
    end_s: index * 2 + 2,
  })),
});

test("fails identity text that is not fully readable", () => {
  const result = validateEditData({
    edit: editWith(typeBeat({job: "identity", readability: "recoverable"})),
    captions: validCaptions,
  });

  assert.match(result.failures.join("\n"), /identity.*readability.*full/i);
});

test("allows controlled rear environmental transformation text", () => {
  const result = validateEditData({
    edit: editWith(
      typeBeat(
        {
          job: "transformation",
          scale: "environmental",
          depth: "rear",
          readability: "recoverable",
        },
        "hero_field",
      ),
    ),
    captions: validCaptions,
  });

  assert.deepEqual(result.failures, []);
});

test("warns instead of failing on three repeated nearby treatment signatures", () => {
  const beat = typeBeat({job: "thesis"});
  const result = validateEditData({
    edit: editWith(
      {...beat, id: "a"},
      {...beat, id: "b"},
      {...beat, id: "c"},
    ),
    captions: validCaptions,
  });

  assert.equal(result.failures.length, 0);
  assert.match(result.warnings.join("\n"), /repeated treatment signature/i);
});

test("fails an impossible single-word duration", () => {
  const result = validateEditData({
    edit: editWith(legacyBeat),
    captions: {words: [{t: 0, e: 7, w: "stuck"}]},
  });

  assert.match(result.failures.join("\n"), /7\.000s/);
});

test("warns on a suspicious but not impossible single-word duration", () => {
  const result = validateEditData({
    edit: editWith(legacyBeat),
    captions: {words: [{t: 0, e: 3.4, w: "stretched"}]},
  });

  assert.equal(result.failures.length, 0);
  assert.match(result.warnings.join("\n"), /3\.400s/);
});

test("fails unsorted caption timings", () => {
  const result = validateEditData({
    edit: editWith(legacyBeat),
    captions: {
      words: [
        {t: 1, e: 1.4, w: "one"},
        {t: 0.5, e: 0.9, w: "two"},
      ],
    },
  });

  assert.match(result.failures.join("\n"), /not sorted/i);
});

test("fails caption overlaps greater than fifty milliseconds", () => {
  const result = validateEditData({
    edit: editWith(legacyBeat),
    captions: {
      words: [
        {t: 0, e: 1, w: "one"},
        {t: 0.8, e: 1.2, w: "two"},
      ],
    },
  });

  assert.match(result.failures.join("\n"), /overlaps/i);
});

test("allows a valid pause between caption words", () => {
  const result = validateEditData({
    edit: editWith(legacyBeat),
    captions: {
      words: [
        {t: 0, e: 0.4, w: "one"},
        {t: 2, e: 2.3, w: "two"},
      ],
    },
  });

  assert.deepEqual(result.failures, []);
});

test("fails Devanagari caption text", () => {
  const result = validateEditData({
    edit: editWith(legacyBeat),
    captions: {words: [{t: 0, e: 0.4, w: "लगता"}]},
  });

  assert.match(result.failures.join("\n"), /Devanagari/i);
});

test("accepts a legacy overlay accent beat without design data", () => {
  const result = validateEditData({
    edit: editWith(legacyBeat),
    captions: validCaptions,
  });

  assert.deepEqual(result.failures, []);
});

test("fails an unknown type treatment", () => {
  const result = validateEditData({
    edit: editWith(typeBeat({}, "random_template")),
    captions: validCaptions,
  });

  assert.match(result.failures.join("\n"), /unknown type treatment/i);
});

test("fails mixed depth without explicit rear and front text pieces", () => {
  const result = validateEditData({
    edit: editWith(typeBeat({depth: "mixed"})),
    captions: validCaptions,
  });

  assert.match(result.failures.join("\n"), /mixed depth.*rear.*front/i);
});

test("allows mixed depth with explicit rear and front text pieces", () => {
  const beat = typeBeat({depth: "mixed"});
  beat.content.lines = [
    {text: "BEHIND", at: 0.2, layer: "rear"},
    {text: "IN FRONT", at: 0.8, layer: "front"},
  ];
  const result = validateEditData({
    edit: editWith(beat),
    captions: validCaptions,
  });

  assert.deepEqual(result.failures, []);
});
