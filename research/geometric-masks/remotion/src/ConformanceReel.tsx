import React from "react";
import { AbsoluteFill, useCurrentFrame, staticFile, interpolate } from "remotion";

// Manual clamp (Remotion 4.0.x does not export clamp from remotion package)
const clamp = (val: number, min: number, max: number) =>
  Math.min(Math.max(val, min), max);
import { Video } from "@remotion/media";

// ─────────────────────────────────────────────────────────────────────────────
// Segment layout (all frame numbers are absolute, 0-indexed)
// Each segment is 120 frames (4 s @ 30fps).
// First 15 frames of each segment = neutral-gray text label.
// ─────────────────────────────────────────────────────────────────────────────
//  Seg 0  DIFFERENCE FLASH   abs 0–119
//  Seg 1  CUT BRIDGE         abs 120–239
//  Seg 2  CIRCULAR REVEAL    abs 240–359
//  Seg 3  BEFORE/AFTER SLIDER abs 360–479
//  Seg 4  GRADIENT FOCUS BAND abs 480–599
// ─────────────────────────────────────────────────────────────────────────────

const SEG = 120; // frames per segment
const LABEL_DUR = 15; // frames for label card

// Flash events in Seg 0 (DIFFERENCE FLASH):
// Content starts at abs frame 15 (seg-local frame 15).
// Event A: 2-frame flash  → abs 25–26  (seg-local 25–26)
// Event B: 3-frame flash  → abs 50–52  (seg-local 50–52)
// Stacked: rect0 80-83 (4f), rect1 83-86 (4f), rect2 86-89 (4f)
//   → 1-frame overlaps between successive pairs; clean plate from frame 90
const FLASH_A_START = 25;
const FLASH_A_END   = 28; // inclusive — 4 frames
const FLASH_B_START = 50;
const FLASH_B_END   = 54; // inclusive — 5 frames
const STACK_0_START = 80; const STACK_0_END = 83;
const STACK_1_START = 83; const STACK_1_END = 86;
const STACK_2_START = 86; const STACK_2_END = 89;

// CUT BRIDGE (Seg 1, abs 120–239):
// Hard cut at abs frame 180 (seg-local 60).
// Flash A: 3 frames ending on last pre-cut frame → abs 177–179
// Flash B: 3 frames starting on first post-cut frame → abs 180–182
const SEG1_START = 120;
const CUT_FRAME   = 180; // first frame of second half
const SEG1_FLASH_A_START = 177; const SEG1_FLASH_A_END = 179;
const SEG1_FLASH_B_START = 180; const SEG1_FLASH_B_END = 182;

// CIRCULAR REVEAL (Seg 2, abs 240–359):
// Label: abs 240–254. Reveal animation: abs 270–299 (30 frames = 1s).
const SEG2_START = 240;
const REVEAL_START = 270; const REVEAL_END = 299;

// BEFORE/AFTER SLIDER (Seg 3, abs 360–479):
// Label: abs 360–374. Sweep: abs 390–449 (60 frames = 2s).
const SEG3_START = 360;
const SWEEP_START = 390; const SWEEP_END = 449;

// GRADIENT FOCUS BAND (Seg 4, abs 480–599):
const SEG4_START = 480;

// ─────────────────────────────────────────────────────────────────────────────
// Helper: neutral-gray label overlay
// ─────────────────────────────────────────────────────────────────────────────
const LabelCard: React.FC<{ text: string }> = ({ text }) => (
  <div
    style={{
      position: "absolute",
      inset: 0,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      backgroundColor: "rgba(0,0,0,0.55)",
      zIndex: 100,
    }}
  >
    <span
      style={{
        fontFamily: "Arial, Helvetica, sans-serif",
        fontWeight: 700,
        fontSize: 72,
        color: "#999999",
        letterSpacing: 4,
      }}
    >
      {text}
    </span>
  </div>
);

// ─────────────────────────────────────────────────────────────────────────────
// Plate video component (hard-linked into public/)
// startFrom: the absolute frame in the source to start reading from.
// ─────────────────────────────────────────────────────────────────────────────
const PlateVideo: React.FC<{ src: string; startFrom?: number }> = ({
  src,
  startFrom = 0,
}) => (
  <AbsoluteFill>
    <Video
      src={staticFile(src)}
      objectFit="cover"
      muted
      startFrom={startFrom}
    />
  </AbsoluteFill>
);

// ─────────────────────────────────────────────────────────────────────────────
// Segment 0: DIFFERENCE FLASH
// ─────────────────────────────────────────────────────────────────────────────
const Seg0DifferenceFlash: React.FC<{ frame: number }> = ({ frame }) => {
  const showLabel = frame < LABEL_DUR;

  // Event A: 2-frame white rect (abs 25–26)
  const flashA = frame >= FLASH_A_START && frame <= FLASH_A_END;
  // Event B: 3-frame white rect (abs 50–52)
  const flashB = frame >= FLASH_B_START && frame <= FLASH_B_END;
  // Stacked: 3 rects with 1-frame overlaps
  const stack0 = frame >= STACK_0_START && frame <= STACK_0_END;
  const stack1 = frame >= STACK_1_START && frame <= STACK_1_END;
  const stack2 = frame >= STACK_2_START && frame <= STACK_2_END;

  return (
    <AbsoluteFill>
      <PlateVideo src="plate.mp4" startFrom={0} />
      {showLabel && <LabelCard text="DIFFERENCE FLASH" />}

      {/* Event A: 2-frame difference flash */}
      {flashA && (
        <div
          style={{
            position: "absolute",
            top: 200,
            left: 300,
            width: 600,
            height: 200,
            backgroundColor: "white",
            mixBlendMode: "difference",
            zIndex: 10,
          }}
        />
      )}

      {/* Event B: 3-frame difference flash */}
      {flashB && (
        <div
          style={{
            position: "absolute",
            top: 400,
            left: 500,
            width: 800,
            height: 180,
            backgroundColor: "white",
            mixBlendMode: "difference",
            zIndex: 10,
          }}
        />
      )}

      {/* Stacked: rect 0 (9f, abs 80–88) */}
      {stack0 && (
        <div
          style={{
            position: "absolute",
            top: 150,
            left: 200,
            width: 500,
            height: 120,
            backgroundColor: "white",
            mixBlendMode: "difference",
            zIndex: 10,
          }}
        />
      )}
      {/* Stacked: rect 1 (9f, abs 81–89) — 1-frame overlap with rect 0 at end and rect 2 at start */}
      {stack1 && (
        <div
          style={{
            position: "absolute",
            top: 350,
            left: 400,
            width: 700,
            height: 140,
            backgroundColor: "white",
            mixBlendMode: "difference",
            zIndex: 10,
          }}
        />
      )}
      {/* Stacked: rect 2 (9f, abs 82–90) */}
      {stack2 && (
        <div
          style={{
            position: "absolute",
            top: 600,
            left: 600,
            width: 550,
            height: 130,
            backgroundColor: "white",
            mixBlendMode: "difference",
            zIndex: 10,
          }}
        />
      )}
    </AbsoluteFill>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// Segment 1: CUT BRIDGE
// Hard cut at abs frame 180. Two flash events straddling the cut.
// First half: source frames 0–59 of plate.
// Second half: source frames 300–359 of plate (different section).
// ─────────────────────────────────────────────────────────────────────────────
const Seg1CutBridge: React.FC<{ frame: number }> = ({ frame }) => {
  const localFrame = frame - SEG1_START;
  const showLabel = localFrame < LABEL_DUR;

  // Hard cut: frames 120–179 show first half, frames 180–239 show second half
  const inSecondHalf = frame >= CUT_FRAME;

  // Flash A: abs 178–179 (2 frames, ending on last frame before cut)
  const flashA = frame >= SEG1_FLASH_A_START && frame <= SEG1_FLASH_A_END;
  // Flash B: abs 180–181 (2 frames, starting on first frame after cut)
  const flashB = frame >= SEG1_FLASH_B_START && frame <= SEG1_FLASH_B_END;

  // Source frame for first-half video: localFrame - LABEL_DUR, clamped
  // For simplicity, plate startFrom=0 for first half, startFrom=300 for second half
  const firstHalfStart = 0;
  const secondHalfStart = 300;

  return (
    <AbsoluteFill>
      {!inSecondHalf ? (
        <PlateVideo src="plate.mp4" startFrom={firstHalfStart} />
      ) : (
        <PlateVideo src="plate.mp4" startFrom={secondHalfStart} />
      )}
      {showLabel && <LabelCard text="CUT BRIDGE" />}

      {/* Flash A: 2-frame, ends on last frame before cut */}
      {flashA && (
        <div
          style={{
            position: "absolute",
            top: 250,
            left: 350,
            width: 650,
            height: 180,
            backgroundColor: "white",
            mixBlendMode: "difference",
            zIndex: 10,
          }}
        />
      )}

      {/* Flash B: 2-frame, starts on first frame after cut */}
      {flashB && (
        <div
          style={{
            position: "absolute",
            top: 500,
            left: 550,
            width: 700,
            height: 160,
            backgroundColor: "white",
            mixBlendMode: "difference",
            zIndex: 10,
          }}
        />
      )}

      {/* Cut indicator: small static label showing which half we're in */}
      {!showLabel && (
        <div
          style={{
            position: "absolute",
            top: 20,
            right: 40,
            fontFamily: "Arial, Helvetica, sans-serif",
            fontSize: 32,
            color: "#888888",
            fontWeight: 700,
          }}
        >
          {inSecondHalf ? "B-SIDE" : "A-SIDE"}
        </div>
      )}
    </AbsoluteFill>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// Segment 2: CIRCULAR REVEAL
// clip-path circle expands from 0% to 100% radius over 30 frames (1s)
// Inside: gray treated plate. Outside: clean plate.
// ─────────────────────────────────────────────────────────────────────────────
const Seg2CircularReveal: React.FC<{ frame: number }> = ({ frame }) => {
  const localFrame = frame - SEG2_START;
  const showLabel = localFrame < LABEL_DUR;

  // Reveal progress: 0→1 over REVEAL_START to REVEAL_END
  const revealProgress = clamp(
    (frame - REVEAL_START) / (REVEAL_END - REVEAL_START + 1),
    0,
    1
  );

  // Radius goes from 0% to 75% (covers full 1920x1080 from center)
  const radiusPct = revealProgress * 75;

  return (
    <AbsoluteFill>
      {/* Bottom layer: clean plate */}
      <PlateVideo src="plate.mp4" startFrom={0} />

      {/* Top layer: grayscale treated plate, clipped to expanding circle */}
      <AbsoluteFill
        style={{
          clipPath: `circle(${radiusPct}% at 50% 50%)`,
        }}
      >
        <Video
          src={staticFile("plate-gray.mp4")}
          objectFit="cover"
          muted
          startFrom={0}
        />
      </AbsoluteFill>

      {showLabel && <LabelCard text="CIRCULAR REVEAL" />}

      {/* Progress indicator */}
      {!showLabel && (
        <div
          style={{
            position: "absolute",
            bottom: 40,
            left: 40,
            fontFamily: "Arial, Helvetica, sans-serif",
            fontSize: 28,
            color: "#888888",
            fontWeight: 700,
          }}
        >
          {`REVEAL ${Math.round(radiusPct)}%`}
        </div>
      )}
    </AbsoluteFill>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// Segment 3: BEFORE/AFTER SLIDER
// Vertical white 4px line sweeps left→right over 60 frames (2s).
// Left of line: noisy plate. Right: clean plate.
// ─────────────────────────────────────────────────────────────────────────────
const Seg3BeforeAfterSlider: React.FC<{ frame: number }> = ({ frame }) => {
  const localFrame = frame - SEG3_START;
  const showLabel = localFrame < LABEL_DUR;

  // Sweep progress: 0 at frame SWEEP_START, 1 at frame SWEEP_END
  const sweepProgress = clamp(
    (frame - SWEEP_START) / (SWEEP_END - SWEEP_START),
    0,
    1
  );

  // Line X position in pixels (0→1920)
  const lineX = Math.round(sweepProgress * 1920);

  return (
    <AbsoluteFill>
      {/* Right side (clean): full width, underneath */}
      <AbsoluteFill>
        <Video
          src={staticFile("plate.mp4")}
          objectFit="cover"
          muted
          startFrom={0}
        />
      </AbsoluteFill>

      {/* Left side (inverted): clipped to left of slider line */}
      <AbsoluteFill
        style={{
          clipPath: `inset(0 ${1920 - lineX}px 0 0)`,
        }}
      >
        <Video
          src={staticFile("plate-negate.mp4")}
          objectFit="cover"
          muted
          startFrom={0}
        />
      </AbsoluteFill>

      {/* Slider line */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: lineX - 2,
          width: 4,
          height: "100%",
          backgroundColor: "white",
          zIndex: 20,
        }}
      />

      {showLabel && <LabelCard text="BEFORE/AFTER SLIDER" />}

      {/* Side labels */}
      {!showLabel && lineX > 120 && (
        <div
          style={{
            position: "absolute",
            top: 30,
            left: 30,
            fontFamily: "Arial, Helvetica, sans-serif",
            fontSize: 28,
            color: "#999999",
            fontWeight: 700,
          }}
        >
          INVERTED
        </div>
      )}
      {!showLabel && lineX < 1800 && (
        <div
          style={{
            position: "absolute",
            top: 30,
            right: 30,
            fontFamily: "Arial, Helvetica, sans-serif",
            fontSize: 28,
            color: "#999999",
            fontWeight: 700,
          }}
        >
          CLEAN
        </div>
      )}
    </AbsoluteFill>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// Segment 4: CINEMATIC SCREEN CAPTURE
// Near-black #0b0b0d canvas with coordinate grid behind a 3D-tilted text-card
// panel. Camera drifts rotateY(-14→-9deg) linearly using interpolate() —
// seek-safe (no CSS animations). DOF blur applied INSIDE the panel so it tilts
// with it. Scanline texture overlaid at 10% opacity.
// ─────────────────────────────────────────────────────────────────────────────
const Seg4CinematicScreen: React.FC<{ frame: number }> = ({ frame }) => {
  const localFrame = frame - SEG4_START; // 0–119
  const showLabel = localFrame < LABEL_DUR;

  // Camera drift: rotateY linearly −12→−7 deg over the 120-frame segment.
  // Computed per-frame via interpolate() — NO CSS animations, fully seek-safe.
  const rotateYDeg = interpolate(localFrame, [0, 119], [-12, -7]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#0b0b0d" }}>
      {/* ── Coordinate grid: 1px white lines at 120px spacing, ~8% opacity ── */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: [
            "repeating-linear-gradient(to right,  rgba(255,255,255,0.08) 0px, rgba(255,255,255,0.08) 1px, transparent 1px, transparent 120px)",
            "repeating-linear-gradient(to bottom, rgba(255,255,255,0.08) 0px, rgba(255,255,255,0.08) 1px, transparent 1px, transparent 120px)",
          ].join(", "),
          pointerEvents: "none",
        }}
      />

      {/* ── 3D viewport: perspective on the container, transform on the panel ── */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          perspective: "1200px",
          perspectiveOrigin: "50% 50%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {/*
          Panel: full-frame dimensions so the Video layers fill it correctly.
          scale(0.62) keeps all four corners well inside the 1920×1080 frame.
          rotateX(12) + rotateZ(2) are static; rotateY drifts −12→−7 per-frame.
        */}
        <div
          style={{
            width: 1920,
            height: 1080,
            position: "relative",
            flexShrink: 0,
            transform: `rotateX(12deg) rotateY(${rotateYDeg.toFixed(4)}deg) rotateZ(2deg) scale(0.62)`,
            transformOrigin: "center center",
            borderRadius: 6,
            boxShadow: "0 50px 100px rgba(0,0,0,0.5)",
            overflow: "hidden",
          }}
        >
          {/* Layer 1: sharp text card — shows through the transparent center of the DOF mask */}
          <AbsoluteFill>
            <Video
              src={staticFile("text-card.mp4")}
              objectFit="cover"
              muted
              startFrom={0}
            />
          </AbsoluteFill>

          {/* Layer 2: blurred duplicate with gradient mask — applied INSIDE the panel
              so blur tilts with it. Opaque at top/bottom (unreadable), transparent
              in center (sharp layer shows through). */}
          <AbsoluteFill
            style={{
              maskImage:
                "linear-gradient(to bottom, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 20%, rgba(0,0,0,0) 35%, rgba(0,0,0,0) 65%, rgba(0,0,0,1) 80%, rgba(0,0,0,1) 100%)",
              WebkitMaskImage:
                "linear-gradient(to bottom, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 20%, rgba(0,0,0,0) 35%, rgba(0,0,0,0) 65%, rgba(0,0,0,1) 80%, rgba(0,0,0,1) 100%)",
              filter: "blur(28px)",
            }}
          >
            <Video
              src={staticFile("text-card.mp4")}
              objectFit="cover"
              muted
              startFrom={0}
            />
          </AbsoluteFill>

          {/* Layer 3: scanline texture — 2px repeating horizontal stripes at ~10% opacity.
              mixBlendMode overlay keeps it subtle over light text. */}
          <div
            style={{
              position: "absolute",
              inset: 0,
              backgroundImage:
                "repeating-linear-gradient(to bottom, rgba(0,0,0,0.10) 0px, rgba(0,0,0,0.10) 1px, transparent 1px, transparent 2px)",
              mixBlendMode: "overlay",
              pointerEvents: "none",
            }}
          />
        </div>
      </div>

      {showLabel && <LabelCard text="CINEMATIC SCREEN CAPTURE" />}

      {/* Zone indicators + drift readout (visible after label clears) */}
      {!showLabel && (
        <>
          <div
            style={{
              position: "absolute",
              top: 22,
              left: "50%",
              transform: "translateX(-50%)",
              fontFamily: "Arial, Helvetica, sans-serif",
              fontSize: 22,
              color: "#666666",
              fontWeight: 700,
              letterSpacing: 2,
            }}
          >
            BLUR BAND TOP
          </div>
          <div
            style={{
              position: "absolute",
              top: "42%",
              left: 22,
              fontFamily: "Arial, Helvetica, sans-serif",
              fontSize: 22,
              color: "#666666",
              fontWeight: 700,
              letterSpacing: 2,
            }}
          >
            SHARP CENTER
          </div>
          <div
            style={{
              position: "absolute",
              bottom: 22,
              left: "50%",
              transform: "translateX(-50%)",
              fontFamily: "Arial, Helvetica, sans-serif",
              fontSize: 22,
              color: "#666666",
              fontWeight: 700,
              letterSpacing: 2,
            }}
          >
            BLUR BAND BOTTOM
          </div>
          {/* Drift readout for seek/render verification */}
          <div
            style={{
              position: "absolute",
              bottom: 22,
              right: 22,
              fontFamily: "Arial, Helvetica, sans-serif",
              fontSize: 20,
              color: "#555555",
              fontWeight: 700,
            }}
          >
            {`rotY ${rotateYDeg.toFixed(1)}° · f${localFrame}`}
          </div>
        </>
      )}
    </AbsoluteFill>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// Root composition: dispatches to each segment by absolute frame number
// ─────────────────────────────────────────────────────────────────────────────
export const ConformanceReel: React.FC = () => {
  const frame = useCurrentFrame();

  const segment = Math.floor(frame / SEG); // 0-4

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      {segment === 0 && <Seg0DifferenceFlash frame={frame} />}
      {segment === 1 && <Seg1CutBridge frame={frame} />}
      {segment === 2 && <Seg2CircularReveal frame={frame} />}
      {segment === 3 && <Seg3BeforeAfterSlider frame={frame} />}
      {segment === 4 && <Seg4CinematicScreen frame={frame} />}
    </AbsoluteFill>
  );
};
