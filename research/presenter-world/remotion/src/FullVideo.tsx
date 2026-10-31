import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, staticFile, Easing, Sequence } from "remotion";
import { Video } from "@remotion/media";
import transcriptData from "./transcript_romanized.json";

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

export const FullVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const fps = 59.94;
  const time = frame / fps;

  // --- TIMING CONSTANTS (Frames) ---
  const INTRO_END_FRAME = 2398;      // 40.00s
  const OUTRO_START_FRAME = 13966;    // 233.00s
  const OUTRO_END_FRAME = 18152;      // 302.84s

  // --- CAMERA TRAVEL MOTION (Rule N7/N8 compliance) ---
  let scale = 1.0;
  let cx = 960;
  let cy = 540;

  // Section 1: Intro (0 - 40s)
  if (frame <= INTRO_END_FRAME) {
    scale = 1.0;
    cx = 960;
    cy = 540;
  }
  // Section 2: Movie Breakdowns (40s - 233s)
  else if (frame < OUTRO_START_FRAME) {
    // Zoom in on Walter (left character) between 55s and 80s (frames 3296 to 4795)
    if (frame >= 3296 && frame < 4795) {
      const pIn = interpolate(frame, [3296, 3356], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      const pOut = interpolate(frame, [4735, 4795], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      const easeIn = Easing.bezier(0.25, 0.1, 0.25, 1)(pIn);
      const easeOut = Easing.bezier(0.25, 0.1, 0.25, 1)(pOut);
      scale = interpolate(easeIn - easeOut, [0, 1], [1.0, 1.12]);
      cx = interpolate(easeIn - easeOut, [0, 1], [960, 640]);
      cy = interpolate(easeIn - easeOut, [0, 1], [540, 540]);
    }
    // Zoom in on Skyler (right character) between 100s and 125s (frames 5994 to 7492)
    else if (frame >= 5994 && frame < 7492) {
      const pIn = interpolate(frame, [5994, 6054], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      const pOut = interpolate(frame, [7432, 7492], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      const easeIn = Easing.bezier(0.25, 0.1, 0.25, 1)(pIn);
      const easeOut = Easing.bezier(0.25, 0.1, 0.25, 1)(pOut);
      scale = interpolate(easeIn - easeOut, [0, 1], [1.0, 1.12]);
      cx = interpolate(easeIn - easeOut, [0, 1], [960, 1280]);
      cy = interpolate(easeIn - easeOut, [0, 1], [540, 540]);
    }
    else {
      scale = 1.0;
      cx = 960;
      cy = 540;
    }
  }
  // Section 3: Outro/Lesson (233s - 302.84s)
  else {
    const outroFrame = frame - OUTRO_START_FRAME;
    // 233s - 274s (outroFrame: 0 - 2458): slow camera push-in
    if (outroFrame <= 2458) {
      const p = interpolate(outroFrame, [0, 2458], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      const ease = Easing.bezier(0.25, 0.1, 0.25, 1)(p);
      scale = interpolate(ease, [0, 1], [1.0, 1.15]);
      cx = 960;
      cy = interpolate(ease, [0, 1], [540, 420]);
    }
    // 274s - 302.84s (outroFrame: 2458 - end): lateral slide & hold
    else {
      scale = 1.10;
      cx = 960;
      cy = 420;
    }
  }

  // --- REAR GRAPHICS ---
  // Subtext word reveal: Frame 15824 to 17200 (approx 29.19s relative to outro start = 262.19s overall)
  const showSubtext = frame >= 15824 && frame <= 17000;
  const subtextOpacity = interpolate(frame, [15824, 15854, 16970, 17000], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const subtextScale = interpolate(frame, [15824, 17000], [0.95, 1.02], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Climax Canvas Slide (relative frame 2730 in outro = 16696 overall)
  const canvasX = interpolate(frame, [16696, 16726], [-100, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Climax Card Fade
  const cardOpacity = interpolate(frame, [16716, 16746], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Presenter lateral slide (outro frame 2730 - 2760 = 16696 - 16726)
  const presenterX = interpolate(frame, [16696, 16726], [0, -340], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Canvas Swipe Out at the very end to transition out (outro frame 3100 - 3178 = 17066 - 17144)
  const canvasOpacity = interpolate(frame, [17066, 17144], [0.96, 0.0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // --- CAPTION LOGIC (Rule N9 & F10 Captions) ---
  const activeSegment = transcript.segments.find(
    (seg) => time >= seg.start && time < seg.end
  );

  // Fade out at video end
  const globalOpacity = interpolate(frame, [OUTRO_END_FRAME - 60, OUTRO_END_FRAME], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000", opacity: globalOpacity }}>
      {/* Root transform (Scene camera travel) */}
      <AbsoluteFill
        style={{
          transform: `scale(${scale}) translate(${(960 - cx) * scale}px, ${(540 - cy) * scale}px)`,
          transformOrigin: "960px 540px",
        }}
      >
        {/* Layer 1: Background plate (Full original video) */}
        <AbsoluteFill>
          <Video
            src={staticFile("hand-test-bg.mp4")}
            style={{ width: "100%", height: "100%" }}
            objectFit="cover"
            muted
          />
        </AbsoluteFill>

        {/* Layer 2: Rear graphics layer (occluded by presenter cutouts) */}
        <AbsoluteFill>
          {/* Canvas Slide (Intro paper texture) */}
          {frame <= INTRO_END_FRAME && (
            <AbsoluteFill
              style={{
                backgroundColor: "#fcfaf2",
                backgroundImage: `url(${staticFile("warm-ribbed-paper.jpg")})`,
                backgroundSize: "cover",
                backgroundBlendMode: "multiply",
                opacity: 0.12, // Subtle background grid in intro
              }}
            />
          )}

          {/* Canvas Slide (Climax) */}
          {frame >= OUTRO_START_FRAME && (
            <AbsoluteFill
              style={{
                backgroundColor: "#fcfaf2",
                backgroundImage: `url(${staticFile("warm-ribbed-paper.jpg")})`,
                backgroundSize: "cover",
                backgroundBlendMode: "multiply",
                transform: `translateX(${canvasX}%)`,
                opacity: canvasOpacity,
              }}
            />
          )}

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
          {frame >= 16696 && (
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
                opacity: cardOpacity * canvasOpacity,
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
                  color: "#e67e22",
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

        {/* Layer 3: Presenter Alpha Cutouts (VP9 WebM) */}
        {/* Intro cutout (0 - 40s) */}
        {frame <= INTRO_END_FRAME && (
          <Sequence from={0} durationInFrames={INTRO_END_FRAME + 1}>
            <Video
              src={staticFile("intro_cutout.webm")}
              style={{ width: "100%", height: "100%" }}
              objectFit="cover"
              muted
            />
          </Sequence>
        )}

        {/* Outro cutout (233s - end) */}
        {frame >= OUTRO_START_FRAME && frame <= OUTRO_END_FRAME && (
          <Sequence from={OUTRO_START_FRAME} durationInFrames={OUTRO_END_FRAME - OUTRO_START_FRAME + 1}>
            <AbsoluteFill
              style={{
                transform: `translateX(${presenterX}px)`,
              }}
            >
              <Video
                src={staticFile("outro_cutout.webm")}
                style={{ width: "100%", height: "100%" }}
                objectFit="cover"
                muted
              />
            </AbsoluteFill>
          </Sequence>
        )}

        {/* Layer 4: Front overlays / graphics / captions */}
        <AbsoluteFill>
          {/* Subtle vignette in canvas mode */}
          {frame >= 16696 && (
            <div
              style={{
                position: "absolute",
                width: "100%",
                height: "100%",
                pointerEvents: "none",
                background: "radial-gradient(circle, transparent 50%, rgba(0,0,0,0.15) 100%)",
                opacity: cardOpacity * canvasOpacity,
              }}
            />
          )}

          {/* Hinglish Caption Engine */}
          {activeSegment && (
            <div
              style={{
                position: "absolute",
                bottom: 80,
                width: "100%",
                display: "flex",
                justifyContent: "center",
                padding: "0 100px",
                boxSizing: "box-sizing",
              }}
            >
              <div
                style={{
                  fontFamily: "Outfit, sans-serif",
                  fontSize: frame >= INTRO_END_FRAME && frame < OUTRO_START_FRAME ? 40 : 48,
                  fontWeight: 800,
                  textAlign: "center",
                  color: "#ffffff",
                  textShadow: "0px 4px 12px rgba(0,0,0,0.85), -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000",
                  maxWidth: 1200,
                  lineHeight: 1.3,
                  letterSpacing: "-0.5px",
                  backgroundColor: frame >= INTRO_END_FRAME && frame < OUTRO_START_FRAME ? "rgba(0, 0, 0, 0.45)" : "transparent",
                  padding: frame >= INTRO_END_FRAME && frame < OUTRO_START_FRAME ? "8px 24px" : "0",
                  borderRadius: "16px",
                }}
              >
                {activeSegment.words ? (
                  activeSegment.words.map((w, idx) => {
                    const isWordActive = time >= w.start && time < w.end;
                    return (
                      <span
                        key={idx}
                        style={{
                          color: isWordActive ? "#ffaa00" : "#ffffff",
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
