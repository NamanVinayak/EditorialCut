import type {Rect} from "./layout";

export type TypeRole =
  | "attention"
  | "identity"
  | "editorial"
  | "annotation"
  | "utility";
export type TypeTreatment =
  | "identity_lockup"
  | "hero_field"
  | "thesis_build"
  | "editorial_note"
  | "support_overlay";
export type TypeScale = "support" | "feature" | "environmental";
export type TypeDepth = "front" | "rear" | "mixed" | "screen";
export type TypePlacement = "left" | "right" | "lower-left" | "center";

export interface RoleFontMap {
  display: string;
  kicker: string;
  quote: string;
  caption: string;
  attention?: string;
  identity?: string;
  editorial?: string;
  annotation?: string;
  utility?: string;
}

export interface TreatmentBox {
  left: number;
  top: number;
  width: number;
  height: number;
  textAlign: "left" | "center" | "right";
}

export const resolveTypeFont = (
  fonts: RoleFontMap,
  role: TypeRole,
): string => {
  switch (role) {
    case "attention":
      return fonts.attention ?? fonts.display;
    case "identity":
      return fonts.identity ?? fonts.display;
    case "editorial":
      return fonts.editorial ?? fonts.quote;
    case "annotation":
      return fonts.annotation ?? fonts.quote;
    case "utility":
      return fonts.utility ?? fonts.kicker;
  }
};

export const treatmentLayers = (
  depth: TypeDepth,
): Array<"rear" | "front"> => {
  if (depth === "rear") return ["rear"];
  if (depth === "mixed") return ["rear", "front"];
  return ["front"];
};

export const treatmentWhiteSpace = (
  treatment: TypeTreatment,
): "nowrap" | "pre-line" =>
  treatment === "hero_field" ? "nowrap" : "pre-line";

const boxDimensions = (
  treatment: TypeTreatment,
  frameWidth: number,
  frameHeight: number,
  placement: TypePlacement,
): {width: number; height: number} => {
  switch (treatment) {
    case "hero_field":
      return {width: frameWidth, height: frameHeight * 0.72};
    case "thesis_build":
      return {
        width:
          placement === "left" || placement === "right"
            ? frameWidth * 0.54
            : frameWidth * 0.76,
        height: frameHeight * 0.62,
      };
    case "identity_lockup":
      return {
        width: Math.min(
          900,
          frameWidth *
            (placement === "left" || placement === "right" ? 0.58 : 0.64),
        ),
        height: frameHeight * 0.42,
      };
    case "editorial_note":
      return {width: frameWidth * 0.58, height: frameHeight * 0.38};
    case "support_overlay":
      return {width: frameWidth * 0.56, height: frameHeight * 0.42};
  }
};

export const treatmentBox = (
  treatment: TypeTreatment,
  safe: Rect,
  placement: TypePlacement = "right",
): TreatmentBox => {
  const frameWidth = safe.right - safe.left;
  const frameHeight = safe.bottom - safe.top;
  const {width, height} = boxDimensions(
    treatment,
    frameWidth,
    frameHeight,
    placement,
  );

  const centerLeft = safe.left + (frameWidth - width) / 2;
  const rightLeft = safe.right - width;
  const lowerTop = safe.bottom - height;
  const centerTop = safe.top + (frameHeight - height) / 2;

  switch (placement) {
    case "left":
      return {left: safe.left, top: centerTop, width, height, textAlign: "left"};
    case "lower-left":
      return {left: safe.left, top: lowerTop, width, height, textAlign: "left"};
    case "center":
      return {left: centerLeft, top: centerTop, width, height, textAlign: "center"};
    case "right":
      return {
        left: rightLeft,
        top: centerTop,
        width,
        height,
        textAlign:
          treatment === "identity_lockup" || treatment === "thesis_build"
            ? "right"
            : "left",
      };
  }
};

export const treatmentFontSize = (
  treatment: TypeTreatment,
  scale: TypeScale,
  text: string,
  boxWidth: number,
): number => {
  const base = {
    identity_lockup: 112,
    hero_field: 220,
    thesis_build: 116,
    editorial_note: 76,
    support_overlay: 66,
  }[treatment];
  const scaleMultiplier = {
    support: 0.8,
    feature: 1,
    environmental: 1.2,
  }[scale];
  const longestLine = Math.max(
    1,
    ...text.split("\n").map((line) => line.trim().length),
  );
  const approximateCharacterWidth =
    treatment === "hero_field" ? 0.7 : 0.58;
  const approximateFit =
    boxWidth / (longestLine * approximateCharacterWidth);
  return Math.max(32, Math.min(base * scaleMultiplier, approximateFit));
};
