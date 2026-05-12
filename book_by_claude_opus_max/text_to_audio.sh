#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# Convert a single chapter markdown file to MP3
# using Amazon Polly.
#
# Usage:
#   ./text_to_audio.sh <chapter_file.md> [voice] [engine]
#
# Examples:
#   ./text_to_audio.sh 00_prelude.md
#   ./text_to_audio.sh 01_the_coincidence.md Matthew
#   ./text_to_audio.sh 00_prelude.md Ruth generative
#
# Defaults: Voice=Ruth, Engine=neural, Region=us-east-1
# ─────────────────────────────────────────────

VOICE="${2:-Ruth}"
ENGINE="${3:-neural}"
REGION="us-east-1"
OUTPUT_DIR="$(cd "$(dirname "$0")" && pwd)/audiobook"
POLLY_CHAR_LIMIT=2900

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <chapter.md> [voice] [engine]"
    echo ""
    echo "Voices (en-US): Ruth, Matthew, Danielle, Stephen, Gregory, Joanna, Salli"
    echo "Engines: neural (\$16/1M chars), generative (best, \$30/1M chars)"
    exit 1
fi

INPUT_FILE="$1"
[[ ! -f "$INPUT_FILE" ]] && echo "Error: File not found: $INPUT_FILE" && exit 1

mkdir -p "$OUTPUT_DIR"
BASENAME="$(basename "$INPUT_FILE" .md)"
FINAL_OUTPUT="$OUTPUT_DIR/${BASENAME}.mp3"

echo "────────────────────────────────────────"
echo "Chapter:  $INPUT_FILE"
echo "Voice:    $VOICE"
echo "Engine:   $ENGINE"
echo "Output:   $FINAL_OUTPUT"
echo "────────────────────────────────────────"

# ─── Clean markdown to plain text via python (robust) ───
CLEAN_TEXT=$(python3 -c "
import re, sys

text = open(sys.argv[1], 'r').read()

# Strip markdown
text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
text = re.sub(r'\*(.+?)\*', r'\1', text)
text = re.sub(r'\`[^\`]+\`', '', text)
text = re.sub(r'~~(.+?)~~', r'\1', text)
text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)
text = re.sub(r'^[-=]{3,}$', '', text, flags=re.MULTILINE)

# Collapse whitespace runs but preserve paragraph breaks
text = re.sub(r'\n{3,}', '\n\n', text)
text = text.strip()
print(text)
" "$INPUT_FILE")

TOTAL_CHARS=${#CLEAN_TEXT}
echo "Characters: $TOTAL_CHARS"

# ─── Split into chunks at paragraph boundaries ───
CHUNK_DIR=$(mktemp -d)
trap "rm -rf $CHUNK_DIR" EXIT

python3 -c "
import sys, os

text = sys.stdin.read()
limit = int(sys.argv[1])
outdir = sys.argv[2]

paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

chunks = []
current = ''
for para in paragraphs:
    candidate = (current + ' ' + para).strip() if current else para
    if len(candidate) > limit and current:
        chunks.append(current)
        current = para
    else:
        current = candidate

if current:
    chunks.append(current)

for i, chunk in enumerate(chunks, 1):
    with open(os.path.join(outdir, f'chunk_{i:03d}.txt'), 'w') as f:
        f.write(chunk)

print(len(chunks))
" "$POLLY_CHAR_LIMIT" "$CHUNK_DIR" <<< "$CLEAN_TEXT"

CHUNK_COUNT=$(ls "$CHUNK_DIR"/chunk_*.txt 2>/dev/null | wc -l | tr -d ' ')
echo "Chunks:     $CHUNK_COUNT"
echo ""

# ─── Synthesize each chunk ───
PART_NUM=0
for CHUNK_FILE in "$CHUNK_DIR"/chunk_*.txt; do
    PART_NUM=$((PART_NUM + 1))
    PART_OUTPUT="$CHUNK_DIR/part_$(printf '%03d' $PART_NUM).mp3"
    CHARS=$(wc -c < "$CHUNK_FILE" | tr -d ' ')

    echo -n "  Part $PART_NUM/$CHUNK_COUNT (${CHARS} chars)... "

    aws polly synthesize-speech \
        --region "$REGION" \
        --output-format mp3 \
        --voice-id "$VOICE" \
        --engine "$ENGINE" \
        --text-type text \
        --text file://"$CHUNK_FILE" \
        "$PART_OUTPUT" > /dev/null 2>&1

    echo "done"
done

# ─── Concatenate ───
if [[ $PART_NUM -eq 1 ]]; then
    cp "$CHUNK_DIR/part_001.mp3" "$FINAL_OUTPUT"
else
    echo ""
    echo "Concatenating $PART_NUM parts..."
    if command -v ffmpeg &> /dev/null; then
        CONCAT_LIST="$CHUNK_DIR/concat.txt"
        for f in "$CHUNK_DIR"/part_*.mp3; do
            echo "file '$f'" >> "$CONCAT_LIST"
        done
        ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" -c copy "$FINAL_OUTPUT" 2>/dev/null
    else
        cat "$CHUNK_DIR"/part_*.mp3 > "$FINAL_OUTPUT"
    fi
fi

FILE_SIZE=$(ls -lh "$FINAL_OUTPUT" | awk '{print $5}')
echo ""
echo "Output: $FINAL_OUTPUT ($FILE_SIZE)"
echo "Done."
