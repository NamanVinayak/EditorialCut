import React from "react";
import {AbsoluteFill} from "remotion";
import lookData from "../../public/edit/look.json";
import {Captions, LookCtx} from "../kit/parts";
import {TypeTreatmentBeat} from "../kit/typography";
import type {Beat, CaptionDoc, LookTokens} from "../kit/types";

const look = lookData as LookTokens;

const identityBeat: Beat = {
  id: "identity-proof",
  start_s: 0,
  end_s: 4,
  spatial_mode: "overlay",
  presenter_role: "cutout",
  render: "type_treatment",
  camera_template_id: null,
  is_effect_moment: true,
  plate: "b03",
  cutout: "b03",
  design: {
    job: "identity",
    type_role: "identity",
    scale: "feature",
    depth: "front",
    readability: "full",
    edge_policy: "contain",
  },
  content: {
    treatment: "identity_lockup",
    kicker: "CASE STUDY",
    title: "SAMPLE\nPRESENTER",
    placement: "right",
  },
  reason: "Identity must remain fully readable",
};

const heroFieldBeat: Beat = {
  id: "hero-field-proof",
  start_s: 0,
  end_s: 5,
  spatial_mode: "overlay",
  presenter_role: "cutout",
  render: "type_treatment",
  camera_template_id: null,
  is_effect_moment: true,
  plate: "b04",
  cutout: "b04",
  design: {
    job: "transformation",
    type_role: "attention",
    scale: "environmental",
    depth: "rear",
    readability: "recoverable",
    edge_policy: "contain",
  },
  content: {
    treatment: "hero_field",
    placement: "center",
    lines: [{text: "BEFORE → AFTER", tone: "neg", at: 0.4}],
  },
  reason: "Transformation becomes a large environmental statement",
};

const thesisBeat: Beat = {
  id: "thesis-proof",
  start_s: 0,
  end_s: 6.5,
  spatial_mode: "overlay",
  presenter_role: "cutout",
  render: "type_treatment",
  camera_template_id: "T2",
  is_effect_moment: true,
  plate: "b05",
  cutout: "b05",
  design: {
    job: "thesis",
    type_role: "attention",
    scale: "feature",
    depth: "front",
    readability: "full",
    edge_policy: "contain",
  },
  content: {
    treatment: "thesis_build",
    placement: "right",
    lines: [
      {text: "CONFLICT", tone: "paper", at: 0.5},
      {text: "→ DRAMA", tone: "neg", at: 1.2},
    ],
  },
  reason: "The thesis remains inside the shared safe region during the push",
};

const captionGap: CaptionDoc = {
  words: [
    {t: 0.15, e: 0.45, w: "caption"},
    {t: 2, e: 2.35, w: "returns"},
  ],
};

const WithLook: React.FC<{children: React.ReactNode}> = ({children}) => (
  <LookCtx.Provider value={look}>{children}</LookCtx.Provider>
);

export const IdentityProof: React.FC = () => (
  <WithLook>
    <TypeTreatmentBeat beat={identityBeat} />
  </WithLook>
);

export const HeroFieldProof: React.FC = () => (
  <WithLook>
    <TypeTreatmentBeat beat={heroFieldBeat} />
  </WithLook>
);

export const ThesisCameraProof: React.FC = () => (
  <WithLook>
    <TypeTreatmentBeat beat={thesisBeat} />
  </WithLook>
);

export const CaptionGapProof: React.FC = () => (
  <WithLook>
    <AbsoluteFill
      style={{
        background: look.surface,
        color: look.meta,
        alignItems: "center",
        justifyContent: "center",
        fontFamily: look.fonts.utility ?? look.fonts.kicker,
        fontSize: 28,
        letterSpacing: 3,
      }}
    >
      CAPTION GAP PROOF
      <Captions doc={captionGap} />
    </AbsoluteFill>
  </WithLook>
);
