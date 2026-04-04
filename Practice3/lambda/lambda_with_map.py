# Example 1
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))

# Exampl 2
words = ["apple", "banana", "cherry"]
uppercase = list(map(lambda word: word.upper(), words))

# Example 3
words = ["cat", "elephant", "dog"]
lengths = list(map(lambda word: len(word), words))

# Example 4
celsius = [0, 20, 30, 100]
fahrenheit = list(map(lambda c: c * 9/5 + 32, celsius))

# Example 5
list1 = [1, 2, 3]
list2 = [10, 20, 30]
sums = list(map(lambda x, y: x + y, list1, list2))