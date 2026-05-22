#!/usr/bin/env bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PARENT_DIR="$(dirname -- "$(realpath -- "$SCRIPT_DIR")")"
TRANS=$PARENT_DIR/bin/transcribe_translate_cli
$TRANS "ToTranscribe/Sintel.2010.720p_part.mp4" -o "Transcribed" --source_lang en --target_lang de --translator "Argos" -f srt

