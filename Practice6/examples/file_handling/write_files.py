# Example 1: Writing to file (mode 'w' - overwrite)
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write("Hello, World!\n")
    file.write("This is the second line.\n")
    file.write("And this is the third line.\n")
print("File output.txt created and filled")

# Example 2: Appending to file (mode 'a' - append)
with open('output.txt', 'a', encoding='utf-8') as file:
    file.write("This line was added later.\n")
    file.write("One more line at the end of file.\n")
print("Data appended to the end of file")

# Example 3: Writing a list of strings
lines = ["Apple", "Banana", "Orange", "Pear"]
with open('fruits.txt', 'w', encoding='utf-8') as file:
    for line in lines:
        file.write(line + '\n')
print("Fruit list written to file")

# Example 4: Creating a new file (mode 'x' - only if file doesn't exist)
try:
    with open('new_file.txt', 'x', encoding='utf-8') as file:
        file.write("This is a new file created with 'x' mode")
    print("New file created successfully")
except FileExistsError:
    print("File already exists!")

# Example 5: Writing different data types
name = "Anna"
age = 25
city = "Almaty"

with open('user_info.txt', 'w', encoding='utf-8') as file:
    file.write(f"Name: {name}\n")
    file.write(f"Age: {age}\n")
    file.write(f"City: {city}\n")
    file.write(f"Date: 2026-03-17\n")
print("User information saved")