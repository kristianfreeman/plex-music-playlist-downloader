#!/bin/bash

# Use filebot to rename files
# License required to run this script, sorry!

# Check if a path is provided
if [ -z "$1" ]; then
    echo "Please provide a path."
    exit 1
fi

# Use filebot to rename files
filebot -rename "$1" --format "{t} - {artist} - {album}" --db ID3
