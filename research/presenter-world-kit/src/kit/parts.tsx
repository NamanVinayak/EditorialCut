import React, { createContext, useContext } from "react";
import { AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Video } from "@remotion/media";
import type { LookTokens, CaptionDoc, Tone } from "./types";
import {activeCaptionIndex} from "./runtime";

// Look tokens flow through context so no component hardcodes a palette/font.
export const LookCtx = createContext<LookTokens | null>(null);
export const useLook = (): LookTokens => {
  const l = useContext(LookCtx);
  if (!l) throw new Error("LookCtx not provided");
  return l;
};
export const toneColor = (look: LookTokens, tone?: Tone) =>
  tone === "accent" ? look.accent : tone === "neg" ? look.neg : tone === "meta" ? look.meta : look.paper;

export const Plate: React.FC<{ name: string }> = ({ name }) => (
  <AbsoluteFill>
    <Video src={staticFile(`edit/plates/${name}.mp4`)} style={{ width: 1920, height: 1080 }} muted />
  </AbsoluteFill>
);

export const Cutout: React.FC<{ name: string }> = ({ name }) => (
  <AbsoluteFill>
    <Video src={staticFile(`edit/cutouts/${name}.mov`)} style={{ width: 1920, height: 1080 }} muted />
  </AbsoluteFill>
);

// Word-synced karaoke caption band (screen-space; never inside the camera viewport).
// `words` are comp-relative to the FULL video 0; we window ~8 around the active word.
export const Captions: React.FC<{ doc: CaptionDoc; dim?: boolean }> = ({ doc, dim }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const look = useLook();
  const t = frame / fps;
  const words = doc.words;
  const active = activeCaptionIndex(words, t);
  if (active < 0) return null;
  const lo = Math.max(0, active - 4);
  const hi = Math.min(words.length, active + 4);
  return (
    <div style={{ position: "absolute", bottom: dim ? 44 : 96, left: 0, width: 1920, display: "flex", justifyContent: "center", opacity: dim ? 0.72 : 1 }}>
      <div style={{ maxWidth: 1500, textAlign: "center", fontFamily: look.fonts.caption, fontWeight: 600, fontSize: dim ? 34 : 44, lineHeight: 1.25, textShadow: "0 2px 14px rgba(0,0,0,0.85)" }}>
        {words.slice(lo, hi).map((w, i) => {
          const idx = lo + i;
          const spoken = t >= w.t;
          return (
            <span key={idx} style={{ color: idx === active ? look.accent : spoken ? look.paper : "rgba(244,239,230,0.42)", margin: "0 7px" }}>{w.w}</span>
          );
        })}
      </div>
    </div>
  );
};

export const Watermark: React.FC = () => {
  const look = useLook();
  return (
    <div style={{ position: "absolute", top: 22, left: 26, fontFamily: look.fonts.kicker, fontSize: 22, letterSpacing: 2, color: "rgba(244,239,230,0.55)", border: "1px solid rgba(244,239,230,0.35)", padding: "3px 10px", borderRadius: 4 }}>PROXY</div>
  );
};

// N3.1 — subject-MEASURED inset. fx,fy = measured face center in the 1920x1080
// plate (mask head band / vision). Centers the face horizontally with headroom.
export const MeasuredInset: React.FC<{ name: string; fx: number; fy: number; k?: number }> = ({ name, fx, fy, k = 0.66 }) => {
  const look = useLook();
  const W = 430, H = 560;
  const tx = W / 2 - k * fx;
  const ty = H * 0.3 - k * fy;
  return (
    <div style={{ position: "absolute", right: 110, bottom: 150, width: W, height: H, borderRadius: 14, overflow: "hidden", border: `1px solid rgba(244,239,230,0.18)`, boxShadow: "0 18px 60px rgba(0,0,0,0.55)", background: look.surface }}>
      <div style={{ position: "absolute", width: 1920, height: 1080, left: tx, top: ty, transform: `scale(${k})`, transformOrigin: "top left" }}>
        <Video src={staticFile(`edit/plates/${name}.mp4`)} style={{ width: 1920, height: 1080 }} muted />
      </div>
    </div>
  );
};

export const enterAt = (frame: number, fps: number, atSec: number, dur = 0.4) => {
  const p = Math.max(0, Math.min(1, (frame / fps - atSec) / dur));
  const e = 1 - Math.pow(1 - p, 3);
  return { opacity: e, ty: (1 - e) * 12 };
};
