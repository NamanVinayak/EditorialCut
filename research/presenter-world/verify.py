#!/usr/bin/env python3
import os
import sys
import json
import hashlib
import subprocess
from datetime import datetime, timezone

# Paths are relative to this script. Source media is not shipped with the
# repo -- supply your own cutout + background at these (git-ignored) paths and
# update the EXPECTED_* checksums below for your own files.
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT_DIR, "out")
VERIFY_DIR = os.path.join(OUT_DIR, "verification")
MANIFEST_PATH = os.path.join(ROOT_DIR, "manifest.json")

SOURCE_MOV = os.path.join(ROOT_DIR, "remotion", "public", "cutout-alpha.mov")
SOURCE_MP4 = os.path.join(ROOT_DIR, "remotion", "public", "background-270-290.mp4")

EXPECTED_MOV_SHA = "5ee2943014e84d8ec8e721ffbdfc0837ec1017e800519d542559dcfa3ce19292"
EXPECTED_MP4_SHA = "229371d07ea41bf58a8c744fcacec71a24dc9aaf31e3560c3958c2980778f906"

# Outputs configuration for checks
# (filename, expected_frames, check_audio)
OUTPUT_CONFIGS = [
    ("beat1-ribbon.mp4", 180, False),
    ("beat2-pills.mp4", 150, False),
    ("beat3-crossroads.mp4", 180, False),
    ("beat4a-parallax.mp4", 120, False),
    ("beat4b-canvas.mp4", 120, False),
    ("assembled.mp4", 600, True)
]

# Boundary stills specs:
# (beat_prefix, video_filename, frame_index, local_frame_index, crop_x, crop_y)
STILL_SPECS = [
    # Beat 1: frames 79, 95
    ("beat1", "beat1-ribbon.mp4", 79, 79, 810, 150),
    ("beat1", "beat1-ribbon.mp4", 95, 95, 770, 400),
    # Beat 2: frames 180, 240
    ("beat2", "beat2-pills.mp4", 180, 30, 680, 550),
    ("beat2", "beat2-pills.mp4", 240, 90, 940, 550),
    # Beat 3: frames 370, 450
    ("beat3", "beat3-crossroads.mp4", 370, 40, 680, 450),
    ("beat3", "beat3-crossroads.mp4", 450, 120, 940, 550),
    # Beat 4a: frames 535, 555
    ("beat4a", "beat4a-parallax.mp4", 535, 55, 730, 150),
    ("beat4a", "beat4a-parallax.mp4", 555, 75, 890, 150),
    # Beat 4b: frames 561, 570
    ("beat4b", "beat4b-canvas.mp4", 561, 81, 700, 550),
    ("beat4b", "beat4b-canvas.mp4", 570, 90, 810, 200)
]

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024 * 8), b""):
            h.update(chunk)
    return h.hexdigest()

def probe_video(path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_name,codec_type,width,height,r_frame_rate,nb_read_frames",
        "-show_entries", "format=duration",
        "-select_streams", "v:0",
        "-count_frames",
        "-of", "json", path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    
    # Check for audio streams
    audio_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_type,codec_name",
        "-select_streams", "a",
        "-of", "json", path
    ]
    audio_res = subprocess.run(audio_cmd, capture_output=True, text=True, check=True)
    audio_data = json.loads(audio_res.stdout)
    has_audio = len(audio_data.get("streams", [])) > 0
    
    vstream = data["streams"][0]
    return {
        "width": vstream["width"],
        "height": vstream["height"],
        "fps": vstream["r_frame_rate"],
        "frames": int(vstream["nb_read_frames"]),
        "duration": float(data["format"]["duration"]),
        "codec": vstream["codec_name"],
        "has_audio": has_audio
    }

def extract_boundary_stills():
    os.makedirs(VERIFY_DIR, exist_ok=True)
    for beat_prefix, video_name, global_frame, local_frame, crop_x, crop_y in STILL_SPECS:
        video_path = os.path.join(OUT_DIR, video_name)
        time_sec = local_frame / 30.0
        
        # 1. Full resolution boundary still
        still_name = f"{beat_prefix}_boundary_f{global_frame}.png"
        still_path = os.path.join(VERIFY_DIR, still_name)
        
        still_cmd = [
            "ffmpeg", "-y", "-ss", f"{time_sec:.6f}", "-i", video_path,
            "-frames:v", "1", "-update", "1", still_path
        ]
        subprocess.run(still_cmd, capture_output=True, text=True, check=True)
        
        # 2. 2x-upscaled crop of boundary region
        crop_name = f"{beat_prefix}_crop_f{global_frame}.png"
        crop_path = os.path.join(VERIFY_DIR, crop_name)
        
        # crop W=300, H=300, scale to 600x600 with neighbor
        crop_cmd = [
            "ffmpeg", "-y", "-ss", f"{time_sec:.6f}", "-i", video_path,
            "-vf", f"crop=300:300:{crop_x}:{crop_y},scale=600:600:flags=neighbor",
            "-frames:v", "1", "-update", "1", crop_path
        ]
        subprocess.run(crop_cmd, capture_output=True, text=True, check=True)
        print(f"Extracted still & crop for frame {global_frame} of {video_name}")

def generate_contact_sheet():
    assembled_path = os.path.join(OUT_DIR, "assembled.mp4")
    contact_path = os.path.join(VERIFY_DIR, "contact-sheet.jpg")
    
    cmd = [
        "ffmpeg", "-y", "-i", assembled_path,
        "-vf", "select='not(mod(n,20))',scale=320:180,tile=6x5",
        "-frames:v", "1", "-update", "1", contact_path
    ]
    subprocess.run(cmd, capture_output=True, text=True, check=True)
    print("Generated contact-sheet.jpg")

def main():
    print("Starting verification...")
    
    # 1. Compute input SHA-256 before doing anything else (or using stored post-run values)
    print("Computing input hashes...")
    mov_sha_before = sha256_of(SOURCE_MOV)
    mp4_sha_before = sha256_of(SOURCE_MP4)
    
    # Verify pre-run hashes are as expected
    if mov_sha_before != EXPECTED_MOV_SHA:
        print(f"ERROR: cutout-alpha.mov hash mismatch! Expected {EXPECTED_MOV_SHA}, got {mov_sha_before}")
        sys.exit(1)
    if mp4_sha_before != EXPECTED_MP4_SHA:
        print(f"ERROR: background-270-290.mp4 hash mismatch! Expected {EXPECTED_MP4_SHA}, got {mp4_sha_before}")
        sys.exit(1)
        
    # Generate boundary stills and crops
    print("Extracting boundary stills and crops...")
    extract_boundary_stills()
    
    # Generate contact sheet
    print("Generating contact sheet...")
    generate_contact_sheet()
    
    # Verify outputs
    print("Verifying output files...")
    overall_pass = True
    output_details = {}
    
    for filename, expected_frames, check_audio in OUTPUT_CONFIGS:
        path = os.path.join(OUT_DIR, filename)
        if not os.path.exists(path):
            print(f"ERROR: Output file missing: {filename}")
            overall_pass = False
            continue
            
        try:
            probe = probe_video(path)
            sha = sha256_of(path)
            
            checks = {
                "width": probe["width"] == 1920,
                "height": probe["height"] == 1080,
                "fps": probe["fps"] == "30/1",
                "frames": probe["frames"] == expected_frames,
                "codec": probe["codec"] == "h264",
                "audio": probe["has_audio"] if check_audio else True
            }
            
            file_pass = all(checks.values())
            if not file_pass:
                print(f"ERROR: {filename} failed checks: {checks} (probe data: {probe})")
                overall_pass = False
            else:
                print(f"OK: {filename} ({probe['frames']} frames, {probe['width']}x{probe['height']}, fps={probe['fps']}, codec={probe['codec']}, audio={probe['has_audio']})")
                
            output_details[filename] = {
                "sha256": sha,
                "size_bytes": os.path.getsize(path),
                "checks": checks,
                "probe": probe,
                "pass": file_pass
            }
        except Exception as e:
            print(f"ERROR parsing {filename}: {e}")
            overall_pass = False
            
    # Compute input SHA-256 after the run
    mov_sha_after = sha256_of(SOURCE_MOV)
    mp4_sha_after = sha256_of(SOURCE_MP4)
    
    inputs_unchanged = (mov_sha_before == mov_sha_after) and (mp4_sha_before == mp4_sha_after)
    if not inputs_unchanged:
        print("ERROR: Input files were modified during the run!")
        overall_pass = False
        
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "cutout-alpha.mov": {
                "path": SOURCE_MOV,
                "sha256_before": mov_sha_before,
                "sha256_after": mov_sha_after,
                "match": mov_sha_before == mov_sha_after
            },
            "background-270-290.mp4": {
                "path": SOURCE_MP4,
                "sha256_before": mp4_sha_before,
                "sha256_after": mp4_sha_after,
                "match": mp4_sha_before == mp4_sha_after
            }
        },
        "outputs": output_details,
        "overall_pass": overall_pass and inputs_unchanged
    }
    
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest written to {MANIFEST_PATH}")
    
    if manifest["overall_pass"]:
        print("VERIFICATION SUCCESSFUL")
        sys.exit(0)
    else:
        print("VERIFICATION FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
