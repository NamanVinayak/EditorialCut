import "./index.css";
import { Composition } from "remotion";
import { MainA, MainB } from "./Compositions";
import { ProbeA, ProbeB } from "./Probe";
import { HandTest } from "./HandTest";
import { FullVideo } from "./FullVideo";

const FPS = 30;
const DURATION_IN_FRAMES = 600; // 20.000s at 30fps
const WIDTH = 1920;
const HEIGHT = 1080;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="FullVideo"
        component={FullVideo}
        durationInFrames={18152} // 302.84 seconds at 59.94fps
        fps={59.94}
        width={1920}
        height={1080}
      />
      <Composition
        id="HandTest"
        component={HandTest}
        durationInFrames={3178} // 53.00 seconds at 59.94fps
        fps={59.94}
        width={1920}
        height={1080}
      />
      <Composition
        id="MainA"
        component={MainA}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="MainB"
        component={MainB}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition id="ProbeA" component={ProbeA} durationInFrames={600} fps={FPS} width={WIDTH} height={HEIGHT} />
      <Composition id="ProbeB" component={ProbeB} durationInFrames={600} fps={FPS} width={WIDTH} height={HEIGHT} />
    </>
  );
};


