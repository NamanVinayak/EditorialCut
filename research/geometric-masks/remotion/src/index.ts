import "./index.css";
export { RemotionRoot as default } from "./Root";

// Remotion entry point
import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";
registerRoot(RemotionRoot);
