import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  Easing,
  staticFile,
} from "remotion";
import { Video } from "@remotion/media";

// ---------------------------------------------------------------------------
// Video-09 grammar proof: diagonal push-in + lateral slide
//
// Demonstrates the CORRECTED understanding of video-09's camera travel:
//   1. Static full frame (anchor)              0–2s    (f0–f59)
//   2. Diagonal push-in toward Element A       2–4.5s  (f60–f134)
//   3. Lateral slide right to Element B        4.5–7.5s (f135–f224)
//   4. Return to anchor                        7.5–9s  (f225–f269)
//   5. Hold anchor                             9–10s   (f270–f299)
//
// Key differences from CameraTravel.tsx (video-01 grammar):
//   - The push stays zoomed and slides continuously (no return between elements)
//   - The push is DIAGONAL (forward + sideways), not purely lateral
//   - Elements are BEHIND the presenter cutout (rear layer), not beside on canvas
//
// Uses the same benchmark clip assets (plate + cutout-alpha, Masterclass 270–290s).
// ---------------------------------------------------------------------------

const INK = "#1a1f2e";
const WARM = "#f5efe6";
const ACCENT_A = "#e8553d";    // element A accent (warm red)
const ACCENT_B = "#3d7be8";    // element B accent (cool blue)

// --- Camera -----------------------------------------------------------------

type CamState = { cx: number; cy: number; s: number };

// Anchor: presenter centered, full frame
const ANCHOR: CamState = { cx: 960, cy: 540, s: 1 };

// Element A: upper-left of presenter — the camera pushes in diagonally
// (forward = scale up, left+up = translate), landing close on the element
const ELEM_A: CamState = { cx: 686, cy: 400, s: 1.40 };

// Element B: right of presenter — camera slides right while staying zoomed
const ELEM_B: CamState = { cx: 1234, cy: 420, s: 1.40 };

type Travel = { from: number; to: number; a: CamState; b: CamState };

const FPS = 30;

const TRAVELS: Travel[] = [
  // 2s–4.5s: diagonal push-in to element A
  { from: 60, to: 134, a: ANCHOR, b: ELEM_A },
  // 4.5s–7.5s: lateral slide right to element B (staying zoomed)
  { from: 135, to: 224, a: ELEM_A, b: ELEM_B },
  // 7.5s–9s: return to anchor
  { from: 225, to: 269, a: ELEM_B, b: ANCHOR },
];

const camEase = Easing.bezier(0.35, 0.05, 0.15, 1);

const cameraAt = (frame: number): CamState => {
  let state: CamState = ANCHOR;
  for (const t of TRAVELS) {
    if (frame < t.from) return state;
    if (frame <= t.to) {
      const p = camEase((frame - t.from) / (t.to - t.from));
      return {
        cx: t.a.cx + (t.b.cx - t.a.cx) * p,
        cy: t.a.cy + (t.b.cy - t.a.cy) * p,
        s: t.a.s + (t.b.s - t.a.s) * p,
      };
    }
    state = t.b;
  }
  return state;
};

// --- Plate & cutout (locked together, never separate) -----------------------

const Plate: React.FC = () => (
  <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080 }}>
    <Video
      src={staticFile("background-270-290.mp4")}
      style={{ width: "100%", height: "100%" }}
      objectFit="cover"
      muted
    />
  </div>
);

const Cutout: React.FC = () => (
  <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080 }}>
    <Video
      src={staticFile("cutout-alpha.mov")}
      style={{ width: "100%", height: "100%" }}
      objectFit="cover"
      muted
    />
  </div>
);

// --- Element A: behind presenter, upper-left area ---------------------------
// A designed card that the camera pushes into diagonally.
// Positioned BEHIND the cutout (between plate and cutout in render order).

const ElementA: React.FC<{ frame: number }> = ({ frame }) => {
  // Appear as camera approaches (starting a bit before camera arrives)
  if (frame < 50 || frame > 250) return null;

  const fadeIn = interpolate(frame, [50, 80], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [225, 250], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Card builds up as camera arrives
  const cardScale = interpolate(frame, [60, 100], [0.85, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  // Label appears after camera is close
  const labelIn = interpolate(frame, [90, 110], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Subtle value change (like the $5 → $15 morph in video 9)
  const valueProgress = interpolate(frame, [110, 130], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const valueText = valueProgress < 0.5 ? "+$5" : "+$15";

  return (
    <div
      style={{
        position: "absolute",
        left: 330,
        top: 220,
        opacity: fadeIn * fadeOut,
        transform: `scale(${cardScale})`,
        transformOrigin: "center center",
      }}
    >
      {/* Translucent card */}
      <div
        style={{
          width: 380,
          padding: "36px 40px",
          background: "rgba(232, 85, 61, 0.15)",
          backdropFilter: "blur(8px)",
          border: `3px solid ${ACCENT_A}`,
          borderRadius: 24,
        }}
      >
        {/* Avatar icon */}
        <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 20 }}>
          <div
            style={{
              width: 52,
              height: 52,
              borderRadius: "50%",
              background: ACCENT_A,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontFamily: "system-ui, sans-serif",
              fontWeight: 800,
              fontSize: 24,
              color: "#fff",
            }}
          >
            R
          </div>
          <div
            style={{
              fontFamily: "system-ui, sans-serif",
              fontWeight: 700,
              fontSize: 22,
              color: WARM,
              opacity: 0.8,
            }}
          >
            RUSH CLIENT
          </div>
        </div>
        {/* Mock text lines */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 24 }}>
          <div style={{ height: 10, width: "90%", borderRadius: 5, background: "rgba(245,239,230,0.25)" }} />
          <div style={{ height: 10, width: "70%", borderRadius: 5, background: "rgba(245,239,230,0.18)" }} />
          <div style={{ height: 10, width: "80%", borderRadius: 5, background: "rgba(245,239,230,0.15)" }} />
        </div>
        {/* Value */}
        <div
          style={{
            fontFamily: "system-ui, sans-serif",
            fontWeight: 900,
            fontSize: 64,
            color: ACCENT_A,
            letterSpacing: -2,
            opacity: labelIn,
            transform: `translateY(${(1 - labelIn) * 14}px)`,
          }}
        >
          {valueText}
        </div>
      </div>
    </div>
  );
};

// --- Element B: behind presenter, right side --------------------------------
// The camera slides right to reach this element.

const ElementB: React.FC<{ frame: number }> = ({ frame }) => {
  if (frame < 120 || frame > 250) return null;

  const fadeIn = interpolate(frame, [120, 155], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [225, 250], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const cardScale = interpolate(frame, [135, 170], [0.85, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  const labelIn = interpolate(frame, [160, 180], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        left: 1240,
        top: 240,
        opacity: fadeIn * fadeOut,
        transform: `scale(${cardScale})`,
        transformOrigin: "center center",
      }}
    >
      <div
        style={{
          width: 380,
          padding: "36px 40px",
          background: "rgba(61, 123, 232, 0.15)",
          backdropFilter: "blur(8px)",
          border: `3px solid ${ACCENT_B}`,
          borderRadius: 24,
        }}
      >
        {/* Avatar icon */}
        <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 20 }}>
          <div
            style={{
              width: 52,
              height: 52,
              borderRadius: "50%",
              background: ACCENT_B,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontFamily: "system-ui, sans-serif",
              fontWeight: 800,
              fontSize: 24,
              color: "#fff",
            }}
          >
            L
          </div>
          <div
            style={{
              fontFamily: "system-ui, sans-serif",
              fontWeight: 700,
              fontSize: 22,
              color: WARM,
              opacity: 0.8,
            }}
          >
            LOYAL CLIENT
          </div>
        </div>
        {/* Mock text lines */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 24 }}>
          <div style={{ height: 10, width: "85%", borderRadius: 5, background: "rgba(245,239,230,0.25)" }} />
          <div style={{ height: 10, width: "65%", borderRadius: 5, background: "rgba(245,239,230,0.18)" }} />
          <div style={{ height: 10, width: "75%", borderRadius: 5, background: "rgba(245,239,230,0.15)" }} />
        </div>
        {/* Value */}
        <div
          style={{
            fontFamily: "system-ui, sans-serif",
            fontWeight: 900,
            fontSize: 64,
            color: ACCENT_B,
            letterSpacing: -2,
            opacity: labelIn,
            transform: `translateY(${(1 - labelIn) * 14}px)`,
          }}
        >
          6 MONTHS
        </div>
      </div>
    </div>
  );
};

// --- The world ---------------------------------------------------------------

export const V09Grammar: React.FC = () => {
  const frame = useCurrentFrame();
  const { cx, cy, s } = cameraAt(frame);

  // Map world -> viewport: world point (cx, cy) lands at viewport center.
  const tx = 960 - cx * s;
  const ty = 540 - cy * s;

  return (
    <AbsoluteFill style={{ background: INK, overflow: "hidden" }}>
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          transform: `translate(${tx}px, ${ty}px) scale(${s})`,
          transformOrigin: "0 0",
        }}
      >
        {/* Layer order: plate → rear elements → cutout (presenter in front) */}

        {/* 1. Plate (background video) */}
        <Plate />

        {/* 2. Rear elements — BEHIND the presenter */}
        <ElementA frame={frame} />
        <ElementB frame={frame} />

        {/* 3. Presenter cutout — in FRONT of elements */}
        <Cutout />
      </div>
    </AbsoluteFill>
  );
};
