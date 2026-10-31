import React from "react";
import { Composition } from "remotion";
import { FullVideo, editMeta } from "./FullVideo";
import {
  CaptionGapProof,
  HeroFieldProof,
  IdentityProof,
  ThesisCameraProof,
} from "./proofs/EditorialTreatmentProof";

// Total duration = last beat end. The executor renders this ONE composition.
const totalFrames = Math.max(...editMeta.beats.map((b) => Math.round(b.end_s * editMeta.fps)));

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="FullVideo"
      component={FullVideo}
      durationInFrames={totalFrames}
      fps={editMeta.fps}
      width={editMeta.width}
      height={editMeta.height}
    />
    <Composition
      id="EditorialIdentityProof"
      component={IdentityProof}
      durationInFrames={120}
      fps={30}
      width={1920}
      height={1080}
    />
    <Composition
      id="EditorialHeroFieldProof"
      component={HeroFieldProof}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
    />
    <Composition
      id="EditorialThesisCameraProof"
      component={ThesisCameraProof}
      durationInFrames={195}
      fps={30}
      width={1920}
      height={1080}
    />
    <Composition
      id="EditorialCaptionGapProof"
      component={CaptionGapProof}
      durationInFrames={90}
      fps={30}
      width={1920}
      height={1080}
    />
  </>
);
