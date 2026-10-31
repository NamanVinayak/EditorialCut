// ---------------------------------------------------------------------------
// Presenter-world edit kit — data contract.
// A video is rendered by supplying THREE json files + per-beat media assets;
// NO per-video TSX. An executor (any CLI) fills these, never edits the kit code.
//   public/edit/look.json      -> LookTokens  (DERIVED per video — see look-derivation-recipe.md)
//   public/edit/beat-map.json  -> EditPlan    (beat-map-schema.md + the `content` payloads)
//   public/edit/captions.json  -> CaptionDoc  (word-synced, comp-relative to 0; Hinglish, zero Devanagari)
//   public/edit/plates/<id>.mp4 , cutouts/<id>.mov (cutout only for masked beats)
// ---------------------------------------------------------------------------

import type {
  TypeDepth,
  TypePlacement,
  TypeRole,
  TypeScale,
  TypeTreatment,
} from "./typography-model";

export type Tone = "paper" | "accent" | "neg" | "meta";

export interface LookTokens {
  concept: string;            // e.g. "screenwriter's case file" (derived from genre/register)
  accent: string;             // hex — DERIVED from the footage's motivated key light/color
  accent_source: string;      // provenance sentence (what in the footage it came from)
  neg: string;                // semantic-negative hex
  surface: string;            // card background hex
  paper: string;              // primary text hex
  meta: string;               // secondary text hex
  fonts: {
    display: string;
    kicker: string;
    quote: string;
    caption: string;
    attention?: string;
    identity?: string;
    editorial?: string;
    annotation?: string;
    utility?: string;
  };
  material: string;           // material language note (proxy uses css; conform may add texture)
}

export interface StationSpec { kicker: string; who: string; drive: string; because?: string; becauseAt?: number }

export type BeatDesignJob =
  | "identity"
  | "transformation"
  | "thesis"
  | "comparison"
  | "evidence"
  | "quote"
  | "annotation"
  | "utility"
  | "atmosphere";

export interface BeatDesign {
  job: BeatDesignJob;
  type_role: TypeRole;
  scale: TypeScale;
  depth: TypeDepth;
  readability: "full" | "recoverable" | "decorative";
  edge_policy: "contain" | "intentional_crop";
}

export interface BeatContent {
  kicker?: string;
  title?: string;
  subtitle?: string;
  placement?: TypePlacement;
  treatment?: TypeTreatment;
  // OverlayAccent: stacked lines each with a tone and an arrival time (comp-relative sec within the beat)
  lines?: {
    text: string;
    tone?: Tone;
    at?: number;
    role?: TypeRole;
    layer?: "rear" | "front";
  }[];
  // PulseList / rules: numbered items that pulse in on their onset (N2)
  items?: { n: string; text: string; at: number }[];
  // StationCompare (T4 lr-phrase): two narration-relevant stations
  stations?: { left: StationSpec; right: StationSpec };
  // measured face for a presentation inset (N3.1 — never blind); null/absent => no inset
  inset?: { fx: number; fy: number; k?: number } | null;
}

export interface Beat {
  id: string;
  start_s: number;
  end_s: number;
  spatial_mode: "clean" | "overlay" | "presentation";
  presenter_role: "anchor" | "cutout" | "framed_insert" | "absent";
  // which generic renderer to use for this beat
  render:
    | "clean"
    | "overlay_accent"
    | "type_treatment"
    | "station_compare"
    | "pulse_list"
    | "card";
  camera_template_id: "T1" | "T2" | "T3" | "T4" | null;
  is_effect_moment: boolean;
  plate: string;              // asset basename under public/edit/plates/<plate>.mp4
  cutout?: string | null;     // asset basename under public/edit/cutouts/<cutout>.mov (masked beats)
  design?: BeatDesign;
  content?: BeatContent;
  reason?: string;
}

export interface EditPlan {
  edit_slug: string;
  fps: number;
  width: number;
  height: number;
  proxy_watermark?: boolean;
  beats: Beat[];
}

export interface CaptionWord { t: number; e: number; w: string }
export interface CaptionDoc { words: CaptionWord[] }
