# Third-party notices

EditorialCut is an editorial layer and calls external tools. Those projects are not
vendored here and remain governed by their own licenses. `scripts/setup.sh` fetches
or installs the ones marked "fetched by setup"; the rest are optional integrations.

## Rendering and composition engines

| Project | Role | License treatment |
|---|---|---|
| Remotion | React video renderer; installed per-composition via npm | Follow Remotion's current license, including its organization-size terms. No Remotion repository source is copied here. |
| HyperFrames | motion-design renderer; fetched by setup | Apache-2.0 project; its code is not copied here. |
| video-use | CLI-driven real-footage cutting/assembly orchestration; fetched by setup | MIT; its code is not copied here. |
| Open Design | optional design-component donor | Install separately; Apache-2.0 project code is not copied here. |
| FFmpeg | media processing | Install separately and follow the terms of the build you distribute. |

## Analysis models and tools

| Project | Role | License treatment |
|---|---|---|
| Robust Video Matting (RVM) | default subject-masking backend; repo fetched and checkpoint downloaded by setup | GPL-3.0 per its repository; no RVM source is copied here. |
| EdgeTAM | optional prompted-masking backend (own venv) | Install separately; follow its repository license (Apache-2.0). |
| beat_this | beat/downbeat detection; git-installed by setup | Follow its repository license; downloads its own model checkpoint on first run. |
| demucs | music/vocal stem separation; installed by setup | MIT per its repository. |
| yt-dlp | corpus/footage download CLI; installed by setup | Unlicense per its repository. |
| mlx-whisper | transcription CLI (Apple Silicon); installed by setup | MIT per its repository. |
| inaSpeechSegmenter | speech/music segmentation | MIT per its repository; may need an isolated venv (see setup notes). |
| silero-vad | voice-activity detection | MIT per its repository. |
| PySceneDetect (`scenedetect`) | shot detection | BSD-3-Clause per its repository. |
| OpenAI CLIP (via `transformers`) | frame/query embedding for footage mining | Follow the model card and `transformers` (Apache-2.0) terms. |

## Services (bring your own keys)

| Service | Role | Terms |
|---|---|---|
| fal | image-to-video generation over HTTP (`FAL_KEY`) | Governed by fal's terms of service. |
| Pexels API | licensed stock footage sourcing | Governed by the Pexels API terms. |
| ElevenLabs | word-level transcription used by video-use (`ELEVENLABS_API_KEY`) | Governed by ElevenLabs' terms of service. |

Names and links identify interoperability targets; they do not imply endorsement.
