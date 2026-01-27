#Example 1
i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue
    print(f"Odd: {i}")


#Example 2
numbers = [1, 2, 3, 4, 5, 6]
i = 0
while i < len(numbers):
    if numbers[i] == 4:
        i += 1
        continue
    print(numbers[i])
    i += 1


#Example 3
data = [10, 0, 30, 0, 50]
index = 0
while index < len(data):
    if data[index] == 0:
        index += 1
        continue
    print(f"Processing {data[index]}")
    index += 1


#Example 4
text = "python programming"
i = 0
while i < len(text):
    if text[i] in "aeiou":
        i += 1
        continue
    print(text[i], end=" ")
    i += 1
print()


#Example 5
# (commented example)
# while True:
#     age = input("Enter age (positive number): ")
#     if not age.isdigit():
#         print("Invalid input")
#         continue
#     age = int(age)
#     if age <= 0:
#         print("Age must be positive")
#         continue
#     print(f"Your age is {age}")
#     break