# Example 1
words = ["apple", "banana", "cherry", "date"]
sorted_by_length = sorted(words, key=lambda x: len(x))

# Example 2
words = ["apple", "banana", "cherry", "date"]
sorted_by_last = sorted(words, key=lambda x: x[-1])

# Example 3
numbers = [-10, 5, -3, 15, -1]
sorted_by_abs = sorted(numbers, key=lambda x: abs(x))

# Example 4
students = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 22},
    {"name": "Charlie", "age": 23}
]
sorted_by_age = sorted(students, key=lambda x: x["age"])

# Example 5
people = [
    ("Alice", 25),
    ("Bob", 30),
    ("Charlie", 25),
    ("Diana", 30)
]
sorted_people = sorted(people, key=lambda x: (x[1], x[0]))