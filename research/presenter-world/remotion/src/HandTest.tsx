import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, staticFile, Easing } from "remotion";
import { Video } from "@remotion/media";
import transcriptData from "./transcript_romanized.json";

// Types for transcript
interface Word {
  word: string;
  start: number;
  end: number;
}

interface Segment {
  start: number;
  end: number;
  text: string;
  words?: Word[];
}

const transcript = transcriptData as { segments: Segment[] };

export const HandTest: React.FC = () => {
  const frame = useCurrentFrame();
  const fps = 59.94;
  const time = frame / fps;

  // --- CAMERA TRAVEL MOTION (Stage 4 & Rule N7/N8 compliance) ---
  // Scale and center tracking
  let scale = 1.0;
  let cx = 960;
  let cy = 540;

  // Frame boundaries
  // Hook (0 - 360 frames / 0 - 6s): static
  if (frame <= 360) {
    scale = 1.0;
    cx = 960;
    cy = 540;
  }
  // Intro (360 - 700 frames / 6 - 11.67s): slow push
  else if (frame <= 700) {
    const p = interpolate(frame, [360, 700], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    const ease = Easing.bezier(0.25, 0.1, 0.25, 1)(p);
    scale = interpolate(ease, [0, 1], [1.0, 1.08]);
    cx = 960;
    cy = interpolate(ease, [0, 1], [540, 480]);
  }
  // Transition (700 - 1150 frames / 11.67 - 19.18s): hold zoom
  else if (frame <= 1150) {
    scale = 1.08;
    cx = 960;
    cy = 480;
  }
  // Walter's Emotion (1150 - 1750 frames / 19.18 - 29.19s): deeper push
  else if (frame <= 1750) {
    const p = interpolate(frame, [1150, 1750], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    const ease = Easing.bezier(0.25, 0.1, 0.25, 1)(p);
    scale = interpolate(ease, [0, 1], [1.08, 1.15]);
    cx = 960;
    cy = interpolate(ease, [0, 1], [480, 420]);
  }
  // Subtext Build (1750 - 2730 frames / 29.19 - 45.54s): hold deep zoom
  else if (frame <= 2730) {
    scale = 1.15;
    cx = 960;
    cy = 420;
  }
  // Climax Climax (2730 - 3178 frames / 45.54 - 53s): lateral drift and scale down to fit card
  else {
    const p = interpolate(frame, [2730, 2760], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    const ease = Easing.bezier(0.25, 0.1, 0.25, 1)(p);
    scale = interpolate(ease, [0, 1], [1.15, 1.10]);
    cx = 960;
    cy = 420;
  }

  // --- REAR GRAPHICS ---
  // Subtext word reveal: Frame 1887 to 2000 (approx 2s hold, ends on pause)
  const showSubtext = frame >= 1887 && frame <= 2100;
  const subtextOpacity = interpolate(frame, [1887, 1900, 2080, 2100], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const subtextScale = interpolate(frame, [1887, 2100], [0.95, 1.02], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Climax Canvas Slide (Frame 2730 onwards)
  const canvasX = interpolate(frame, [2730, 2750], [-100, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Climax Card Fade (Frame 2750 onwards)
  const cardOpacity = interpolate(frame, [2750, 2780], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Presenter lateral slide (Frame 2730 - 2760)
  const presenterX = interpolate(frame, [2730, 2760], [0, -340], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // --- CAPTION LOGIC (Rule N9 & F10 Captions) ---
  // Find current segment
  const activeSegment = transcript.segments.find(
    (seg) => time >= seg.start && time < seg.end
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* Root transform (Scene camera travel) */}
      <AbsoluteFill
        style={{
          transform: `scale(${scale}) translate(${(960 - cx) * scale}px, ${(540 - cy) * scale}px)`,
          transformOrigin: "960px 540px",
        }}
      >
        {/* Layer 1: Background plate (H.264 video proxy) */}
        <AbsoluteFill>
          <Video
            src={staticFile("hand-test-bg.mp4")}
            style={{ width: "100%", height: "100%" }}
            objectFit="cover"
            muted
          />
        </AbsoluteFill>

        {/* Layer 2: Rear graphics layer (occluded by Naman's cutout) */}
        <AbsoluteFill>
          {/* Canvas Slide (Rule N8 / Climax Transformation) */}
          <AbsoluteFill
            style={{
              backgroundColor: "#fcfaf2", // Warm eggshell cream
              backgroundImage: `url(${staticFile("warm-ribbed-paper.jpg")})`,
              backgroundSize: "cover",
              backgroundBlendMode: "multiply",
              transform: `translateX(${canvasX}%)`,
              opacity: 0.96,
            }}
          />

          {/* Subtext Reveal Word */}
          {showSubtext && (
            <div
              style={{
                position: "absolute",
                top: "16%",
                width: "100%",
                display: "flex",
                justifyContent: "center",
                opacity: subtextOpacity,
                transform: `scale(${subtextScale})`,
              }}
            >
              <h1
                style={{
                  fontFamily: "Playfair Display, serif",
                  fontSize: 160,
                  fontWeight: 800,
                  fontStyle: "italic",
                  color: "#2a2a2a",
                  margin: 0,
                  letterSpacing: "4px",
                }}
              >
                SUBTEXT
              </h1>
            </div>
          )}

          {/* Climax Cards on the right */}
          {frame >= 2730 && (
            <div
              style={{
                position: "absolute",
                left: "1020px",
                top: "0",
                width: "800px",
                height: "100%",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                opacity: cardOpacity,
                fontFamily: "Playfair Display, serif",
                color: "#1c1c1c",
              }}
            >
              <div
                style={{
                  fontSize: 54,
                  fontWeight: 800,
                  lineHeight: 1.1,
                  letterSpacing: "-1px",
                  textTransform: "uppercase",
                  marginBottom: 10,
                }}
              >
                What is not
                <br />
                being told
              </div>
              <div
                style={{
                  fontFamily: "Playfair Display, serif",
                  fontStyle: "italic",
                  fontSize: 36,
                  color: "#e67e22", // Warm orange accent
                  margin: "15px 0",
                  fontWeight: 600,
                }}
              >
                is bigger than
              </div>
              <div
                style={{
                  fontSize: 54,
                  fontWeight: 800,
                  lineHeight: 1.1,
                  letterSpacing: "-1px",
                  textTransform: "uppercase",
                }}
              >
                What is
                <br />
                being told
              </div>
            </div>
          )}
        </AbsoluteFill>

        {/* Layer 3: Presenter Alpha Cutout (RVM ProRes 4444 master) */}
        <AbsoluteFill
          style={{
            transform: `translateX(${presenterX}px)`,
          }}
        >
          <Video
            src={staticFile("hand-test-cutout.mov")}
            style={{ width: "100%", height: "100%" }}
            objectFit="cover"
            muted
          />
        </AbsoluteFill>

        {/* Layer 4: Front overlays / graphics */}
        <AbsoluteFill>
          {/* Subtle diagnostic/climax vignette in canvas mode */}
          {frame >= 2730 && (
            <div
              style={{
                position: "absolute",
                width: "100%",
                height: "100%",
                pointerEvents: "none",
                background: "radial-gradient(circle, transparent 50%, rgba(0,0,0,0.15) 100%)",
                opacity: cardOpacity,
              }}
            />
          )}

          {/* Hinglish Caption Engine (Rule N9, F10 sync) */}
          {activeSegment && (
            <div
              style={{
                position: "absolute",
                bottom: 80,
                width: "100%",
                display: "flex",
                justifyContent: "center",
                padding: "0 100px",
                boxSizing: "border-box",
              }}
            >
              <div
                style={{
                  fontFamily: "Outfit, sans-serif",
                  fontSize: 48,
                  fontWeight: 800,
                  textAlign: "center",
                  color: "#ffffff",
                  textShadow: "0px 4px 12px rgba(0,0,0,0.85), -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000",
                  maxWidth: 1200,
                  lineHeight: 1.3,
                  letterSpacing: "-0.5px",
                }}
              >
                {activeSegment.words ? (
                  activeSegment.words.map((w, idx) => {
                    const isWordActive = time >= w.start && time < w.end;
                    return (
                      <span
                        key={idx}
                        style={{
                          color: isWordActive ? "#ffaa00" : "#ffffff", // Highlight color
                          transition: "color 0.05s ease",
                          marginRight: "10px",
                          display: "inline-block",
                        }}
                      >
                        {w.word}
                      </span>
                    );
                  })
                ) : (
                  <span>{activeSegment.text}</span>
                )}
              </div>
            </div>
          )}
        </AbsoluteFill>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
