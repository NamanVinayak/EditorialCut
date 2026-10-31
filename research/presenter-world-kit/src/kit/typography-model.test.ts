import {
  resolveTypeFont,
  treatmentBox,
  treatmentFontSize,
  treatmentLayers,
  treatmentWhiteSpace,
} from "./typography-model";

const fail = (message: string): never => {
  throw new Error(message);
};

const assert = (condition: boolean, message: string) => {
  if (!condition) fail(message);
};

const assertEqual = <T>(actual: T, expected: T, message: string) => {
  if (actual !== expected) {
    fail(`${message}: expected ${String(expected)}, received ${String(actual)}`);
  }
};

const fonts = {
  display: "Display",
  kicker: "Kicker",
  quote: "Quote",
  caption: "Caption",
  attention: "Attention",
  identity: "Identity",
  editorial: "Editorial",
  annotation: "Annotation",
  utility: "Utility",
};

assertEqual(
  resolveTypeFont(fonts, "attention"),
  "Attention",
  "attention role uses its derived font",
);
assertEqual(
  resolveTypeFont(
    {
      display: "Display",
      kicker: "Kicker",
      quote: "Quote",
      caption: "Caption",
    },
    "annotation",
  ),
  "Quote",
  "legacy look falls back from annotation to quote",
);
assertEqual(
  resolveTypeFont(
    {
      display: "Display",
      kicker: "Kicker",
      quote: "Quote",
      caption: "Caption",
    },
    "utility",
  ),
  "Kicker",
  "legacy look falls back from utility to kicker",
);

assertEqual(
  treatmentLayers("rear").join(","),
  "rear",
  "rear design renders behind the presenter",
);
assertEqual(
  treatmentLayers("front").join(","),
  "front",
  "front design renders above the presenter",
);
assertEqual(
  treatmentLayers("mixed").join(","),
  "rear,front",
  "mixed design renders explicit rear and front pieces",
);

const safe = {left: 300, top: 140, right: 1700, bottom: 900};
for (const treatment of [
  "identity_lockup",
  "hero_field",
  "thesis_build",
  "editorial_note",
  "support_overlay",
] as const) {
  const box = treatmentBox(treatment, safe, "right");
  assert(box.left >= safe.left, `${treatment} begins inside the safe rectangle`);
  assert(
    box.left + box.width <= safe.right,
    `${treatment} ends inside the safe rectangle`,
  );
  assert(box.top >= safe.top, `${treatment} begins below the safe top`);
  assert(
    box.top + box.height <= safe.bottom,
    `${treatment} ends above the safe bottom`,
  );
}
assertEqual(
  treatmentBox("identity_lockup", safe, "right").textAlign,
  "right",
  "right-side identity text aligns away from a central presenter",
);
assertEqual(
  treatmentBox("thesis_build", safe, "right").textAlign,
  "right",
  "right-side thesis text aligns into the available outer third",
);
assert(
  treatmentBox("thesis_build", safe, "right").width <=
    (safe.right - safe.left) * 0.58,
  "right-side thesis reserves the central presenter region",
);

const heroSize = treatmentFontSize(
  "hero_field",
  "environmental",
  "HERO → ZERO",
  1400,
);
const identitySize = treatmentFontSize(
  "identity_lockup",
  "feature",
  "SAMPLE PRESENTER",
  900,
);
const supportSize = treatmentFontSize(
  "support_overlay",
  "support",
  "A SUPPORTING POINT",
  700,
);
assert(heroSize > identitySize, "hero field is larger than an identity lockup");
assert(identitySize > supportSize, "identity lockup is larger than support text");
assert(heroSize >= 180, "environmental hero type is genuinely oversized");
assert(
  treatmentFontSize(
    "hero_field",
    "environmental",
    "HERO → ZERO",
    1920,
  ) <= 250,
  "hero field stays on one oversized line instead of wrapping behind the presenter",
);
assertEqual(
  treatmentWhiteSpace("hero_field"),
  "nowrap",
  "hero field preserves a single readable transformation phrase",
);

console.log("typography model tests: PASS");
