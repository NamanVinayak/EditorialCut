#!/usr/bin/env bash
# Fetches the third-party engines and installs the Node/Python toolchains
# EditorialCut's research/ code calls out to. Nothing this script downloads
# is committed to the repo -- engines/, models/, .venv*/, and node_modules/
# are all git-ignored. Safe to re-run; existing clones and installs are
# left alone.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== EditorialCut setup =="
echo "Root: $ROOT"
echo

# ---------------------------------------------------------------------------
# 0. Activation layer. Expose the one skills/ source to every CLI's skill root
#    and regenerate the per-CLI contract copies from AGENTS.md. Both are
#    idempotent and touch no media/engines, so run them first -- a fresh clone
#    self-activates for whichever coding agent the user runs.
# ---------------------------------------------------------------------------
echo "-- linking skills into per-tool skill roots (scripts/link-skills.sh)"
bash "$ROOT/scripts/link-skills.sh"
echo
echo "-- regenerating contract copies from AGENTS.md (scripts/gen-contract.sh)"
bash "$ROOT/scripts/gen-contract.sh"

# ---------------------------------------------------------------------------
# 1. Third-party engines. Cloned, never vendored -- each keeps its own
#    license and history. Remotion is NOT cloned here; it comes from npm
#    below (source-available with redistribution restrictions).
# ---------------------------------------------------------------------------
mkdir -p engines models

clone_or_skip() {
  local name="$1" url="$2" dest="$3"
  if [ -d "$dest/.git" ]; then
    echo "-- $name already present at $dest, skipping clone"
  else
    echo "-- cloning $name -> $dest"
    git clone "$url" "$dest"
  fi
}

clone_or_skip "HyperFrames"          "https://github.com/heygen-com/hyperframes.git"          "engines/hyperframes"
clone_or_skip "video-use"            "https://github.com/browser-use/video-use.git"           "engines/video-use"
clone_or_skip "RobustVideoMatting"   "https://github.com/PeterL1n/RobustVideoMatting"         "engines/robust-video-matting"

echo
echo "NOTE: read each engine's own LICENSE before using or redistributing it."
echo "  - RobustVideoMatting is GPL-3.0."
echo "  - video-use is MIT; HyperFrames follows its own repo license."

# ---------------------------------------------------------------------------
# 2. RVM checkpoint -- the default subject-masking backend needs the
#    MobileNetV3 weights. Downloaded into git-ignored models/ and verified
#    against the checksum this repo was built and tested with
#    (docs/capabilities/subject-masking.md).
# ---------------------------------------------------------------------------
RVM_CKPT="models/rvm_mobilenetv3.pth"
RVM_URL="https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3.pth"
RVM_SHA="3c7c1d92033f7c38d6577c481d13a195d7d80a159b960f4f3119ac7b534cf4f8"

echo
if [ -f "$RVM_CKPT" ]; then
  echo "-- RVM checkpoint already present at $RVM_CKPT, skipping download"
else
  echo "-- downloading RVM MobileNetV3 checkpoint -> $RVM_CKPT"
  if ! curl -fL --retry 3 -o "$RVM_CKPT" "$RVM_URL"; then
    echo "!! RVM checkpoint download failed; re-run setup or fetch manually:"
    echo "   curl -fL -o $RVM_CKPT $RVM_URL"
    rm -f "$RVM_CKPT"
  fi
fi
if [ -f "$RVM_CKPT" ]; then
  ACTUAL_SHA="$(shasum -a 256 "$RVM_CKPT" | awk '{print $1}')"
  if [ "$ACTUAL_SHA" = "$RVM_SHA" ]; then
    echo "-- RVM checkpoint checksum verified"
  else
    echo "!! RVM checkpoint checksum MISMATCH (got $ACTUAL_SHA); delete $RVM_CKPT and re-run"
  fi
fi

# ---------------------------------------------------------------------------
# 3. Remotion compositions. Each one is its own npm project; Remotion,
#    React, and Tailwind come down as ordinary npm dependencies.
# ---------------------------------------------------------------------------
REMOTION_DIRS=(
  "research/alpha-compositing/remotion"
  "research/camera-travel/remotion"
  "research/geometric-masks/remotion"
  "research/presenter-world/remotion"
  "research/camera-templates/composition/remotion"
  "research/presenter-world-kit"
)

for dir in "${REMOTION_DIRS[@]}"; do
  echo
  if [ -f "$dir/package.json" ]; then
    echo "-- npm install: $dir"
    (cd "$dir" && npm install)
  else
    echo "!! skipping $dir (no package.json found there)"
  fi
done

# HyperFrames composition (uses npx hyperframes, not a bundled engine)
HF_CHECK="research/alpha-compositing/hyperframes-check/hf-check"
echo
if [ -f "$HF_CHECK/package.json" ]; then
  echo "-- npm install: $HF_CHECK (HyperFrames composition)"
  (cd "$HF_CHECK" && npm install)
else
  echo "!! skipping $HF_CHECK (no package.json)"
fi

# ---------------------------------------------------------------------------
# 4. Python toolchain -- one shared venv carrying the plain-pip deps plus
#    the CLI tools the audio/footage pipelines shell out to.
# ---------------------------------------------------------------------------
echo
if [ -d ".venv" ]; then
  echo "-- .venv already exists, reusing it"
else
  echo "-- creating Python venv at .venv"
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "-- installing pipeline CLIs into .venv: demucs, yt-dlp"
pip install demucs yt-dlp

echo "-- installing beat_this (beat/downbeat detection, pinned v1.1.0)"
pip install "git+https://github.com/CPJKU/beat_this@v1.1.0"

if [ "$(uname -s)" = "Darwin" ] && [ "$(uname -m)" = "arm64" ]; then
  echo "-- Apple Silicon detected: installing mlx-whisper"
  pip install mlx-whisper
else
  echo "-- skipping mlx-whisper (Apple Silicon only); bring your own whisper CLI"
fi
deactivate

# ---------------------------------------------------------------------------
# 5. The short list that genuinely cannot be automated -- keys, and the
#    masking backends whose dependency stacks conflict with the shared venv.
# ---------------------------------------------------------------------------
cat <<'NOTES'

== Setup complete. What was installed ==

  engines/hyperframes            motion-design renderer
  engines/video-use              real-footage cutting + assembly orchestration
  engines/robust-video-matting   subject masking (RVM)
  models/rvm_mobilenetv3.pth     RVM checkpoint (checksum-verified)
  7x npm projects                Remotion + HyperFrames compositions
  .venv                          Python deps + demucs, yt-dlp, beat_this
                                 (+ mlx-whisper on Apple Silicon)

Activate the Python env with:  source .venv/bin/activate
(demucs, yt-dlp, beat_this, and mlx-whisper CLIs live inside it.)

== The short manual list ==

  API keys (put them in your shell or an ignored .env, never in a commit):
    FAL_KEY             image-to-video (research/image-to-video/)
    ELEVENLABS_API_KEY  word-level transcription used by video-use
    PEXELS_API_KEY      licensed stock sourcing (research/footage-sourcing/)

  video-use transcription caveat: prefer mlx-whisper (or your own whisper)
  with word timestamps over video-use's bundled helpers/transcribe.py --
  the bundled helper pins whisper-large-v3-turbo and drops probability
  metadata this system's caption gates rely on.

  beat_this downloads its own model checkpoint on first run.

  EdgeTAM / Apple Vision masking backends: each backend under
  research/masking/backends/ runs in its own per-backend venv; their
  dependency stacks conflict with each other and with the shared .venv.
  Don't try to merge them.

  inaSpeechSegmenter needs TensorFlow + tf-keras with TF_USE_LEGACY_KERAS=1
  at run time. If it fights the shared venv's numpy/torch at runtime, give
  it its own isolated venv -- that is what the original research
  environment did.
NOTES
