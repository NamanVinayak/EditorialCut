import React from "react";
import {useCurrentFrame, useVideoConfig} from "remotion";
import {evaluateCamera} from "./runtime";
import type {CameraLeg} from "./runtime";

export type {CameraLeg} from "./runtime";

// Head-session camera engine for the N10 template study (2026-07-16).
// Treatments declare a schedule of legs; this component owns the transform
// math and the boundary clamp. Treatment files must NOT reimplement motion.
//
// Camera model: the viewport samples a window of the 1920x1080 logical frame,
// window width 1920/s, centered on (cx, cy). The clamp keeps the window fully
// inside the frame, so no move can ever expose canvas beyond the video edge.

export const CameraViewport: React.FC<{
  legs: CameraLeg[];
  children: React.ReactNode;
}> = ({ legs, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const {scale: s, cx, cy} = evaluateCamera(legs, frame / fps);

  return (
    <div
      style={{
        width: 1920,
        height: 1080,
        overflow: "hidden",
        position: "relative",
        background: "#000",
      }}
    >
      <div
        style={{
          width: 1920,
          height: 1080,
          position: "absolute",
          transformOrigin: "960px 540px",
          transform: `translate(${-s * (cx - 960)}px, ${-s * (cy - 540)}px) scale(${s})`,
        }}
      >
        {children}
      </div>
    </div>
  );
};
