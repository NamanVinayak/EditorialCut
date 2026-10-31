---
title: Hinglish Caption Romanization
aliases:
  - Devanagari to Hinglish
  - Romanize Hindi Captions
  - Hinglish Captions
type: capability
status: accepted-v1
updated: 2026-07-16
---

# Hinglish Caption Romanization

## Decision

**Accepted for v1 (concept + register locked 2026-07-16). Move on once the first
caption render passes the backstop.** On-screen text for Hindi speech is written in
**Hinglish** — Hindi words in Latin script — never in Devanagari. The conversion is
performed by an **LLM following the register doc**, dispatched to a small-model
sub-agent, and guaranteed script-clean by a `grep` backstop. There is no
transliteration program to build.

This capability exists because the failure it prevents actually shipped: the
`fp-excerpt-corrected.mp4` render (2026-07-16) was marked approved with the Devanagari
word `लगता` still on screen. Rule N9 already required Hinglish — nothing *enforced*
it. This capability is the enforcement.

## Editorial purpose

Turn a word-timestamped **Devanagari** transcript (Whisper's Hindi output) into
word-timestamped **Hinglish** caption tokens, preserving every word's timing, so the
F10 active-word caption system paints Latin-script text that lands on the spoken word.

The target register is *how modern people actually write Hindi in Latin script* —
casual and phonetic ("main abhi Hindi bol raha hoon lekin English mein likh raha
hoon") — **not** academic transliteration. That distinction is the whole capability.

## Why an LLM, not a script

Mechanical Devanagari→Latin transliterators (ITRANS, IAST, ISO 15919) are
deterministic and *wrong for this job*: they emit `लगता`→"lagataa", `हूँ`→"hūṁ",
`क्यों`→"kyoṃ" — stiff, diacritic-laden, nothing like how anyone texts. Producing
natural Hinglish requires judgment: phonetic casual spelling, English loanwords
restored to English spelling, and ASR-mishearing resolution by sentence context.
That is a language-understanding task, so the converter is an LLM. The only code is
the backstop check (a `grep`), which validates but never converts.

## How it runs (provider-neutral, delegated, async)

- **Delegated to a sub-agent** so it never burns the director's context — this is the
  project's standard [delegated-worker model](../../CLAUDE.md) applied to captions.
- **Role, not a vendor model:** "the smallest / cheapest model in the current provider
  that passes the backstop." A small model (Haiku-tier or equivalent) is sufficient.
  No provider name is hardcoded, so the same capability runs under Claude Code, Codex,
  or Antigravity — each binds the role to its own sub-agent facility and small tier.
- **Async:** dispatch → keep editing → collect. The **caller** runs the backstop
  before trusting the return.
- **Register travels with the prompt:** the sub-agent gets the register table from the
  skill, so a small model produces the project lead's Hinglish, not its own guess.

## Contract

- **In:** `{"words":[{"start","end","text":"<devanagari>"}]}` (or `segments[].words[]`).
- **Out:** same structure, `text` rewritten to Hinglish, **1:1 token alignment**,
  **timings untouched**.
- **Pass condition:** zero Devanagari codepoints (U+0900–U+097F) in the output.

## Register (the project lead-locked, 2026-07-16)

The authoritative register lives in the skill
([`skills/romanize-hinglish/SKILL.md`](../../skills/romanize-hinglish/SKILL.md)) —
single source of truth so it can't drift. Locked high-frequency calls: `hoon` (not
hun), `kyun` (not kyu), `woh` (not vo), `mein` (not me); drop academic long-vowels
and diacritics; English loanwords in English spelling; `z` for ज़. the project lead's on-screen
corrections extend the locked table over time.

## Boundaries

- **Hinglish, not translation.** Keep the Hindi words; only the script changes (English
  loanwords excepted, because the speaker already said them in English).
- **Timings and token count are sacred** — this rewrites text only.
- **Not a transliteration library.** Do not build or adopt a mechanical converter.
- **Flag, don't guess** ambiguous words rather than shipping a confident wrong spelling.

## Enforcement

- Rule [N9](../../docs/rulebook/beat-to-primitive-rules.md) — the language-register rule.
- Editorial verification gate, check #9 (zero-Devanagari `grep`) in
  [`creative-director-instructions.md`](../../docs/rulebook/creative-director-instructions.md)
  — no render is presented until it passes.
- Consumed by the **F10** active-word caption system.

## Skill

[`skills/romanize-hinglish/SKILL.md`](../../skills/romanize-hinglish/SKILL.md) — the
repeatable procedure, delegation contract, full register, and backstop command.
