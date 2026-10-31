# Project layout

The repository contains reusable knowledge and code only. Put each film in a separate,
ignored workspace.

```text
EditorialCut/
  docs/                 capability and editorial contracts
  skills/               repeatable procedures
  research/   reusable reference implementations and verifiers
  scripts/              repository safety checks

your-film-workspace/
  inputs/                immutable source links or copies
  analysis/              transcripts, beat maps, shot maps
  assets/                licensed/generated project assets
  renders/               previews and finals
  review/                contact sheets and decisions
```

Credentials stay in the environment. Engines and model weights stay outside both trees.

