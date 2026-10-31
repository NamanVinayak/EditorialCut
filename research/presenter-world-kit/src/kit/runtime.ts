import {Easing, interpolate} from "remotion";

export type Ease = "standard" | "easeOut" | "linear" | "snap";

export interface CameraLeg {
  t0: number;
  t1: number;
  scale: [number, number];
  cx?: [number, number];
  cy?: [number, number];
  ease?: Ease;
}

export interface CameraState {
  scale: number;
  cx: number;
  cy: number;
}

export interface CaptionWordLike {
  t: number;
  e: number;
  w: string;
}

const easeFn = (ease: Ease | undefined): ((progress: number) => number) => {
  switch (ease) {
    case "easeOut":
      return Easing.out(Easing.cubic);
    case "linear":
      return Easing.linear;
    case "snap":
      return Easing.out(Easing.exp);
    default:
      return Easing.bezier(0.25, 0.1, 0.25, 1);
  }
};

export const evaluateCamera = (
  legs: CameraLeg[],
  time: number,
): CameraState => {
  let scale = legs.length ? legs[0].scale[0] : 1;
  let cx = legs.length && legs[0].cx ? legs[0].cx[0] : 960;
  let cy = legs.length && legs[0].cy ? legs[0].cy[0] : 540;

  for (const leg of legs) {
    if (time >= leg.t1) {
      scale = leg.scale[1];
      if (leg.cx) cx = leg.cx[1];
      if (leg.cy) cy = leg.cy[1];
    } else if (time >= leg.t0) {
      const duration = leg.t1 - leg.t0;
      const linearProgress = duration <= 0 ? 1 : (time - leg.t0) / duration;
      const progress = easeFn(leg.ease)(
        Math.max(0, Math.min(1, linearProgress)),
      );
      scale = interpolate(progress, [0, 1], leg.scale);
      if (leg.cx) cx = interpolate(progress, [0, 1], leg.cx);
      if (leg.cy) cy = interpolate(progress, [0, 1], leg.cy);
      break;
    } else {
      break;
    }
  }

  scale = Math.max(scale, 1);
  const minCx = 960 / scale;
  const maxCx = 1920 - 960 / scale;
  const minCy = 540 / scale;
  const maxCy = 1080 - 540 / scale;
  cx = Math.min(Math.max(cx, minCx), maxCx);
  cy = Math.min(Math.max(cy, minCy), maxCy);

  return {scale, cx, cy};
};

export const activeCaptionIndex = (
  words: CaptionWordLike[],
  time: number,
  endGrace = 0.18,
): number => {
  let active = -1;
  for (let index = 0; index < words.length; index += 1) {
    const word = words[index];
    if (time >= word.t && time <= word.e + endGrace) {
      active = index;
    }
  }
  return active;
};
