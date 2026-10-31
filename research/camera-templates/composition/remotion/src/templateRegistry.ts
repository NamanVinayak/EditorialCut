import registry from "../../../templates.json";
import { CameraLeg, Ease } from "./camera";

export type ActiveTemplateId =
  | "reveal-out"
  | "emphasis-push"
  | "right-reveal"
  | "lr-phrase";

interface RegistryLeg {
  t0: number;
  t1: number;
  scale: [number, number];
  cx: [number, number];
  cy: [number, number];
  ease: Ease;
  reason: string;
}

interface RegistryTemplate {
  id: string;
  status: "candidate" | "rejected";
  composition_id: string | null;
  legs: RegistryLeg[];
}

const templates = registry.templates as RegistryTemplate[];

export const getCameraLegs = (id: ActiveTemplateId): CameraLeg[] => {
  const template = templates.find((item) => item.id === id && item.status === "candidate");
  if (!template) {
    throw new Error(`Active camera template not found: ${id}`);
  }
  return template.legs.map((leg) => ({
    t0: leg.t0,
    t1: leg.t1,
    scale: leg.scale,
    cx: leg.cx,
    cy: leg.cy,
    ease: leg.ease,
  }));
};
