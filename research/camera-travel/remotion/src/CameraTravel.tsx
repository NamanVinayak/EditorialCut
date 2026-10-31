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
// Station-travel capability proof (rulebook N7), on the accepted benchmark
// window (Masterclass 270–290s, 1920x1080, 30 fps, 600 frames).
//
// Grammar being proven (from the video-01 camera study):
//   anchor -> travel to a station on its word -> hold within budget ->
//   return to anchor -> travel to the next station -> one vertical move ->
//   return to anchor.
//
// World model: one rigid 2.5D canvas. The presenter scene (plate + cutout,
// IDENTICAL transforms — the anti-doubling law) sits at world (0,0)-(1920,1080).
// Stations are placed on the surrounding canvas. The camera is a single
// translate+scale on the world root, so plate and cutout can never separate.
//
// Word sync (from assets/excerpt-270-290.json, offsets within the window):
//   "एवरेज ऑडियंस"        2.64–3.88s  -> travel to Station A on f79; label lands f95
//   "बहुत पसंद आएगा"       8.44–8.88s  -> audience dots pulse f253
//   (return to anchor     f267–289)
//   "फिल्मेकर के लेंचे"     12.14–13.08s -> travel to Station B on f364; label f385
//   "नॉर्मल ऑडियंस"        15.56–16.16s -> vertical travel to Station C f467; label f484
//   "यह शो अच्छा लगता"     17.44–18.46s -> return travel f529; GOOD SHOW chip on f529
//
// Hold budgets (N1/N2): A ≈ 6.2s, B ≈ 2.6s, C ≈ 1.4s, chip ≈ 1.9s — all ≤ 7s.
// Styling is diagnostic (concept-first); the design pass owns taste.
// ---------------------------------------------------------------------------

const INK = "#2a2f3a";
const ACCENT = "#9b8ec4";
const PAPER = "#f4f1ea";

// --- Camera -----------------------------------------------------------------

type CamState = { cx: number; cy: number; s: number };

const ANCHOR: CamState = { cx: 960, cy: 540, s: 1 };
const ST_A: CamState = { cx: 662, cy: 420, s: 1.45 };
const ST_B: CamState = { cx: 1258, cy: 420, s: 1.45 };
const ST_C: CamState = { cx: 1258, cy: 660, s: 1.45 };

type Travel = { from: number; to: number; a: CamState; b: CamState };

const TRAVELS: Travel[] = [
  { from: 79, to: 103, a: ANCHOR, b: ST_A }, // "एवरेज" f79
  { from: 267, to: 289, a: ST_A, b: ANCHOR }, // back to him for "फैमिली में पसंद आएगा"
  { from: 364, to: 388, a: ANCHOR, b: ST_B }, // "फिल्मेकर" f364
  { from: 467, to: 487, a: ST_B, b: ST_C }, // "नॉर्मल" f467 — the vertical move
  { from: 529, to: 555, a: ST_C, b: ANCHOR }, // "शो अच्छा लगता"
];

const camEase = Easing.bezier(0.45, 0.05, 0.2, 1);

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

// --- Scene modules ----------------------------------------------------------

const PlateAndNothingElse: React.FC = () => (
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

// Rear chip beside the head (head spans x 820–1240; face center ~(1030,320)).
// Left edge tucks behind the hair line so occlusion is visibly correct.
const GoodShowChip: React.FC<{ frame: number }> = ({ frame }) => {
  if (frame < 529 || frame > 597) return null;
  const opacity = interpolate(frame, [529, 537, 586, 596], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const rise = interpolate(frame, [529, 537], [16, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <div
      style={{
        position: "absolute",
        left: 1200,
        top: 236 + rise,
        padding: "18px 34px",
        background: "#ffffff",
        border: `4px solid ${INK}`,
        borderRadius: 14,
        transform: "rotate(-2deg)",
        opacity,
        fontFamily: "system-ui, -apple-system, sans-serif",
        fontWeight: 800,
        fontSize: 58,
        color: INK,
        whiteSpace: "nowrap",
      }}
    >
      GOOD SHOW.
    </div>
  );
};

// --- Station A: average audience (dot crowd) --------------------------------

const StationA: React.FC<{ frame: number }> = ({ frame }) => {
  if (frame < 82 || frame > 292) return null;
  const exit = interpolate(frame, [270, 284], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const ROWS = 3;
  const COLS = 5;
  const dots: React.ReactElement[] = [];
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const i = r * COLS + c;
      const born = 85 + i * 1.2;
      const pop = interpolate(frame, [born, born + 6], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      // "पसंद आएगा" pulse at f253 — the crowd likes it
      const pulse =
        1 +
        0.14 *
          Math.max(
            0,
            Math.sin(
              Math.PI *
                interpolate(frame, [253 + (r % 2) * 2, 265 + (r % 2) * 2], [0, 1], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                })
            )
          );
      dots.push(
        <div
          key={i}
          style={{
            position: "absolute",
            left: c * 90,
            top: r * 80,
            width: 48,
            height: 48,
            borderRadius: "50%",
            background: r === 1 && c === 2 ? ACCENT : INK,
            opacity: 0.92,
            transform: `scale(${pop * pulse})`,
          }}
        />
      );
    }
  }

  const labelIn = interpolate(frame, [95, 104], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ position: "absolute", left: 200, top: 220, opacity: exit }}>
      <div style={{ position: "relative", width: 420, height: 210 }}>{dots}</div>
      <div
        style={{
          marginTop: 20,
          opacity: labelIn,
          transform: `translateY(${(1 - labelIn) * 22}px)`,
          fontFamily: "system-ui, -apple-system, sans-serif",
          fontWeight: 800,
          fontSize: 48,
          letterSpacing: 2,
          color: INK,
        }}
      >
        AVERAGE AUDIENCE
      </div>
    </div>
  );
};

// --- Station B: filmmaker's lens (viewfinder) --------------------------------

const StationB: React.FC<{ frame: number }> = ({ frame }) => {
  if (frame < 366) return null;
  const ringDash = interpolate(frame, [368, 398], [1000, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const bracketsIn = interpolate(frame, [375, 385], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const labelIn = interpolate(frame, [385, 394], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const B = 90; // bracket arm length
  const bracket = (x: number, y: number, sx: number, sy: number) => (
    <path
      d={`M ${x + sx * B} ${y} L ${x} ${y} L ${x} ${y + sy * B}`}
      stroke={INK}
      strokeWidth={14}
      fill="none"
      opacity={bracketsIn}
    />
  );

  return (
    <div style={{ position: "absolute", left: 1220, top: 260 }}>
      <svg width={560} height={360} viewBox="0 0 1180 760">
        {/* viewfinder frame corners */}
        {bracket(40, 40, 1, 1)}
        {bracket(1140, 40, -1, 1)}
        {bracket(40, 720, 1, -1)}
        {bracket(1140, 720, -1, -1)}
        {/* the lens ring draws in */}
        <circle
          cx={590}
          cy={380}
          r={252}
          fill="none"
          stroke={ACCENT}
          strokeWidth={30}
          pathLength={1000}
          strokeDasharray={1000}
          strokeDashoffset={ringDash}
          transform="rotate(-90 590 380)"
        />
        <circle cx={590} cy={380} r={116} fill="none" stroke={INK} strokeWidth={16} opacity={bracketsIn} />
        {/* focus tick */}
        <line x1={590} y1={96} x2={590} y2={148} stroke={INK} strokeWidth={14} opacity={bracketsIn} />
      </svg>
      <div
        style={{
          marginTop: 10,
          opacity: labelIn,
          transform: `translateY(${(1 - labelIn) * 22}px)`,
          fontFamily: "system-ui, -apple-system, sans-serif",
          fontWeight: 800,
          fontSize: 48,
          letterSpacing: 2,
          color: INK,
          textAlign: "center",
          width: 560,
        }}
      >
        FILMMAKER&rsquo;S LENS
      </div>
    </div>
  );
};

// --- Station C: normal audience (seats facing a screen) ----------------------

const StationC: React.FC<{ frame: number }> = ({ frame }) => {
  if (frame < 470) return null;
  const screenIn = interpolate(frame, [476, 486], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const labelIn = interpolate(frame, [484, 493], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const seat = (x: number, y: number, i: number) => {
    const born = 478 + i * 2;
    const pop = interpolate(frame, [born, born + 6], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    return (
      <g key={`${x}-${y}`} transform={`translate(${x} ${y}) scale(${pop})`} opacity={0.94}>
        <rect x={-52} y={-40} width={104} height={84} rx={18} fill={INK} />
        <rect x={-64} y={28} width={128} height={30} rx={14} fill={INK} />
      </g>
    );
  };

  const seats: React.ReactElement[] = [];
  [0, 1, 2, 3].forEach((c) => seats.push(seat(300 + c * 180, 420, c)));
  [0, 1, 2].forEach((c) => seats.push(seat(390 + c * 180, 560, 4 + c)));

  return (
    <div style={{ position: "absolute", left: 1220, top: 620 }}>
      <svg width={500} height={300} viewBox="0 0 1060 640">
        {/* the screen they watch */}
        <rect
          x={190}
          y={60}
          width={680}
          height={200}
          rx={10}
          fill={ACCENT}
          opacity={screenIn * 0.9}
        />
        <rect x={190} y={60} width={680} height={200} rx={10} fill="none" stroke={INK} strokeWidth={10} opacity={screenIn} />
        {seats}
      </svg>
      <div
        style={{
          marginTop: 10,
          opacity: labelIn,
          transform: `translateY(${(1 - labelIn) * 22}px)`,
          fontFamily: "system-ui, -apple-system, sans-serif",
          fontWeight: 800,
          fontSize: 48,
          letterSpacing: 2,
          color: INK,
          textAlign: "center",
          width: 500,
        }}
      >
        NORMAL AUDIENCE
      </div>
    </div>
  );
};

// --- The world ---------------------------------------------------------------

export const CameraTravel: React.FC = () => {
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
        {/* Layer order: plate -> stations/elements -> cutout (presenter in front) */}
        <PlateAndNothingElse />

        {/* Stations live behind the presenter cutout */}
        <StationA frame={frame} />
        <StationB frame={frame} />
        <StationC frame={frame} />
        <GoodShowChip frame={frame} />

        <Cutout />
      </div>
    </AbsoluteFill>
  );
};
