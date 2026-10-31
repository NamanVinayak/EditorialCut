#!/bin/bash
set -euo pipefail

cd <REDACTED-PATH>
FRAMES=frames
mkdir -p "$FRAMES"

# frame indices at 30fps for t = 0, 4, 8, 12, 16, 19.9 seconds
declare -a SECS=("00.0" "04.0" "08.0" "12.0" "16.0" "19.9")
declare -a IDXS=(0 120 240 360 480 597)

OUTPUTS=("01-conservative" "02-reference" "03-aggressive" "matte-reference")

for out in "${OUTPUTS[@]}"; do
  for i in "${!IDXS[@]}"; do
    idx="${IDXS[$i]}"
    sec="${SECS[$i]}"
    ffmpeg -y -v error -i "${out}.mp4" -vf "select=eq(n\,${idx})" -vframes 1 -update 1 \
      "${FRAMES}/${out}_${sec}s.jpg"
  done
done

# face crops at t=8s (frame 240) for the 3 treatment variants only, 700x500 around head
for out in "01-conservative" "02-reference" "03-aggressive"; do
  ffmpeg -y -v error -i "${out}.mp4" -vf "select=eq(n\,240),crop=700:500:650:0" -vframes 1 -update 1 \
    "${FRAMES}/${out}_face_08.0s.jpg"
done

echo "frames done:"
ls -la "$FRAMES" | wc -l

# Contact sheets: 3x2 grid per output, xstack with cumulative-sum layout
contact_num_for() {
  case "$1" in
    "01-conservative") echo "01" ;;
    "02-reference") echo "02" ;;
    "03-aggressive") echo "03" ;;
    "matte-reference") echo "04" ;;
  esac
}

for out in "${OUTPUTS[@]}"; do
  num="$(contact_num_for "$out")"
  f0="${FRAMES}/${out}_00.0s.jpg"
  f1="${FRAMES}/${out}_04.0s.jpg"
  f2="${FRAMES}/${out}_08.0s.jpg"
  f3="${FRAMES}/${out}_12.0s.jpg"
  f4="${FRAMES}/${out}_16.0s.jpg"
  f5="${FRAMES}/${out}_19.9s.jpg"
  ffmpeg -y -v error \
    -i "$f0" -i "$f1" -i "$f2" -i "$f3" -i "$f4" -i "$f5" \
    -filter_complex "
      [0:v]scale=640:360[v0];
      [1:v]scale=640:360[v1];
      [2:v]scale=640:360[v2];
      [3:v]scale=640:360[v3];
      [4:v]scale=640:360[v4];
      [5:v]scale=640:360[v5];
      [v0][v1][v2][v3][v4][v5]xstack=inputs=6:layout=0_0|w0_0|w0+w1_0|0_h0|w0_h0|w0+w1_h0[out]
    " -map "[out]" "contact-${num}.jpg"
done

echo "contact sheets done:"
ls -la contact-*.jpg
