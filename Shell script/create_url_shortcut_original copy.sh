#!/bin/zsh

# Prompt for file name and URL
read "filename?Enter the file name (without extension): "
read "url?Enter the URL: "

# Specify the directory where you want to save the file
directory=""  # Change this to your desired location

# Create the URL shortcut file
echo "[InternetShortcut]" > "$directory/$filename.url"
echo "URL=$url" >> "$directory/$filename.url"

echo "Shortcut created at $directory/$filename.url"

# Guideline:
# 1. make the script executable: chmod +x create_url_shortcut.sh
# 2. run the script: ./create_url_shortcut.sh