import "./index.css";
import { Composition } from "remotion";
import { RearTypography, FrontBadge, Both } from "./Compositions";

const FPS = 30;
const DURATION_IN_FRAMES = 600; // 20.000s at 30fps
const WIDTH = 1920;
const HEIGHT = 1080;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="RearTypography"
        component={RearTypography}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="FrontBadge"
        component={FrontBadge}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="Both"
        component={Both}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
    </>
  );
};
