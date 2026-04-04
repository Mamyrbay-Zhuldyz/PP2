import os
import shutil
from pathlib import Path
from datetime import datetime

# Example 1: Copying file using shutil.copy()
if os.path.exists('output.txt'):
    shutil.copy('output.txt', 'output_copy.txt')
    print("File copied: output.txt → output_copy.txt")

# Example 2: Copying with metadata preservation (shutil.copy2())
if os.path.exists('fruits.txt'):
    shutil.copy2('fruits.txt', 'fruits_backup.txt')
    print("File copied with metadata: fruits.txt → fruits_backup.txt")

# Example 3: Safe file deletion with check
file_to_delete = 'temp_file.txt'

# Create test file
with open(file_to_delete, 'w') as f:
    f.write("This is a temporary file")

# Delete with check
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"File {file_to_delete} deleted")
else:
    print(f"File {file_to_delete} not found")

# Example 4: Creating backup with date stamp
if os.path.exists('user_info.txt'):
    # Create filename with current date
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"user_info_backup_{date_str}.txt"
    
    shutil.copy2('user_info.txt', backup_name)
    print(f"Backup created: {backup_name}")

# Example 5: Working with pathlib (modern approach)
source = Path('sample.txt')
destination = Path('backup/sample.txt')

# Create backup folder if it doesn't exist
destination.parent.mkdir(exist_ok=True)

if source.exists():
    shutil.copy2(source, destination)
    print(f"File copied using pathlib: {source} → {destination}")
    
    # Uncomment to delete via pathlib
    # destination.unlink()
    # print("File deleted using pathlib")