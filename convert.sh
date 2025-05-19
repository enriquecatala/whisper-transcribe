#!/bin/bash
# This recursively converts all .mp4 files inside a folder into .wav files
#
# Usage: ./convert.sh /path/to/input /path/to/output
# 

if [ $# -ne 2 ]; then
  echo "Usage: $0 <input_folder> <output_folder>"
  exit 1
fi

input_folder="$(realpath "$1")"
output_folder="$(realpath "$2")"

mkdir -p "$output_folder"

# Move into the input folder
cd "$input_folder" || exit 1

# Find all MP4 files, ignoring case, returning paths relative to the current dir
#find . -type f -iname "*.m4a" -print0 | while IFS= read -r -d '' relpath; do
find . -type f \( -iname "*.mp4" -o -iname "*.m4a" \) -print0 | while IFS= read -r -d '' relpath; do
    # Remove leading ./ if present
    relpath="${relpath#./}"
    # Strip extension
    base="${relpath%.*}"
    # Replace any slashes in subdirs with '-'
    base="${base//\//-}"

    # Full path for ffmpeg
    absolute_path="$input_folder/$relpath"
    # Output file
    output_file="$output_folder/${base}.wav"

    echo "Converting: $absolute_path -> $output_file"    
    ffmpeg -i "$absolute_path" -vn -acodec pcm_s16le -ar 44100 -ac 2 "$output_file" < /dev/null

done
