#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# Create MP4 video from cover image + audio.
# Static image with audio overlay, YouTube-ready.
#
# Usage:
#   ./make_video.sh <basename>
#   ./make_video.sh 01_first_chapter
#
# Expects:
#   audiobook/<basename>.mp3
#   audiobook/<basename>_cover.png
#
# Output:
#   audiobook/<basename>.mp4
#
# Batch all chapters:
#   for mp3 in audiobook/*.mp3; do
#     base=$(basename "$mp3" .mp3)
#     [[ -f "audiobook/${base}_cover.png" ]] || continue
#     ./make_video.sh "$base"
#   done
# ─────────────────────────────────────────────

AUDIO_DIR="${AUDIO_DIR:-$(cd "$(dirname "$0")" && pwd)/audiobook}"

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <basename>"
    echo ""
    echo "Example: $0 01_first_chapter"
    echo "  Reads:  audiobook/01_first_chapter.mp3"
    echo "          audiobook/01_first_chapter_cover.png"
    echo "  Output: audiobook/01_first_chapter.mp4"
    exit 1
fi

BASENAME="$1"
COVER="$AUDIO_DIR/${BASENAME}_cover.png"
AUDIO="$AUDIO_DIR/${BASENAME}.mp3"
OUTPUT="$AUDIO_DIR/${BASENAME}.mp4"

[[ ! -f "$COVER" ]] && echo "Error: Cover not found: $COVER" && exit 1
[[ ! -f "$AUDIO" ]] && echo "Error: Audio not found: $AUDIO" && exit 1

if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is required. Install with: brew install ffmpeg"
    exit 1
fi

echo "────────────────────────────────────────"
echo "Cover:    $COVER"
echo "Audio:    $AUDIO"
echo "Output:   $OUTPUT"
echo "────────────────────────────────────────"

ffmpeg -y \
    -loop 1 \
    -i "$COVER" \
    -i "$AUDIO" \
    -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" \
    -c:v libx264 \
    -tune stillimage \
    -c:a aac \
    -b:a 192k \
    -pix_fmt yuv420p \
    -shortest \
    "$OUTPUT"

FILE_SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUTPUT" 2>/dev/null | cut -d. -f1)
MINUTES=$((DURATION / 60))
SECONDS=$((DURATION % 60))

echo ""
echo "Output:   $OUTPUT ($FILE_SIZE, ${MINUTES}m${SECONDS}s)"
echo "Done."
