import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile } from "remotion";
import { CameraViewport } from "./camera";
import { getCameraLegs } from "./templateRegistry";

// Version 2: one reveal-out action, then the camera remains neutral.
const LEGS = getCameraLegs("reveal-out");

export const T1: React.FC = () => (
  <AbsoluteFill>
    <CameraViewport legs={LEGS}>
      <OffthreadVideo src={staticFile("excerpt.mp4")} style={{ width: 1920, height: 1080 }} />
    </CameraViewport>
  </AbsoluteFill>
);
