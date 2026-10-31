// Consume the accepted N10 camera registry (mirrors canonical
// research/camera-templates/templates.json). T1..T4 -> the four accepted
// atoms; T5 (step-punch) rejected & non-selectable. Executors NEVER hand-author legs.
import templates from "./templates.json";
import type { CameraLeg } from "./camera";

const idFor: Record<string, string> = { T1: "reveal-out", T2: "emphasis-push", T3: "right-reveal", T4: "lr-phrase" };

interface CameraTemplateRecord {
  id: string;
  status: string;
  legs: CameraLeg[];
}

export const getLegs = (atom: "T1" | "T2" | "T3" | "T4"): CameraLeg[] => {
  const wanted = idFor[atom];
  const records = templates.templates as unknown as CameraTemplateRecord[];
  const t = records.find((candidate) => candidate.id === wanted && candidate.status === "candidate");
  if (!t) throw new Error(`camera atom ${atom} (${wanted}) not found/candidate in registry`);
  return t.legs;
};
