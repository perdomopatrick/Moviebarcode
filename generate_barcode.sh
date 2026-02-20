#!/bin/bash
INPUT="$1"
OUTPUT="$2"

START_TIME=$(date +%s)

DURATION=$(ffprobe -v error \
-show_entries format=duration \
-of default=noprint_wrappers=1:nokey=1 "$INPUT" \
| awk '{print int($1)}')
FRAMES=$DURATION

if [[ -z "$DURATION" || "$DURATION" -lt 1 ]]; then
    echo "Invalid duration (default to 1 frame)"
    FRAMES=1
fi

echo "-------------------------------------------------------"
echo "Generating Moviebarcode (1 slice/sec)"
echo "Input: $INPUT"
echo "Output: $OUTPUT"
echo "Frames: $FRAMES"
echo "-------------------------------------------------------"

ffmpeg -hide_banner -stats -an -i "$INPUT" \
-vf "fps=1,scale=160:-2:flags=fast_bilinear,scale=1:1:flags=area,scale=1:1080,tile=layout=${FRAMES}x1" \
-frames:v 1 \
-update 1 \
-fps_mode passthrough \
-threads 0 \
-y "$OUTPUT"

END_TIME=$(date +%s)
ELAPSED=$(( END_TIME - START_TIME ))

echo "-------------------------------------------------------"
echo "Finished in $(( ELAPSED / 60 ))m $(( ELAPSED % 60 ))s"
echo "-------------------------------------------------------"