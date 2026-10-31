import React from "react";
import { AbsoluteFill } from "remotion";
import { BackgroundVideo, PresenterAlpha, PillRow } from "./beats";

// Probe A: job-1 structure — flat AbsoluteFill stack, no wrapper transform
export const ProbeA: React.FC = () => (
  <AbsoluteFill>
    <BackgroundVideo />
    <PillRow frame={200} />
    <PresenterAlpha />
  </AbsoluteFill>
);

// Probe B: worker structure — same layers inside scaled black wrapper
export const ProbeB: React.FC = () => (
  <div style={{ position: "absolute", width: "100%", height: "100%", transform: "scale(1.0)", transformOrigin: "center center", backgroundColor: "black", overflow: "hidden" }}>
    <BackgroundVideo />
    <PillRow frame={200} />
    <PresenterAlpha />
  </div>
);
