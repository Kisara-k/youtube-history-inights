"""
Script to find and copy history.json files from subdirectories to the root directory.

This script searches through all subdirectories starting from the script's location
for files named 'history.json' and copies them to the root directory where the script is run.

Example:
    If you have a directory structure like:
    root/
        folder1/
            history.json
        folder2/
            subfolder/
                history.json
    
    Running this script will result in:
    root/
        folder1/
            history.json
        folder2/
            subfolder/
                history.json
        history.json           # Copy from folder1
        history_1.json       # Copy from folder2/subfolder

Usage:
    Simply run the script from the directory containing the subdirectories with history files.
    The script will automatically find and copy all history.json files to the current directory.
"""

import os
import shutil

def find_history_files(root):
    for dirpath, _, filenames in os.walk(root):
        if dirpath == root:
            continue
        for filename in filenames:
            if filename.endswith('history.json'):
                yield os.path.join(dirpath, filename)

def copy_files_to_root(files, root, rename_on_conflict=False):
    for src in files:
        base = os.path.basename(src)
        dst = os.path.join(root, base)

        # Failsafe if prefixing is not applied, it will suffix duplicate files with _1, _2, etc.
        if rename_on_conflict:
            count = 1
            while os.path.exists(dst):
                name, ext = os.path.splitext(base)
                dst = os.path.join(root, f"{name}_{count}{ext}")
                count += 1
        
        shutil.copy2(src, dst)

if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    files = find_history_files(root)
    copy_files_to_root(files, root)
