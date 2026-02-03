# Example 1
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even = list(filter(lambda x: x % 2 == 0, numbers))

# Example 2
words = ["apple", "banana", "cat", "dog", "elephant"]
long_words = list(filter(lambda word: len(word) > 3, words))

# Example 3
numbers = [-10, -5, 0, 5, 10, 15]
positive = list(filter(lambda x: x > 0, numbers))

# Example 4
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
filtered = list(filter(lambda x: x > 3 and x < 8, numbers))

# Example 5
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78}
]
good_students = list(filter(lambda student: student["grade"] > 80, students))