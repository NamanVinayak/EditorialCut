import React from "react";
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

// Head-session camera engine for the N10 template study (2026-07-16).
// Treatments declare a schedule of legs; this component owns the transform
// math and the boundary clamp. Treatment files must NOT reimplement motion.
//
// Camera model: the viewport samples a window of the 1920x1080 logical frame,
// window width 1920/s, centered on (cx, cy). The clamp keeps the window fully
// inside the frame, so no move can ever expose canvas beyond the video edge.

export type Ease = "standard" | "easeOut" | "linear" | "snap";

export interface CameraLeg {
  t0: number; // seconds, comp-relative
  t1: number;
  scale: [number, number];
  cx?: [number, number]; // omitted -> holds 960
  cy?: [number, number]; // omitted -> holds 540
  ease?: Ease;
}

const easeFn = (e: Ease | undefined): ((p: number) => number) => {
  switch (e) {
    case "easeOut":
      return Easing.out(Easing.cubic);
    case "linear":
      return Easing.linear;
    case "snap":
      return Easing.out(Easing.exp);
    default:
      return Easing.bezier(0.25, 0.1, 0.25, 1);
  }
};

// Legs must be sorted by t0 and non-overlapping. Between legs the camera
// holds the previous leg's end state; before the first leg it holds that
// leg's start state.
export const evaluateCamera = (
  legs: CameraLeg[],
  t: number,
): { scale: number; cx: number; cy: number } => {
  let scale = legs.length ? legs[0].scale[0] : 1;
  let cx = legs.length && legs[0].cx ? legs[0].cx[0] : 960;
  let cy = legs.length && legs[0].cy ? legs[0].cy[0] : 540;

  for (const leg of legs) {
    if (t >= leg.t1) {
      scale = leg.scale[1];
      if (leg.cx) cx = leg.cx[1];
      if (leg.cy) cy = leg.cy[1];
    } else if (t >= leg.t0) {
      const p = easeFn(leg.ease)((t - leg.t0) / (leg.t1 - leg.t0));
      scale = interpolate(p, [0, 1], leg.scale);
      if (leg.cx) cx = interpolate(p, [0, 1], leg.cx);
      if (leg.cy) cy = interpolate(p, [0, 1], leg.cy);
      break;
    } else {
      break;
    }
  }

  // A 1920x1080 viewport cannot fit inside a 1920x1080 source below 1x.
  // Enforce the boundary contract before calculating center limits.
  scale = Math.max(scale, 1);

  // Boundary-safe clamp (compose-presenter-world formula).
  const minCx = 960 / scale;
  const maxCx = 1920 - 960 / scale;
  const minCy = 540 / scale;
  const maxCy = 1080 - 540 / scale;
  cx = Math.min(Math.max(cx, minCx), maxCx);
  cy = Math.min(Math.max(cy, minCy), maxCy);

  return { scale, cx, cy };
};

export const CameraViewport: React.FC<{
  legs: CameraLeg[];
  children: React.ReactNode;
}> = ({ legs, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { scale: s, cx, cy } = evaluateCamera(legs, frame / fps);

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
