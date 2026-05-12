#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# Convert a chapter to MP3 with multiple voices
# for dialogue. Uses Amazon Polly generative engine.
#
# Usage:
#   ./text_to_audio_multivoice.sh <chapter.md>
#
# Voice assignments (generative engine, en-US):
#   Narrator:  Ruth     (female, warm, authoritative)
#   Maya:      Danielle (female, younger)
#   Morrison:  Stephen  (male, measured)
#   Ravi:      Matthew  (male)
#   Elena:     Joanna   (female, precise)
#   Sarah:     Salli    (female, direct)
#   Amara:     Ruth     (female — reuse narrator, distinct in context)
#   Marcus:    Matthew  (male)
#   River:     Danielle (female — non-binary, lighter voice)
#   Zero:      Stephen  (male, calm)
#   Torres:    Gregory  (male, authoritative)
# ─────────────────────────────────────────────

ENGINE="generative"
REGION="us-east-1"
OUTPUT_DIR="$(cd "$(dirname "$0")" && pwd)/audiobook"

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <chapter.md>"
    exit 1
fi

INPUT_FILE="$1"
[[ ! -f "$INPUT_FILE" ]] && echo "Error: File not found: $INPUT_FILE" && exit 1

mkdir -p "$OUTPUT_DIR"
BASENAME="$(basename "$INPUT_FILE" .md)"
FINAL_OUTPUT="$OUTPUT_DIR/${BASENAME}.mp3"
WORK_DIR=$(mktemp -d)
trap "rm -rf $WORK_DIR" EXIT

echo "────────────────────────────────────────"
echo "Chapter:  $INPUT_FILE"
echo "Engine:   $ENGINE (multi-voice)"
echo "Output:   $FINAL_OUTPUT"
echo "────────────────────────────────────────"

# ─── Parse chapter into voice-tagged segments via Python ───
python3 - "$INPUT_FILE" "$WORK_DIR" << 'PYTHON_SCRIPT'
import re, sys, os, json

input_file = sys.argv[1]
work_dir = sys.argv[2]

VOICE_MAP = {
    "narrator": "Ruth",
    "maya": "Danielle",
    "morrison": "Stephen",
    "ravi": "Matthew",
    "elena": "Joanna",
    "sarah": "Salli",
    "amara": "Ruth",
    "marcus": "Matthew",
    "river": "Danielle",
    "zero": "Stephen",
    "torres": "Matthew",
    "kenji": "Matthew",
    "priya": "Joanna",
}

def strip_markdown(text):
    text = re.sub(r'^#{1,6}\s+.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`[^`]+`', '', text)
    text = re.sub(r'~~(.+?)~~', r'\1', text)
    text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[-=]{3,}$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def identify_speaker(line, prev_speaker, context_lines):
    """Identify who is speaking a quoted line based on attribution."""
    line_lower = line.lower()

    # Direct attribution patterns: "text," Character said / Character: "text"
    attr_patterns = [
        (r'maya|chen', 'maya'),
        (r'morrison|james', 'morrison'),
        (r'ravi|chandrasekaran', 'ravi'),
        (r'elena|vasquez', 'elena'),
        (r'sarah|park', 'sarah'),
        (r'amara|okafor', 'amara'),
        (r'marcus|zhang', 'marcus'),
        (r'river|nakamura', 'river'),
        (r'torres|colonel', 'torres'),
        (r'kenji|watanabe', 'kenji'),
        (r'priya|sen', 'priya'),
    ]

    # Check surrounding context (2 lines before/after) for character names
    context = ' '.join(context_lines).lower()
    for pattern, speaker in attr_patterns:
        if re.search(pattern, context):
            # Check if this is attribution (said, asked, replied, etc.)
            if re.search(rf'{pattern}.{{0,30}}(said|asked|replied|answered|continued|called|whispered|muttered|told)', context):
                return speaker
            if re.search(rf'(said|asked|replied|answered|continued) .{{0,20}}{pattern}', context):
                return speaker

    # Alternating dialogue: if we know previous speaker, alternate
    if prev_speaker and prev_speaker != 'narrator':
        return prev_speaker  # keep same until context switch

    return prev_speaker or 'narrator'

def parse_into_segments(text):
    """Parse text into (voice, text) segments."""
    lines = text.split('\n')
    segments = []
    current_voice = 'narrator'
    current_text = []
    last_dialogue_speaker = None

    # Track recent context for attribution
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            if current_text:
                current_text.append('')
            i += 1
            continue

        # Check if this line is dialogue (starts with " or \u201c)
        is_dialogue = bool(re.match(r'^[\u201c""]', line))

        if is_dialogue:
            # Flush narrator buffer
            if current_text and current_voice == 'narrator':
                segments.append(('narrator', ' '.join(t for t in current_text if t)))
                current_text = []

            # Get context: surrounding lines for attribution
            context_start = max(0, i - 2)
            context_end = min(len(lines), i + 2)
            context_lines = lines[context_start:context_end]

            # Determine speaker
            speaker = identify_speaker(line, last_dialogue_speaker, context_lines)

            # Check for explicit speaker switch in the SAME line or next
            full_context = ' '.join(lines[max(0,i-1):min(len(lines),i+2)])
            full_lower = full_context.lower()

            # Maya speaking patterns
            if any(x in full_lower for x in ['maya said', 'maya asked', 'she said', 'she asked', 'chen said']):
                if last_dialogue_speaker != 'maya':
                    speaker = 'maya'
            # Morrison speaking
            elif any(x in full_lower for x in ['morrison said', 'morrison asked', 'he said', 'he asked', 'james said']):
                if last_dialogue_speaker not in ('ravi',):
                    speaker = 'morrison'
            # Ravi speaking
            elif any(x in full_lower for x in ['ravi', 'chandrasekaran']):
                speaker = 'ravi'

            # Simple alternation for rapid back-and-forth
            if speaker == last_dialogue_speaker or speaker == 'narrator':
                # Try to alternate based on conversation participants
                pass

            last_dialogue_speaker = speaker if speaker != 'narrator' else last_dialogue_speaker
            segments.append((speaker if speaker != 'narrator' else (last_dialogue_speaker or 'narrator'), line))
            current_voice = 'narrator'
        else:
            # Check if this line contains inline dialogue
            # e.g.: Morrison said, "Something something"
            inline_match = re.search(r'[\u201c""](.+?)[\u201d""]', line)
            if inline_match:
                # Split: narration before quote, quote, narration after
                # For simplicity, keep as narrator with the full line
                current_text.append(line)
            else:
                current_text.append(line)

        i += 1

    # Flush remaining
    if current_text:
        segments.append(('narrator', ' '.join(t for t in current_text if t)))

    return segments

# ─── Main ───
with open(input_file, 'r') as f:
    raw = f.read()

text = strip_markdown(raw)
segments = parse_into_segments(text)

# Merge consecutive same-voice segments
merged = []
for voice, text in segments:
    text = text.strip()
    if not text:
        continue
    if merged and merged[-1][0] == voice:
        merged[-1] = (voice, merged[-1][1] + ' ' + text)
    else:
        merged.append((voice, text))

# Split any segment over 2900 chars
LIMIT = 2900
final_segments = []
for voice, text in merged:
    if len(text) <= LIMIT:
        final_segments.append((voice, text))
    else:
        # Split at sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunk = ''
        for sent in sentences:
            if len(chunk) + len(sent) + 1 > LIMIT and chunk:
                final_segments.append((voice, chunk.strip()))
                chunk = sent
            else:
                chunk = chunk + ' ' + sent if chunk else sent
        if chunk:
            final_segments.append((voice, chunk.strip()))

# Write segment files
manifest = []
for idx, (voice, text) in enumerate(final_segments, 1):
    polly_voice = VOICE_MAP.get(voice, 'Ruth')
    seg_file = os.path.join(work_dir, f'seg_{idx:04d}.txt')
    with open(seg_file, 'w') as f:
        f.write(text)
    manifest.append({'idx': idx, 'voice': polly_voice, 'speaker': voice, 'chars': len(text), 'file': seg_file})

# Write manifest
manifest_file = os.path.join(work_dir, 'manifest.json')
with open(manifest_file, 'w') as f:
    json.dump(manifest, f)

print(f"Segments: {len(final_segments)}")
voices_used = set(v for v, _ in final_segments)
print(f"Voices:   {', '.join(sorted(voices_used))}")
total_chars = sum(len(t) for _, t in final_segments)
print(f"Chars:    {total_chars}")
PYTHON_SCRIPT

echo ""

# ─── Synthesize each segment ───
MANIFEST="$WORK_DIR/manifest.json"
TOTAL=$(python3 -c "import json; print(len(json.load(open('$MANIFEST'))))")

echo "Synthesizing $TOTAL segments..."
echo ""

SEG_IDX=0
while IFS= read -r entry; do
    SEG_IDX=$((SEG_IDX + 1))
    VOICE=$(echo "$entry" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['voice'])")
    SPEAKER=$(echo "$entry" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['speaker'])")
    CHARS=$(echo "$entry" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['chars'])")
    SEG_FILE=$(echo "$entry" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['file'])")
    PART_OUTPUT="$WORK_DIR/part_$(printf '%04d' $SEG_IDX).mp3"

    echo -n "  [$SEG_IDX/$TOTAL] $SPEAKER ($VOICE) ${CHARS} chars... "

    aws polly synthesize-speech \
        --region "$REGION" \
        --output-format mp3 \
        --voice-id "$VOICE" \
        --engine "$ENGINE" \
        --text-type text \
        --text file://"$SEG_FILE" \
        "$PART_OUTPUT" > /dev/null 2>&1

    echo "done"
done < <(python3 -c "
import json
manifest = json.load(open('$MANIFEST'))
for entry in manifest:
    print(json.dumps(entry))
")

# ─── Concatenate ───
echo ""
echo "Concatenating..."

if command -v ffmpeg &> /dev/null; then
    CONCAT_LIST="$WORK_DIR/concat.txt"
    for f in "$WORK_DIR"/part_*.mp3; do
        echo "file '$f'" >> "$CONCAT_LIST"
    done
    ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" -c copy "$FINAL_OUTPUT" 2>/dev/null
else
    cat "$WORK_DIR"/part_*.mp3 > "$FINAL_OUTPUT"
fi

FILE_SIZE=$(ls -lh "$FINAL_OUTPUT" | awk '{print $5}')
echo ""
echo "Output: $FINAL_OUTPUT ($FILE_SIZE)"
echo "Done."
