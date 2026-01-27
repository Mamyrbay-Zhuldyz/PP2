#Example 1
for num in range(1, 11):
    if num % 2 == 0:
        continue
    print(f"Odd: {num}")


#Example 2
words = ["hello", "", "world", "", "python"]
for word in words:
    if word == "":
        continue
    print(word)


#Example 3
numbers = [5, -2, 0, 10, -8, 3]
for n in numbers:
    if n <= 0:
        continue
    print(f"Positive: {n}")


#Example 4
text = "programming"
for char in text:
    if char in "aeiou":
        continue
    print(char, end=" ")
print()


#Example 5
data = ["apple", 123, "banana", 0, "cherry", None]
for item in data:
    if not isinstance(item, str):
        continue
    print(f"String found: {item}")