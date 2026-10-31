import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import {
  BackgroundVideo,
  PresenterAlpha,
  RibbonRear,
  RibbonFront,
  PillRow,
  Crossroads,
  ShowText,
} from "./beats";

// RULE: the background plate and the presenter cutout are the same physical
// scene. They must share IDENTICAL transforms at every frame — any relative
// motion between them produces a visible "double presenter" at his silhouette.
// Parallax/depth cues are applied to GRAPHICS layers only.

const usePull = () => {
  const frame = useCurrentFrame();
  const pullProgress = interpolate(frame, [495, 555], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const pullEase = Easing.bezier(0.25, 0.1, 0.25, 1)(pullProgress);
  const scale = interpolate(pullEase, [0, 1], [1.08, 1.0]);
  // Rear graphics scale slightly more than the scene during the pull so they
  // visibly parallax without ever separating the plate from the cutout.
  const rearScale = 1 + (scale - 1) * 1.5;
  return { frame, scale, rearScale };
};

export const MainA: React.FC = () => {
  const { frame, scale, rearScale } = usePull();

  return (
    <AbsoluteFill
      style={{ transform: `scale(${scale})`, transformOrigin: "center center" }}
    >
      {/* Scene: plate (locked with cutout below) */}
      <BackgroundVideo />

      {/* REAR graphics — behind the presenter */}
      <AbsoluteFill
        style={{ transform: `scale(${rearScale / scale})`, transformOrigin: "center center" }}
      >
        <RibbonRear frame={frame} />
        <PillRow frame={frame} />
        <Crossroads frame={frame} />
        <ShowText frame={frame} />
      </AbsoluteFill>

      {/* Scene: presenter cutout (locked with plate above — NO extra transform) */}
      <PresenterAlpha />

      {/* FRONT graphics — in front of the presenter */}
      <AbsoluteFill>
        <RibbonFront frame={frame} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const MainB: React.FC = () => {
  const { frame, scale, rearScale } = usePull();

  // Swipe: a designed canvas page slides in from the left, frames 555-567.
  const swipeX = interpolate(frame, [555, 567], [-100, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{ transform: `scale(${scale})`, transformOrigin: "center center" }}
    >
      {/* Scene background slot: plate + swiping canvas, locked with the cutout */}
      <AbsoluteFill style={{ overflow: "hidden" }}>
        <BackgroundVideo />
        <AbsoluteFill
          style={{
            backgroundColor: "#f4f1ea",
            backgroundImage: `
              linear-gradient(to right, rgba(0,0,0,0.05) 1px, transparent 1px),
              linear-gradient(to bottom, rgba(0,0,0,0.05) 1px, transparent 1px)
            `,
            backgroundSize: "80px 80px",
            transform: `translateX(${swipeX}%)`,
          }}
        />
      </AbsoluteFill>

      {/* REAR graphics */}
      <AbsoluteFill
        style={{ transform: `scale(${rearScale / scale})`, transformOrigin: "center center" }}
      >
        <RibbonRear frame={frame} />
        <PillRow frame={frame} />
        <Crossroads frame={frame} />
        {frame < 555 && <ShowText frame={frame} />}
      </AbsoluteFill>

      {/* Presenter cutout — locked to the scene, persists over the canvas page */}
      <PresenterAlpha />

      {/* FRONT graphics */}
      <AbsoluteFill>
        <RibbonFront frame={frame} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
