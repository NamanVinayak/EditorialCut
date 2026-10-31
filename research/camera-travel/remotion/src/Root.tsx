import "./index.css";
import { Composition } from "remotion";
import { CameraTravel } from "./CameraTravel";
import { V09Grammar } from "./V09Grammar";

const FPS = 30;
const DURATION_IN_FRAMES = 600; // 20.000s at 30fps — the accepted benchmark window
const WIDTH = 1920;
const HEIGHT = 1080;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="CameraTravel"
        component={CameraTravel}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="V09Grammar"
        component={V09Grammar}
        durationInFrames={300}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
    </>
  );
};
