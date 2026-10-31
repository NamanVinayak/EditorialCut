import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { CameraViewport } from "./camera";
import { getLegs } from "./registry";
import { Plate, Cutout, MeasuredInset, useLook, toneColor, enterAt } from "./parts";
import {TypeTreatmentBeat} from "./typography";
import type { Beat } from "./types";

// Every generic renderer takes ONE beat spec and the look; it hand-codes nothing
// video-specific. Wording/placement/timing all come from beat.content.

const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return { frame, fps };
};

const Enter: React.FC<{ at: number; style?: React.CSSProperties; children: React.ReactNode }> = ({ at, style, children }) => {
  const { frame, fps } = useT();
  const e = enterAt(frame, fps, at);
  return <div style={{ opacity: e.opacity, transform: `translateY(${e.ty}px)`, ...style }}>{children}</div>;
};

// ---- CLEAN: plate + captions only -----------------------------------------
export const CleanBeat: React.FC<{ beat: Beat }> = ({ beat }) => (
  <AbsoluteFill style={{ background: "#000" }}>
    <Plate name={beat.plate} />
  </AbsoluteFill>
);

// ---- OVERLAY ACCENT: masked/anchor presenter + a stacked text element ------
// Handles the "kicker + display label" (b02) and "CONFLICT -> DRAMA / EXTREME"
// element (b05, b23) and short accents (b04/b07/b16/b20/b32) via content.lines.
const placementStyle = (p?: string): React.CSSProperties => {
  switch (p) {
    case "left": return { left: 90, top: 300, width: 760, textAlign: "left" };
    case "lower-left": return { left: 96, bottom: 250, width: 900, textAlign: "left" };
    case "center": return { left: 260, top: 360, width: 1400, textAlign: "left" };
    default: return { right: 70, top: 300, width: 780, textAlign: "left" }; // right
  }
};
export const OverlayAccent: React.FC<{ beat: Beat }> = ({ beat }) => {
  const look = useLook();
  const c = beat.content || {};
  const legs = beat.camera_template_id ? getLegs(beat.camera_template_id) : null;
  const Block = (
    <div style={{ position: "absolute", ...placementStyle(c.placement) }}>
      {c.kicker ? <Enter at={c.lines?.[0]?.at ?? 1.6}><div style={{ fontFamily: look.fonts.kicker, fontSize: 26, letterSpacing: 4, color: look.accent }}>{c.kicker}</div></Enter> : null}
      {c.title ? <Enter at={(c.lines?.[0]?.at ?? 1.7) + 0.2} style={{ marginTop: 10 }}><div style={{ fontFamily: look.fonts.display, fontWeight: 800, fontSize: 92, lineHeight: 1.0, color: look.paper, whiteSpace: "pre-line" }}>{c.title}</div></Enter> : null}
      {c.subtitle ? <Enter at={(c.lines?.[0]?.at ?? 2.0) + 0.5} style={{ marginTop: 14 }}><div style={{ fontFamily: look.fonts.quote, fontStyle: "italic", fontSize: 34, color: look.meta }}>{c.subtitle}</div></Enter> : null}
      {(c.lines || []).map((ln, i) => (
        <Enter key={i} at={ln.at ?? 2.2 + i * 1.4} style={{ marginTop: i === 0 ? 8 : 22 }}>
          <div style={{ fontFamily: look.fonts.display, fontWeight: 800, fontSize: 74, lineHeight: 1.05, color: toneColor(look, ln.tone) }}
            dangerouslySetInnerHTML={{ __html: ln.text.replace(/->/g, `<span style="color:${look.accent}">→</span>`) }} />
        </Enter>
      ))}
    </div>
  );
  const scene = (
    <>
      <Plate name={beat.plate} />
      {Block}
      {beat.cutout ? <Cutout name={beat.cutout} /> : null}
    </>
  );
  return <AbsoluteFill style={{ background: "#000" }}>{legs ? <CameraViewport legs={legs}>{scene}</CameraViewport> : <AbsoluteFill>{scene}</AbsoluteFill>}</AbsoluteFill>;
};

// ---- PULSE LIST: N2 accumulating numbered list beside masked presenter -----
export const PulseList: React.FC<{ beat: Beat }> = ({ beat }) => {
  const look = useLook();
  const { frame, fps } = useT();
  const c = beat.content || {};
  const legs = beat.camera_template_id ? getLegs(beat.camera_template_id) : null;
  const List = (
    <div style={{ position: "absolute", right: 70, top: 150, width: 830 }}>
      {(c.items || []).map((it, i) => {
        const e = enterAt(frame, fps, it.at);
        return (
          <div key={i} style={{ display: "flex", alignItems: "baseline", marginBottom: 18, opacity: e.opacity, transform: `translateY(${e.ty}px)` }}>
            <span style={{ fontFamily: look.fonts.kicker, fontSize: 34, color: look.accent, width: 82 }}>{it.n}</span>
            <span style={{ fontFamily: look.fonts.display, fontWeight: 700, fontSize: 52, color: look.paper }}>{it.text}</span>
          </div>
        );
      })}
    </div>
  );
  const scene = (<><Plate name={beat.plate} />{List}{beat.cutout ? <Cutout name={beat.cutout} /> : null}</>);
  return <AbsoluteFill style={{ background: "#000" }}>{legs ? <CameraViewport legs={legs}>{scene}</CameraViewport> : <AbsoluteFill>{scene}</AbsoluteFill>}</AbsoluteFill>;
};

// ---- STATION COMPARE: T4 lr-phrase, two narration stations, anchor presenter
export const StationCompare: React.FC<{ beat: Beat }> = ({ beat }) => {
  const look = useLook();
  const { frame, fps } = useT();
  const c = beat.content || {};
  const legs = beat.camera_template_id ? getLegs(beat.camera_template_id) : getLegs("T4");
  const Card = (side: "left" | "right", s: NonNullable<typeof c.stations>["left"], at: number) => {
    const e = enterAt(frame, fps, at);
    const e2 = enterAt(frame, fps, s.becauseAt ?? at + 4);
    return (
      <div style={{ position: "absolute", top: 300, [side]: 70, width: 560, opacity: e.opacity, transform: `translateY(${e.ty}px)` } as React.CSSProperties}>
        <div style={{ fontFamily: look.fonts.kicker, fontSize: 22, letterSpacing: 3, color: look.meta }}>{s.kicker}</div>
        <div style={{ fontFamily: look.fonts.display, fontWeight: 800, fontSize: 62, color: look.paper, marginTop: 8 }}>{s.who}</div>
        <div style={{ fontFamily: look.fonts.display, fontWeight: 700, fontSize: 40, color: look.accent, marginTop: 8 }}>{s.drive}</div>
        {s.because ? <div style={{ fontFamily: look.fonts.quote, fontStyle: "italic", fontSize: 32, color: look.neg, marginTop: 12, opacity: e2.opacity }}>{s.because}</div> : null}
      </div>
    );
  };
  const st = c.stations!;
  const scene = (<><Plate name={beat.plate} />{Card("left", st.left, st.left.becauseAt ? st.left.becauseAt - 4.4 : 1.3)}{Card("right", st.right, st.right.becauseAt ? st.right.becauseAt - 5.4 : 6.9)}{beat.cutout ? <Cutout name={beat.cutout} /> : null}</>);
  return <AbsoluteFill style={{ background: "#000" }}><CameraViewport legs={legs}>{scene}</CameraViewport></AbsoluteFill>;
};

// ---- CARD: full-frame presentation state (term/quote/rules/closing) --------
export const CardBeat: React.FC<{ beat: Beat }> = ({ beat }) => {
  const look = useLook();
  const c = beat.content || {};
  return (
    <AbsoluteFill style={{ background: look.surface }}>
      <AbsoluteFill style={{ background: `radial-gradient(1200px 700px at 30% 25%, ${look.accent}12, transparent 60%)` }} />
      <div style={{ position: "absolute", left: 130, top: c.items ? 240 : 360, width: 1400 }}>
        {c.kicker ? <Enter at={0.15}><div style={{ fontFamily: look.fonts.kicker, fontSize: 28, letterSpacing: 5, color: look.accent }}>{c.kicker}</div></Enter> : null}
        {c.title ? <Enter at={0.4} style={{ marginTop: 14 }}><div style={{ fontFamily: look.fonts.display, fontWeight: 800, fontSize: c.items ? 92 : 122, lineHeight: 0.99, color: look.paper, whiteSpace: "pre-line" }}>{c.title}</div></Enter> : null}
        {c.subtitle ? <Enter at={1.0} style={{ marginTop: 26 }}><div style={{ fontFamily: look.fonts.quote, fontSize: 40, color: look.meta, maxWidth: 1000 }}>{c.subtitle}</div></Enter> : null}
        {(c.items || []).map((it, i) => (
          <Enter key={i} at={it.at} style={{ display: "flex", alignItems: "baseline", marginTop: 30 }}>
            <span style={{ fontFamily: look.fonts.kicker, fontSize: 44, color: look.accent, width: 100 }}>{it.n}</span>
            <span style={{ fontFamily: look.fonts.display, fontWeight: 700, fontSize: 58, color: look.paper, maxWidth: 1180 }}>{it.text}</span>
          </Enter>
        ))}
      </div>
      {c.inset ? <MeasuredInset name={beat.plate} fx={c.inset.fx} fy={c.inset.fy} k={c.inset.k} /> : null}
    </AbsoluteFill>
  );
};

export const renderBeat = (beat: Beat) => {
  switch (beat.render) {
    case "type_treatment": return <TypeTreatmentBeat beat={beat} />;
    case "overlay_accent": return <OverlayAccent beat={beat} />;
    case "pulse_list": return <PulseList beat={beat} />;
    case "station_compare": return <StationCompare beat={beat} />;
    case "card": return <CardBeat beat={beat} />;
    default: return <CleanBeat beat={beat} />;
  }
};
