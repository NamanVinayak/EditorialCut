import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { LookCtx, Captions, Watermark } from "./kit/parts";
import { renderBeat } from "./kit/beats";
import type { EditPlan, LookTokens, CaptionDoc } from "./kit/types";

import editData from "../public/edit/beat-map.json";
import lookData from "../public/edit/look.json";
import capsData from "../public/edit/captions.json";

const edit = editData as unknown as EditPlan;
const look = lookData as unknown as LookTokens;
const caps = capsData as unknown as CaptionDoc;

// One composition renders the WHOLE video from data. No per-video code.
export const FullVideo: React.FC = () => {
  const fps = edit.fps;
  return (
    <LookCtx.Provider value={look}>
      <AbsoluteFill style={{ background: "#000" }}>
        {edit.beats.map((b) => {
          const from = Math.round(b.start_s * fps);
          const dur = Math.max(1, Math.round((b.end_s - b.start_s) * fps));
          return (
            <Sequence key={b.id} from={from} durationInFrames={dur} name={b.id}>
              {renderBeat(b)}
            </Sequence>
          );
        })}
        {/* screen-space, global-time overlays */}
        <Captions doc={caps} />
        {edit.proxy_watermark ? <Watermark /> : null}
      </AbsoluteFill>
    </LookCtx.Provider>
  );
};

export const editMeta = edit;
