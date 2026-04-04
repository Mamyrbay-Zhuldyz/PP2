# Example 1: Reading entire file at once
with open('sample.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print("Entire file content:")
    print(content)

# Example 2: Reading file line by line (method 1)
with open('sample.txt', 'r', encoding='utf-8') as file:
    print("\nReading line by line (method 1):")
    for line in file:
        print(f"Line: {line.strip()}")

# Example 3: Reading with readline() method
with open('sample.txt', 'r', encoding='utf-8') as file:
    print("\nReading with readline():")
    line = file.readline()
    while line:
        print(f"→ {line.strip()}")
        line = file.readline()

# Example 4: Reading all lines into a list with readlines()
with open('sample.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    print(f"\nTotal lines: {len(lines)}")
    print(f"First 3 lines: {lines[:3]}")

# Example 5: Reading with error handling
try:
    with open('non_existent_file.txt', 'r', encoding='utf-8') as file:
        content = file.read()
except FileNotFoundError:
    print("\nError: File not found!")
except PermissionError:
    print("Error: No permission to read file!")