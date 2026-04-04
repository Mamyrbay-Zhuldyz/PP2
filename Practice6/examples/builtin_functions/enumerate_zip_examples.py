# Example 1: enumerate() - add counter to iterable
fruits = ['apple', 'banana', 'cherry', 'date']

print("Enumerate examples:")
for i, fruit in enumerate(fruits):
    print(f"Index {i}: {fruit}")

# Start enumeration from 1
for i, fruit in enumerate(fruits, start=1):
    print(f"Item {i}: {fruit}")

# Example 2: zip() - combine multiple iterables
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
cities = ['New York', 'London', 'Tokyo']

print("\nZip examples:")
for name, age, city in zip(names, ages, cities):
    print(f"{name} is {age} years old, lives in {city}")

# Create list of tuples
combined = list(zip(names, ages))
print(f"Zipped list: {combined}")

# Example 3: Creating dictionaries with zip()
# Create dictionary from two lists
name_age_dict = dict(zip(names, ages))
print(f"\nDictionary from zip: {name_age_dict}")

# Create dictionary with enumerate
fruit_dict = {i: fruit for i, fruit in enumerate(fruits)}
print(f"Dictionary from enumerate: {fruit_dict}")

# Example 4: Unzipping with zip(*)
pairs = [('Alice', 25), ('Bob', 30), ('Charlie', 35)]
unzipped_names, unzipped_ages = zip(*pairs)

print(f"\nUnzipped names: {unzipped_names}")
print(f"Unzipped ages: {unzipped_ages}")

# Example 5: Practical applications
# Parallel iteration with different length lists
students = ['Alice', 'Bob', 'Charlie']
grades = [85, 92, 78, 88]  # Extra grade

print("\nParallel iteration with zip (stops at shortest):")
for student, grade in zip(students, grades):
    print(f"{student}: {grade}")

# Using enumerate with zip for numbered pairs
print("\nNumbered pairs:")
for i, (student, grade) in enumerate(zip(students, grades), 1):
    print(f"{i}. {student} - {grade}")

# Create HTML table rows
headers = ['Name', 'Age', 'City']
data = [
    ['Alice', 25, 'NYC'],
    ['Bob', 30, 'LA'],
    ['Charlie', 35, 'Chicago']
]

print("\nHTML table rows:")
for row in data:
    html_row = ''.join(f"<td>{item}</td>" for item in row)
    print(f"<tr>{html_row}</tr>")