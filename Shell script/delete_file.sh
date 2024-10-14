#!/bin/zsh
# Author: Raymond Li
# Description: A script that delete files with certain file extension from a source directory 

# Prompt for file name and URL
read "src?Enter the source directory (# Can fill in the pattern dst): "
read "file_extension?Enter the file extension (txt/png): "

# delete files matching the file extension
for file in "$src"/*; do
    if [[ "$(basename "$file")" == *"$file_extension" ]]; then
        rm "$file"
    fi
done