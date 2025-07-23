"""
Script to add prefixes to files based on their parent directory names.

This script processes directories where the top-level folders have a specific naming pattern
(a short 2-4 character prefix followed by a space and the rest of the name). It then adds
this prefix to all files within those directories, preventing duplicate prefixes.

Example:
    If you have a directory structure like:
    AB folder name/
        file1.json
        subfolder/
            file2.json
    
    Running this script will rename the files to:
    AB folder name/
        AB file1.json
        subfolder/
            AB file2.json

Usage:
    Simply run the script from the directory containing the folders you want to process.
    The script will automatically process all valid directories in the current working directory.
"""

import os

def is_prefixed_folder(folder_name):
    parts = folder_name.split(' ', 1)
    return len(parts) == 2 and 2 <= len(parts[0]) <= 4

def rename_files_with_prefix(base_path):
    for item in os.listdir(base_path):
        top_level_path = os.path.join(base_path, item)
        if os.path.isdir(top_level_path) and is_prefixed_folder(item):
            prefix = item.split(' ', 1)[0] + ' '
            for root, _, files in os.walk(top_level_path):
                for file in files:
                    old_path = os.path.join(root, file)
                    if not file.startswith(prefix):  # Prevent double-prefixing
                        new_name = prefix + file
                        new_path = os.path.join(root, new_name)
                        os.rename(old_path, new_path)
                        print(f"Renamed: {old_path} -> {new_path}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    rename_files_with_prefix(current_dir)
