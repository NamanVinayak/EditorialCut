import "./index.css";
import { Composition } from "remotion";
import { ConformanceReel } from "./ConformanceReel";

const FPS = 30;
const DURATION_IN_FRAMES = 600; // exactly 20.000s
const WIDTH = 1920;
const HEIGHT = 1080;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ConformanceReel"
        component={ConformanceReel}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
    </>
  );
};
