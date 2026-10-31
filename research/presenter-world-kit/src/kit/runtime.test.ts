import {activeCaptionIndex, evaluateCamera} from "./runtime";
import {safeWorldRect, visibleWorldRect} from "./layout";

const fail = (message: string): never => {
  throw new Error(message);
};

const assert = (condition: boolean, message: string) => {
  if (!condition) fail(message);
};

const assertEqual = <T>(actual: T, expected: T, message: string) => {
  if (actual !== expected) {
    fail(`${message}: expected ${String(expected)}, received ${String(actual)}`);
  }
};

const assertNear = (
  actual: number,
  expected: number,
  message: string,
  epsilon = 0.001,
) => {
  if (Math.abs(actual - expected) > epsilon) {
    fail(`${message}: expected ${expected}, received ${actual}`);
  }
};

const full = visibleWorldRect({scale: 1, cx: 960, cy: 540});
assertNear(full.left, 0, "1x left edge");
assertNear(full.top, 0, "1x top edge");
assertNear(full.right, 1920, "1x right edge");
assertNear(full.bottom, 1080, "1x bottom edge");

const move = [
  {
    t0: 0,
    t1: 2,
    scale: [1, 1.2] as [number, number],
    cx: [960, 1040] as [number, number],
    cy: [540, 500] as [number, number],
    ease: "linear" as const,
  },
];
const safe = safeWorldRect(move, 3, {x: 80, y: 100});
assert(safe.left > 80, "safe rect intersects the move on the left");
assert(safe.right < 1840, "safe rect intersects the move on the right");
assert(safe.top > 100, "safe rect intersects the move on the top");
assert(safe.bottom < 980, "safe rect intersects the move on the bottom");

const landing = evaluateCamera(move, 2);
assertNear(landing.scale, 1.2, "camera lands at requested scale");
assertNear(landing.cx, 1040, "camera lands at requested x center");
assertNear(landing.cy, 500, "camera lands at requested y center");

const words = [
  {t: 0, e: 0.4, w: "one"},
  {t: 2, e: 2.3, w: "two"},
];
assertEqual(
  activeCaptionIndex(words, 1),
  -1,
  "caption clears after end plus grace during a pause",
);
assertEqual(
  activeCaptionIndex(words, 2.1),
  1,
  "caption advances to the next word at its onset",
);
assertEqual(
  activeCaptionIndex(words, 0.5),
  0,
  "caption remains briefly visible inside the end grace",
);
assertEqual(
  activeCaptionIndex(words, 0.59),
  -1,
  "caption clears immediately after the end grace",
);

console.log("runtime tests: PASS");
