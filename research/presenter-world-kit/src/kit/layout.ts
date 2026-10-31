import {evaluateCamera} from "./runtime";
import type {CameraLeg, CameraState} from "./runtime";

export interface Rect {
  left: number;
  top: number;
  right: number;
  bottom: number;
}

export interface SafeMargin {
  x: number;
  y: number;
}

export const visibleWorldRect = (state: CameraState): Rect => {
  const halfWidth = 960 / state.scale;
  const halfHeight = 540 / state.scale;
  return {
    left: state.cx - halfWidth,
    top: state.cy - halfHeight,
    right: state.cx + halfWidth,
    bottom: state.cy + halfHeight,
  };
};

const insetForScreenMargin = (
  rect: Rect,
  state: CameraState,
  margin: SafeMargin,
): Rect => ({
  left: rect.left + margin.x / state.scale,
  top: rect.top + margin.y / state.scale,
  right: rect.right - margin.x / state.scale,
  bottom: rect.bottom - margin.y / state.scale,
});

const intersect = (left: Rect, right: Rect): Rect => ({
  left: Math.max(left.left, right.left),
  top: Math.max(left.top, right.top),
  right: Math.min(left.right, right.right),
  bottom: Math.min(left.bottom, right.bottom),
});

export const cameraSampleTimes = (
  legs: CameraLeg[],
  duration: number,
): number[] => {
  const times = new Set<number>([0, Math.max(0, duration)]);
  for (const leg of legs) {
    times.add(Math.max(0, Math.min(duration, leg.t0)));
    times.add(Math.max(0, Math.min(duration, (leg.t0 + leg.t1) / 2)));
    times.add(Math.max(0, Math.min(duration, leg.t1)));
  }
  return [...times].sort((a, b) => a - b);
};

export const safeWorldRect = (
  legs: CameraLeg[],
  duration: number,
  margin: SafeMargin = {x: 80, y: 100},
): Rect => {
  const samples = cameraSampleTimes(legs, duration);
  let safe: Rect | null = null;
  for (const time of samples) {
    const state = evaluateCamera(legs, time);
    const atTime = insetForScreenMargin(
      visibleWorldRect(state),
      state,
      margin,
    );
    safe = safe ? intersect(safe, atTime) : atTime;
  }
  if (!safe || safe.left >= safe.right || safe.top >= safe.bottom) {
    throw new Error("camera trajectory leaves no shared safe layout region");
  }
  return safe;
};
