import React from "react";
import {
  AbsoluteFill,
  Easing,
  OffthreadVideo,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { CameraViewport } from "./camera";
import { getCameraLegs } from "./templateRegistry";

// Version 2: open the right third for one visual moment, then return and stay neutral.
const LEGS = getCameraLegs("right-reveal");

// Pills are in-scene elements placed INSIDE CameraViewport, so they are
// authored in the same 1920x1080 scene-coordinate space as the camera legs
// above (absolute left/top === scene x/y).
const PILL_EXIT_T = 7.74;
const PILL_EXIT_DUR = 0.3;
const PILL_ENTER_DUR = 0.35;
const PILL_EASE = Easing.out(Easing.cubic);

const Pill: React.FC<{
  text: string;
  centerX: number;
  centerY: number;
  enterAt: number;
}> = ({ text, centerX, centerY, enterAt }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // Piecewise: fade/slide in over PILL_ENTER_DUR starting at enterAt, hold,
  // then fade/slide out over PILL_EXIT_DUR starting at PILL_EXIT_T (shared
  // by both pills so they release together on payoff).
  const opacity = interpolate(
    t,
    [enterAt, enterAt + PILL_ENTER_DUR, PILL_EXIT_T, PILL_EXIT_T + PILL_EXIT_DUR],
    [0, 1, 1, 0],
    { easing: PILL_EASE, extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  const slideX = interpolate(
    t,
    [enterAt, enterAt + PILL_ENTER_DUR, PILL_EXIT_T, PILL_EXIT_T + PILL_EXIT_DUR],
    [60, 0, 0, 40],
    { easing: PILL_EASE, extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  if (opacity < 0.001) return null;

  return (
    <div
      style={{
        position: "absolute",
        left: centerX,
        top: centerY,
        transform: `translate(-50%, -50%) translateX(${slideX}px)`,
        opacity,
        background: "#F7F4EE",
        color: "#1A1A1A",
        fontFamily: "system-ui, -apple-system, sans-serif",
        fontWeight: 600,
        fontSize: 44,
        lineHeight: 1,
        padding: "18px 36px",
        borderRadius: 999,
        whiteSpace: "nowrap",
      }}
    >
      {text}
    </div>
  );
};

export const T3: React.FC = () => (
  <AbsoluteFill>
    <CameraViewport legs={LEGS}>
      <OffthreadVideo src={staticFile("excerpt.mp4")} style={{ width: 1920, height: 1080 }} />
      <Pill text="FILMMAKING ✗" centerX={1530} centerY={430} enterAt={4.36} />
      <Pill text="SCREEN DIRECTING ✗" centerX={1530} centerY={560} enterAt={5.94} />
    </CameraViewport>
  </AbsoluteFill>
);
