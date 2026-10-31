import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile } from "remotion";
import { CameraViewport, CameraLeg } from "./camera";

// Treatment T5 — implement EXACTLY per SPECS.md section "T5".
// Replace LEGS with the spec's schedule. Do not modify camera.tsx or Root.tsx.
// The whip releases to exactly 1.0. A sub-1.0 target would expose canvas
// because the sampled viewport would be larger than the source frame.
const LEGS: CameraLeg[] = [
  {
    t0: 2.64,
    t1: 2.707,
    scale: [1.0, 1.12],
    cx: [960, 970],
    cy: [540, 500],
    ease: "snap",
  },
  {
    t0: 4.36,
    t1: 4.427,
    scale: [1.12, 1.24],
    cx: [970, 980],
    cy: [500, 450],
    ease: "snap",
  },
  {
    t0: 5.94,
    t1: 6.007,
    scale: [1.24, 1.36],
    cx: [980, 985],
    cy: [450, 410],
    ease: "snap",
  },
  {
    t0: 7.74,
    t1: 7.94,
    scale: [1.36, 1.0],
    cx: [985, 960],
    cy: [410, 540],
    ease: "easeOut",
  },
  {
    t0: 8.98,
    t1: 9.047,
    scale: [1.0, 1.15],
    cx: [960, 985],
    cy: [540, 430],
    ease: "snap",
  },
];

export const T5: React.FC = () => (
  <AbsoluteFill>
    <CameraViewport legs={LEGS}>
      <OffthreadVideo src={staticFile("excerpt.mp4")} style={{ width: 1920, height: 1080 }} />
    </CameraViewport>
  </AbsoluteFill>
);
