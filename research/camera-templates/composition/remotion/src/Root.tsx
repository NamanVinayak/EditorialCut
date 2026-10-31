import "./index.css";
import { Composition } from "remotion";
import { T1 } from "./T1";
import { T2 } from "./T2";
import { T3 } from "./T3";
import { T4 } from "./T4";

const FPS = 30;
const DURATION_IN_FRAMES = 336; // 11.200s sample excerpt
const WIDTH = 1920;
const HEIGHT = 1080;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="N10RevealOut"
        component={T1}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="N10EmphasisPush"
        component={T2}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="N10RightReveal"
        component={T3}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="N10LeftRightPhrase"
        component={T4}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
    </>
  );
};
