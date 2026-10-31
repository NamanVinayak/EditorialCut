import React from "react";
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from "remotion";
import {CameraViewport} from "./camera";
import {safeWorldRect} from "./layout";
import {getLegs} from "./registry";
import {
  Cutout,
  Plate,
  enterAt,
  toneColor,
  useLook,
} from "./parts";
import {
  resolveTypeFont,
  treatmentBox,
  treatmentFontSize,
  treatmentLayers,
  treatmentWhiteSpace,
} from "./typography-model";
import type {Rect} from "./layout";
import type {Beat, BeatContent, BeatDesign, Tone} from "./types";
import type {TypeRole, TypeTreatment} from "./typography-model";

const FULL_FRAME: Rect = {left: 0, top: 0, right: 1920, bottom: 1080};

const ArrowText: React.FC<{text: string; accent: string}> = ({
  text,
  accent,
}) => {
  const pieces = text.split(/(->|→)/g);
  return (
    <>
      {pieces.map((piece, index) =>
        piece === "->" || piece === "→" ? (
          <span key={`${piece}-${index}`} style={{color: accent}}>
            →
          </span>
        ) : (
          <React.Fragment key={`${piece}-${index}`}>{piece}</React.Fragment>
        ),
      )}
    </>
  );
};

interface TreatmentLine {
  text: string;
  tone?: Tone;
  at: number;
  role: TypeRole;
}

const treatmentLines = (
  content: BeatContent,
  design: BeatDesign,
  layer: "rear" | "front",
): TreatmentLine[] => {
  if (design.depth === "mixed") {
    return (content.lines ?? [])
      .filter((line) => line.layer === layer)
      .map((line, index) => ({
        text: line.text,
        tone: line.tone,
        at: line.at ?? 0.5 + index * 0.7,
        role: line.role ?? design.type_role,
      }));
  }

  const lines: TreatmentLine[] = [];
  if (content.kicker) {
    lines.push({
      text: content.kicker,
      tone: "accent",
      at: content.lines?.[0]?.at ?? 0.35,
      role: "utility",
    });
  }
  if (content.title) {
    lines.push({
      text: content.title,
      at: (content.lines?.[0]?.at ?? 0.35) + 0.18,
      role: design.type_role,
    });
  }
  for (const [index, line] of (content.lines ?? []).entries()) {
    lines.push({
      text: line.text,
      tone: line.tone,
      at: line.at ?? 0.6 + index * 0.8,
      role: line.role ?? design.type_role,
    });
  }
  if (content.subtitle) {
    lines.push({
      text: content.subtitle,
      tone: "meta",
      at: Math.max(0.9, ...lines.map((line) => line.at + 0.45)),
      role: "editorial",
    });
  }
  return lines;
};

const treatmentLineStyle = (
  treatment: TypeTreatment,
  role: TypeRole,
  fontSize: number,
): React.CSSProperties => {
  const editorial = role === "editorial" || role === "annotation";
  const utility = role === "utility";
  return {
    fontSize: utility ? Math.min(fontSize, 38) : fontSize,
    lineHeight: treatment === "hero_field" ? 0.86 : editorial ? 1.08 : 0.98,
    fontWeight: utility || editorial ? 500 : 800,
    fontStyle: editorial ? "italic" : "normal",
    letterSpacing:
      treatment === "hero_field" ? -5 : utility ? 3.5 : -1.5,
    textTransform: utility ? "uppercase" : "none",
    whiteSpace: treatmentWhiteSpace(treatment),
  };
};

const TypographyBlock: React.FC<{
  beat: Beat;
  layer: "rear" | "front";
  safe: Rect;
}> = ({beat, layer, safe}) => {
  const look = useLook();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const content = beat.content ?? {};
  const design = beat.design!;
  const treatment = content.treatment!;
  const box = treatmentBox(
    treatment,
    safe,
    treatment === "hero_field" ? "center" : content.placement,
  );
  const lines = treatmentLines(content, design, layer);
  const combinedText = lines.map((line) => line.text).join("\n");
  const baseSize = treatmentFontSize(
    treatment,
    design.scale,
    combinedText,
    box.width,
  );

  return (
    <div
      data-treatment={treatment}
      data-layer={layer}
      style={{
        position: "absolute",
        left: box.left,
        top: box.top,
        width: box.width,
        height: box.height,
        display: "flex",
        flexDirection: "column",
        justifyContent:
          treatment === "editorial_note" ? "flex-end" : "center",
        alignItems:
          box.textAlign === "center"
            ? "center"
            : box.textAlign === "right"
              ? "flex-end"
              : "flex-start",
        textAlign: box.textAlign,
        gap:
          treatment === "hero_field"
            ? 0
            : treatment === "thesis_build"
              ? 18
              : 12,
        transform:
          treatment === "editorial_note" ? "rotate(-1.5deg)" : undefined,
      }}
    >
      {lines.map((line, index) => {
        const entry = enterAt(frame, fps, line.at, treatment === "hero_field" ? 0.32 : 0.4);
        const fontSize =
          line.role === "utility"
            ? Math.min(38, baseSize * 0.38)
            : treatment === "thesis_build" && index > 0
              ? baseSize * 0.82
              : baseSize;
        return (
          <div
            key={`${layer}-${index}-${line.text}`}
            style={{
              opacity: entry.opacity,
              translate: `0 ${entry.ty}px`,
              color: toneColor(look, line.tone),
              fontFamily: resolveTypeFont(look.fonts, line.role),
              maxWidth: "100%",
              ...treatmentLineStyle(treatment, line.role, fontSize),
            }}
          >
            <ArrowText text={line.text} accent={look.accent} />
          </div>
        );
      })}
    </div>
  );
};

export const TypeTreatmentBeat: React.FC<{beat: Beat}> = ({beat}) => {
  const design = beat.design;
  const treatment = beat.content?.treatment;
  if (!design || !treatment) {
    throw new Error(
      `beat ${beat.id}: type_treatment requires design and content.treatment`,
    );
  }

  const legs = beat.camera_template_id
    ? getLegs(beat.camera_template_id)
    : [];
  const duration = Math.max(0, beat.end_s - beat.start_s);
  const safe =
    design.edge_policy === "contain"
      ? safeWorldRect(legs, duration)
      : FULL_FRAME;
  const layers = treatmentLayers(design.depth);
  const world = (
    <AbsoluteFill>
      <Plate name={beat.plate} />
      {design.depth !== "screen" && layers.includes("rear") ? (
        <TypographyBlock beat={beat} layer="rear" safe={safe} />
      ) : null}
      {beat.cutout ? <Cutout name={beat.cutout} /> : null}
      {design.depth !== "screen" && layers.includes("front") ? (
        <TypographyBlock beat={beat} layer="front" safe={safe} />
      ) : null}
    </AbsoluteFill>
  );

  return (
    <AbsoluteFill style={{background: "#000"}}>
      {legs.length ? (
        <CameraViewport legs={legs}>{world}</CameraViewport>
      ) : (
        world
      )}
      {design.depth === "screen" ? (
        <TypographyBlock beat={beat} layer="front" safe={safe} />
      ) : null}
    </AbsoluteFill>
  );
};
