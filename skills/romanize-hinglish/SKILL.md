---
name: romanize-hinglish
description: Invoke whenever Hindi (or Hindi-English) speech becomes on-screen captions/text — converts a word-timestamped Devanagari transcript into modern Hinglish (romanized Hindi, Latin script) while preserving every word's timing. Do NOT hand-write replacement captions or ship Devanagari (rule N9, zero-Devanagari grep-enforced). Run as a delegated sub-agent on the smallest capable model; feeds the F10 caption system.
---

# Romanize Hindi ASR → modern Hinglish captions

## Overview

Whisper transcribes Hindi speech in **Devanagari**. On-screen text in this project
is never Devanagari — it is **Hinglish**: Hindi words written in Latin script, the
way people actually type ("main abhi Hindi bol raha hoon lekin English mein likh
raha hoon"). This skill is that conversion step.

It is **not a transliteration script.** Mechanical Devanagari→Latin libraries
(ITRANS/IAST/ISO) produce stiff, academic forms — `लगता`→"lagataa", `हूँ`→"hūṁ" —
which are exactly wrong. Modern Hinglish is a language-understanding task: phonetic,
casual, context-aware, with English loanwords snapped back to English spelling. So
the converter is **an LLM reading this doc**, not code. The only code anywhere near
this is the backstop check at the end (a `grep`, not a converter).

## Run it as a delegated sub-agent (provider-neutral)

Romanization is mechanical enough to spend a small model on and should not burn the
director's context. Dispatch it:

- **Role, not a named model:** hand this task to a sub-agent on **the smallest /
  cheapest model in the current provider that can pass the backstop.** Do not hardcode
  a vendor model name in the pipeline. This project's [delegated-worker model](../../CLAUDE.md)
  already puts well-specified mechanical work on cheap executors.
- **Per-CLI binding (the contract is portable; the binding is local):**
  - Claude Code → the Agent/sub-agent tool with a small-model subagent (e.g. Haiku tier).
  - Codex / Antigravity / others → their own sub-agent facility and their own small tier.
- **Async:** the caller dispatches, keeps editing, and collects the returned transcript.
  The caller (not the sub-agent) runs the backstop before trusting the result.

Carry this whole file — especially the **Register** section — into the sub-agent's
prompt, so a small model produces *this* register rather than inventing its own.

## I/O contract

- **In:** a word-timestamped transcript in the project's Scribe word-format —
  `{"words":[{"type":"word","start":<s>,"end":<s>,"text":"<devanagari>"}, ...]}`
  (or `segments[].words[]`; preserve whichever shape you were given).
- **Out:** the **same JSON structure**, with each `text` rewritten to Hinglish.
  - **1:1 token alignment.** One output token per input word; never re-segment,
    split, or merge word slots. Downstream caption timing (X1 "arrive on the word")
    depends on the slots and `start`/`end` staying exactly as received.
  - **Timings are immutable.** Only `text` changes. Never touch `start`/`end`.
- **Context, not word-by-word:** read the full sentence/segment while deciding each
  word's spelling (spelling and mishearing-resolution are context-dependent), but
  still emit exactly one token per input slot.

## Register (the project lead-locked, 2026-07-16) — the taste rules

Write how a modern Hindi-speaker texts, not how a textbook transliterates.

**Locked spellings for the high-frequency words (settle these the same way every time):**

| Devanagari | Hinglish | not |
| --- | --- | --- |
| हूँ (…raha हूँ) | `hoon` | hun, hūṁ |
| क्यों | `kyun` | kyu, kyoṃ |
| वो / वोह | `woh` | vo, voh |
| में | `mein` | me, meṃ |
| लगता | `lagta` | lagataa |
| एक लड़के | `ek ladke` | ek laḍke |
| मैंने | `maine` | maiṇe |
| ज़िंदगी | `zindagi` | jindagi |

**General rules:**

1. **Drop academic long-vowel and diacritic markings.** No macrons, dots-under, or
   doubled vowels for length (`lagta`, not "lagataa"). Casual phonetic spelling wins.
2. **English loanwords → English spelling.** YouTube, vlog, video, edit, thumbnail,
   click, definition, comment, subscribe, shoot, camera — never romanize these back
   into Hindi phonetics or write them in Devanagari. If the speaker said an English
   word (even Hindi-accented), spell it in English.
3. **`z` for ज़, not `j`** (`zindagi`, `mazaa`); `w` for व in these words (`woh`,
   `waqt`).
4. **Preserve nasality only where the locked list keeps it** (`mein`, `maine` drop it;
   `hoon` keeps the long "oo"). Follow the table; extend it by analogy.
5. **Sentence case, natural spacing.** Proper nouns capitalized (`Irfan Junejo`).
   No Devanagari punctuation (।) — use Latin punctuation or none, matching the
   caption design.

**Honesty / restraint (from N9):**

- Romanization is a **writing act, not a lookup.** Resolve obvious ASR mishearings
  by context before they reach the screen (correct the word in its slot; keep the
  slot and timing).
- **Flag, don't guess.** If a word is genuinely ambiguous or the audio was unclear,
  mark it (e.g. leave a `"low_confidence": true` field on that token) rather than
  shipping a confident wrong spelling. A human resolves flags before render.

When the project lead corrects a spelling on screen, add it to the locked table above — his eye
is the authority on register, and the table is how his call becomes durable.

## Backstop (the receipt, not the converter)

After the sub-agent returns, the caller asserts the output is actually script-clean.
This is a validation check, **not** the romanization mechanism:

```bash
# On this skill's OWN output (a transcript JSON — every value is rendered data,
# no comments): any hit = a Devanagari codepoint survived → reject and re-run.
grep -oP '[\x{0900}-\x{097F}]+' <romanized-transcript.json> && echo "FAIL: Devanagari present" || echo "OK: clean"
```

Zero Devanagari codepoints (U+0900–U+097F) in the output is the pass condition.

The editorial verification gate runs the same idea as **check #9**, but over the
composition's **rendered text nodes** — not raw source — because Devanagari is *allowed
and useful* in code comments/annotations that trace which spoken Hindi word a card
lands on (e.g. `// card lands ON "क्रिटिकल"`). For an HTML composition, scope the grep
to rendered text between tags:

```bash
grep -oP '>[^<]*<' <composition.html> | grep -oP '[\x{0900}-\x{097F}]+'   # any hit = FAIL
```

This scoping was validated 2026-07-16: it correctly flags the real rendered leak
(`लगता` in the FP caption that shipped in `fp-excerpt-corrected.mp4` and was wrongly
marked approved) while passing the MC composition, whose only Devanagari is in
word-sync comments. A script leak of this class cannot silently regress again.

## Boundaries

- **Conversion is the LLM's job; the only code is the `grep` backstop.** Do not build
  a transliteration program.
- **Timings and token count are sacred.** This skill rewrites text, nothing else.
- **Hinglish, not translation.** Do not translate Hindi into English meaning — keep
  the Hindi words, just in Latin script. (English loanwords are the one exception,
  and only because the speaker already said them in English.)
- Enforced by [rule N9](../../docs/rulebook/beat-to-primitive-rules.md); consumed by
  the F10 caption system. Capability page:
  [`docs/capabilities/hinglish-romanization.md`](../../docs/capabilities/hinglish-romanization.md).
