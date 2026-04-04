from functools import reduce

# Example 1: map() - apply function to all items
numbers = [1, 2, 3, 4, 5]

# Double each number
doubled = list(map(lambda x: x * 2, numbers))
print(f"Original: {numbers}")
print(f"Doubled (map): {doubled}")

# Convert to strings
str_numbers = list(map(str, numbers))
print(f"As strings: {str_numbers}")

# Example 2: filter() - filter items based on condition
# Get even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"\nEven numbers (filter): {evens}")

# Get numbers greater than 3
greater_than_3 = list(filter(lambda x: x > 3, numbers))
print(f"Numbers > 3: {greater_than_3}")

# Example 3: reduce() - reduce list to single value
# Sum all numbers
total = reduce(lambda x, y: x + y, numbers)
print(f"\nSum (reduce): {total}")

# Find maximum number
maximum = reduce(lambda x, y: x if x > y else y, numbers)
print(f"Maximum (reduce): {maximum}")

# Example 4: Combining map, filter, and reduce
# Get sum of squares of even numbers
result = reduce(
    lambda x, y: x + y,
    map(
        lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, numbers)
    )
)
print(f"\nSum of squares of even numbers: {result}")

# Example 5: Practical examples with strings
words = ["apple", "banana", "cherry", "date"]

# Get word lengths
lengths = list(map(len, words))
print(f"\nWord lengths: {lengths}")

# Get words longer than 5 characters
long_words = list(filter(lambda w: len(w) > 5, words))
print(f"Long words: {long_words}")

# Concatenate all words
all_words = reduce(lambda x, y: x + ", " + y, words)
print(f"All words joined: {all_words}")