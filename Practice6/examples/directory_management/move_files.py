import os
import shutil
from pathlib import Path

# Setup: create test files and folders
os.makedirs('source_folder', exist_ok=True)
os.makedirs('destination_folder', exist_ok=True)
os.makedirs('backup_folder', exist_ok=True)

with open('source_folder/move_me.txt', 'w') as f:
    f.write("This file will be moved")
with open('source_folder/copy_me.txt', 'w') as f:
    f.write("This file will be copied")
with open('source_folder/rename_me.txt', 'w') as f:
    f.write("This file will be renamed")

# Example 1: Moving file (shutil.move)
if os.path.exists('source_folder/move_me.txt'):
    shutil.move('source_folder/move_me.txt', 'destination_folder/move_me.txt')
    print("File moved: source_folder/move_me.txt → destination_folder/move_me.txt")

# Example 2: Copying file (shutil.copy2)
if os.path.exists('source_folder/copy_me.txt'):
    shutil.copy2('source_folder/copy_me.txt', 'destination_folder/copy_me.txt')
    print("File copied: source_folder/copy_me.txt → destination_folder/copy_me.txt")

# Example 3: Renaming file (os.rename)
if os.path.exists('source_folder/rename_me.txt'):
    os.rename('source_folder/rename_me.txt', 'source_folder/renamed_file.txt')
    print("File renamed: rename_me.txt → renamed_file.txt")

# Example 4: Moving multiple files by pattern
# Create more test files
for i in range(3):
    with open(f'source_folder/doc_{i}.txt', 'w') as f:
        f.write(f"Document {i}")

# Find all .txt files and move them
txt_files = list(Path('source_folder').glob('*.txt'))
for file in txt_files:
    destination = Path('destination_folder') / file.name
    shutil.move(str(file), str(destination))
    print(f"Moved: {file.name}")

# Example 5: Moving with error handling
def safe_move_file(source, destination):
    """Safely move file with error handling"""
    try:
        if not os.path.exists(source):
            print(f"Source file {source} does not exist")
            return False
        
        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        shutil.move(source, destination)
        print(f"Successfully moved: {source} → {destination}")
        return True
        
    except PermissionError:
        print(f"Permission denied: cannot move {source}")
    except shutil.Error as e:
        print(f"Error during move: {e}")
    return False

# Test safe move
safe_move_file('non_existent.txt', 'destination_folder/')
safe_move_file('source_folder/doc_0.txt', 'destination_folder/doc_0.txt')