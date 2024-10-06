#!/bin/zsh
# Author: Raymond Li
# Description: A script that moves files with a specific pattern in their names 
# from a source directory to a destination directory.

# Prompt for file name and URL
read "src?Enter the source directory (# Can fill in the pattern for copy): "
read "dst?Enter the target directory (# Can fill in the pattern for copy): "
read "filename_pattern?Enter the file name pattern (# Can fill in the pattern for copy): "

# Move files matching the pattern
for file in "$src"/*; do
    if [[ "$(basename "$file")" == *"$filename_pattern"* ]]; then
        mv "$file" "$dst"
    fi
done