#!/usr/bin/env python3
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REMOTION_DIR = os.path.join(HERE, "remotion")
OUT_DIR = os.path.join(HERE, "out")
WAV_PATH = os.path.join(HERE, "assets", "excerpt-270-290.wav")

RENDERS = [
    ("MainA", "beat1-ribbon.mp4", "0-179"),
    ("MainA", "beat2-pills.mp4", "150-299"),
    ("MainA", "beat3-crossroads.mp4", "330-509"),
    ("MainA", "beat4a-parallax.mp4", "480-599"),
    ("MainB", "beat4b-canvas.mp4", "480-599"),
    ("MainA", "assembled-no-audio.mp4", "0-599")
]

def run_cmd(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    start = time.time()
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    duration = time.time() - start
    if res.returncode != 0:
        print(f"FAIL: {res.stderr}")
        raise Exception(f"Command failed: {cmd}")
    print(f"PASS (took {duration:.2f}s)")
    return duration

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # Remove any temp test file
    test_file = os.path.join(REMOTION_DIR, "out", "test.mp4")
    if os.path.exists(test_file):
        os.remove(test_file)
        
    timings = {}
    
    for comp_id, out_name, frames in RENDERS:
        out_path = os.path.join(OUT_DIR, out_name)
        cmd = [
            "npx", "remotion", "render", comp_id, out_path,
            f"--frames={frames}", "--muted", "--color-space=bt709"
        ]
        duration = run_cmd(cmd, cwd=REMOTION_DIR)
        timings[out_name] = duration
        
    # Mux audio into assembled.mp4
    no_audio_path = os.path.join(OUT_DIR, "assembled-no-audio.mp4")
    assembled_path = os.path.join(OUT_DIR, "assembled.mp4")
    
    mux_cmd = [
        "ffmpeg", "-y", "-i", no_audio_path, "-i", WAV_PATH,
        "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0",
        assembled_path
    ]
    
    run_cmd(mux_cmd)
    
    # Clean up no-audio version
    if os.path.exists(no_audio_path):
        os.remove(no_audio_path)
        
    print("\nRender timings:")
    for name, dur in timings.items():
        print(f"  {name}: {dur:.2f}s")

if __name__ == "__main__":
    main()
