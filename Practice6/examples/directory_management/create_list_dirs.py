import os
from pathlib import Path

# Example 1: Creating a single directory
try:
    os.mkdir('test_folder')
    print("Folder 'test_folder' created")
except FileExistsError:
    print("Folder already exists")

# Example 2: Creating nested directories (makedirs)
os.makedirs('projects/2026/march/week3', exist_ok=True)
print("Nested folders created: projects/2026/march/week3")

# Example 3: Getting directory information
current_dir = os.getcwd()
print(f"\nCurrent directory: {current_dir}")

# List files and folders
items = os.listdir('.')
print(f"Contents of current folder: {items}")

# Filter only directories
folders = [item for item in items if os.path.isdir(item)]
print(f"Only folders: {folders}")

# Example 4: Changing directory and verification
print(f"\nCurrent directory: {os.getcwd()}")

# Create and navigate to new folder
os.makedirs('temp_dir', exist_ok=True)
os.chdir('temp_dir')
print(f"After changing directory: {os.getcwd()}")

# Go back
os.chdir('..')
print(f"After returning: {os.getcwd()}")

# Example 5: Finding files by extension
def find_files_by_extension(extension='.txt'):
    """Finds all files with specified extension"""
    found_files = []
    for file in os.listdir('.'):
        if file.endswith(extension):
            found_files.append(file)
    return found_files

txt_files = find_files_by_extension('.txt')
print(f"\nFound .txt files: {txt_files}")

# Using pathlib
path = Path('.')
py_files = list(path.glob('*.py'))
print(f"Found .py files: {[p.name for p in py_files]}")