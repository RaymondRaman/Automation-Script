#!/bin/zsh

# Change src and dest to your desired location
src=""
dest=""

# Change target_file_name to the desired file name
target_file_name=""
for file in "$src"/*; do
    if [[ "$(basename "$file")" == *"target_file_name"* ]]; then 
        mv "$file" "$dest"
    fi
done