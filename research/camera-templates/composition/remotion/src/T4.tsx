import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile } from "remotion";
import { CameraViewport } from "./camera";
import { getCameraLegs } from "./templateRegistry";

// Version 2: neutral lead-in, left-to-right paired phrase, return, then remain neutral.
const LEGS = getCameraLegs("lr-phrase");

export const T4: React.FC = () => (
  <AbsoluteFill>
    <CameraViewport legs={LEGS}>
      <OffthreadVideo src={staticFile("excerpt.mp4")} style={{ width: 1920, height: 1080 }} />
    </CameraViewport>
  </AbsoluteFill>
);
