import React from "react";
import { AbsoluteFill, interpolate, staticFile } from "remotion";
import { Video } from "@remotion/media";

// Assets wrapped in AbsoluteFill for proper stacking
export const BackgroundVideo: React.FC<{ style?: React.CSSProperties }> = ({ style }) => {
  return (
    <AbsoluteFill style={style}>
      <Video
        src={staticFile("background-270-290.mp4")}
        style={{ width: "100%", height: "100%" }}
        objectFit="cover"
        muted
      />
    </AbsoluteFill>
  );
};

export const PresenterAlpha: React.FC<{ style?: React.CSSProperties }> = ({ style }) => {
  return (
    <AbsoluteFill style={style}>
      <Video
        src={staticFile("cutout-alpha.mov")}
        style={{ width: "100%", height: "100%" }}
        objectFit="cover"
        muted
      />
    </AbsoluteFill>
  );
};

// 1. Ribbon Beat
//
// Paths are authored against the MEASURED presenter silhouette in this
// footage (RVM alpha, frame 30): head spans x 820-1240 with face center
// ~(1030, 320); shoulder line at y ~860-940.
// The UPPER band sweeps across the head zone so his head/hair occludes it
// (rear layer); the LOWER band continues the same S across his chest and is
// drawn in front (front layer). One visual curve, two depth assignments —
// the video-09 mechanic.
//
// pathLength={1000} normalizes both paths so dash-based draw-in/retract is
// exact regardless of true path length.

// Authored left-to-right so textPath text reads upright.
const RIBBON_UPPER_D = "M 350 545 C 500 430, 690 408, 950 330 C 1240 240, 1520 160, 1860 70";
const RIBBON_LOWER_D = "M 350 545 C 450 730, 810 790, 1120 800 C 1430 810, 1690 925, 1860 1055";

const useRibbonDash = (
  frame: number,
  drawStart: number,
  drawEnd: number
): number => {
  // Draw-in: dashoffset 1000 -> 0; retract on exit: 0 -> 1000 (reverse).
  const drawIn = interpolate(frame, [drawStart, drawEnd], [1000, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const retract = interpolate(frame, [126, 148], [0, 1000], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return Math.max(drawIn, retract);
};

const ribbonText = (
  word: string,
  pathId: string,
  startOffset: string
): React.ReactElement => (
  <text>
    <textPath href={`#${pathId}`} startOffset={startOffset}>
      <tspan
        dy={20}
        fill="white"
        stroke="black"
        strokeWidth={4}
        paintOrder="stroke"
        style={{
          fontFamily: "system-ui, -apple-system, sans-serif",
          fontSize: 58,
          fontWeight: "bold",
        }}
      >
        {word}
      </tspan>
    </textPath>
  </text>
);

export const RibbonRear: React.FC<{ frame: number }> = ({ frame }) => {
  if (frame < 15 || frame > 150) return null;
  const dashOffset = useRibbonDash(frame, 15, 40);

  return (
    <AbsoluteFill>
      <svg viewBox="0 0 1920 1080" style={{ width: "100%", height: "100%", position: "absolute" }}>
        <path
          id="ribbon-upper"
          d={RIBBON_UPPER_D}
          fill="none"
          stroke="#9b8ec4"
          strokeWidth={64}
          strokeLinecap="round"
          pathLength={1000}
          strokeDasharray={1000}
          strokeDashoffset={dashOffset}
        />
        {/* "average" rides the upper band left of his head, over the room */}
        {frame >= 79 && frame < 126 && ribbonText("average", "ribbon-upper", "8%")}
      </svg>
    </AbsoluteFill>
  );
};

export const RibbonFront: React.FC<{ frame: number }> = ({ frame }) => {
  if (frame < 20 || frame > 150) return null;
  const dashOffset = useRibbonDash(frame, 22, 48);

  return (
    <AbsoluteFill>
      <svg viewBox="0 0 1920 1080" style={{ width: "100%", height: "100%", position: "absolute" }}>
        <path
          id="ribbon-lower"
          d={RIBBON_LOWER_D}
          fill="none"
          stroke="#9b8ec4"
          strokeWidth={64}
          strokeLinecap="round"
          pathLength={1000}
          strokeDasharray={1000}
          strokeDashoffset={dashOffset}
        />
        {/* "audience" rides the lower band across his chest, in front */}
        {frame >= 95 && frame < 126 && ribbonText("audience", "ribbon-lower", "38%")}
      </svg>
    </AbsoluteFill>
  );
};

// 2. Pill Row Beat
export const PillRow: React.FC<{ frame: number }> = ({ frame }) => {
  if (frame < 165 || frame > 285) return null;

  const scale = interpolate(frame, [165, 177, 273, 285], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(frame, [165, 177, 273, 285], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const pillHeights = [100, 180, 140, 260, 220, 160, 200, 240, 140, 220, 170, 280, 130, 90];

  return (
    <div
      style={{
        position: "absolute",
        top: "65%",
        left: 0,
        width: "100%",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "0 100px",
        boxSizing: "border-box",
        transform: `scale(${scale})`,
        transformOrigin: "center center",
        opacity: opacity,
      }}
    >
      {pillHeights.map((h, i) => (
        <div
          key={i}
          style={{
            width: 24,
            height: h,
            borderRadius: 12,
            backgroundColor: "rgba(255, 255, 255, 0.7)",
          }}
        />
      ))}
    </div>
  );
};

// 3. Crossroads Beat
export const Crossroads: React.FC<{ frame: number }> = ({ frame }) => {
  if (frame < 354 || frame > 495) return null;

  const scale = interpolate(frame, [364, 370], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(frame, [364, 370], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        width: "100%",
        height: "100%",
        opacity: opacity,
        transform: `scale(${scale})`,
        transformOrigin: "960px 540px",
      }}
    >
      <svg viewBox="0 0 1920 1080" style={{ width: "100%", height: "100%" }}>
        {/* Road 1: Diagonal Top-Left to Bottom-Right */}
        <polygon
          points="200,-100 300,-100 1720,1180 1420,1180"
          fill="#9b8ec4"
        />
        {/* Road 2: Diagonal Top-Right to Bottom-Left */}
        <polygon
          points="1720,-100 1620,-100 200,1180 500,1180"
          fill="#9b8ec4"
        />
        {/* Centerline 1 */}
        <line
          x1={250}
          y1={-100}
          x2={1570}
          y2={1180}
          stroke="white"
          strokeWidth={8}
          strokeDasharray="30,20"
        />
        {/* Centerline 2 */}
        <line
          x1={1670}
          y1={-100}
          x2={350}
          y2={1180}
          stroke="white"
          strokeWidth={8}
          strokeDasharray="30,20"
        />
      </svg>
    </div>
  );
};

// 4. Parallax & Pull Components
export const ShowText: React.FC<{ frame: number; style?: React.CSSProperties }> = ({ frame, style }) => {
  if (frame < 520) return null;
  const opacity = interpolate(frame, [529, 555], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: "20%",
        left: 0,
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        opacity: opacity,
        ...style,
      }}
    >
      <span
        style={{
          fontFamily: "system-ui, -apple-system, sans-serif",
          fontSize: 180,
          fontWeight: "bold",
          color: "white",
          textShadow: "-3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 3px 3px 0 #000",
        }}
      >
        SHOW
      </span>
    </div>
  );
};
