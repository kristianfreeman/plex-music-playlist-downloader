#!/bin/bash

# Rename all .wav and .flac files to 320kbps MP3 using ffmpeg
# This is a destructive operation and isn't super efficient if you
# run the python script multiple times

# Check if a path is provided
if [ -z "$1" ]; then
    echo "Please provide a path."
    exit 1
fi

# Whitelisted file extensions
declare -a extensions=("wav" "flac")

# Counter for processed files
count=0

# Loop through files in the provided path
for ext in "${extensions[@]}"; do
    for file in "$1"/*.$ext; do
        # Check if file exists
        if [ -f "$file" ]; then
            # Check if the MP3 file already exists
            if [ -f "${file%.*}.mp3" ]; then
                echo "File already exists: ${file%.*}.mp3"
                rm "$file"
                continue
            fi

            # Convert to 320kbps MP3 and delete original
            ffmpeg -hide_banner -loglevel error -i "$file" -ab 320k -map_metadata 0 -id3v2_version 3 "${file%.*}.mp3" && rm "$file"
            ((count++))
        fi
    done
done

# Output the total number of processed files
echo "Total files processed: $count"
