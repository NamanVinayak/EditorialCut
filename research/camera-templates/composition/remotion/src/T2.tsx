import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile } from "remotion";
import { CameraViewport } from "./camera";
import { getCameraLegs } from "./templateRegistry";

// Version 2: one emphasis push and its motivated return, with no later push.
const LEGS = getCameraLegs("emphasis-push");

export const T2: React.FC = () => (
  <AbsoluteFill>
    <CameraViewport legs={LEGS}>
      <OffthreadVideo src={staticFile("excerpt.mp4")} style={{ width: 1920, height: 1080 }} />
    </CameraViewport>
  </AbsoluteFill>
);
