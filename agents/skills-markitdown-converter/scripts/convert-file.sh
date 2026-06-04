#!/usr/bin/env bash
# convert-file.sh — Convert a file to Markdown and report stats
#
# Usage: bash convert-file.sh <input-file> [output-file]
#        bash convert-file.sh <input-file>             # to stdout
#        bash convert-file.sh <youtube-url>            # YouTube transcript
# Exit codes:
#   0 = success
#   1 = markitdown not installed
#   2 = input file not found
#   3 = conversion error

set +e

if [ -z "$1" ]; then
    echo "Usage: $0 <input-file-or-url> [output-file]"
    exit 1
fi

# Check markitdown
if ! command -v markitdown >/dev/null 2>&1; then
    echo "ERROR: markitdown not installed"
    echo "Install: pip install 'markitdown[all]'"
    exit 1
fi

INPUT="$1"
OUTPUT="${2:-}"

# If input is a local file, check existence
if [[ "$INPUT" != http* ]]; then
    if [ ! -f "$INPUT" ] && [ ! -L "$INPUT" ]; then
        echo "ERROR: file not found: $INPUT"
        exit 2
    fi
    FILE_SIZE=$(stat -c %s "$INPUT" 2>/dev/null || stat -f %z "$INPUT" 2>/dev/null)
    echo "Input: $INPUT (${FILE_SIZE} bytes)"
else
    echo "Input: $INPUT (URL)"
fi

# Convert
if [ -n "$OUTPUT" ]; then
    echo "Output: $OUTPUT"
    markitdown "$INPUT" -o "$OUTPUT"
    if [ $? -ne 0 ]; then
        echo "ERROR: conversion failed"
        exit 3
    fi
    OUTPUT_SIZE=$(stat -c %s "$OUTPUT" 2>/dev/null || stat -f %z "$OUTPUT" 2>/dev/null)
    echo "Output size: ${OUTPUT_SIZE} bytes"
    # Rough token estimate
    TOKENS=$((OUTPUT_SIZE / 4))
    echo "Approx tokens: ~${TOKENS}"
else
    # Stdout
    markitdown "$INPUT"
    if [ $? -ne 0 ]; then
        echo "ERROR: conversion failed"
        exit 3
    fi
fi

exit 0
