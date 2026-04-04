#Example 1
i = 1
while i <= 10:
    print(i)
    if i == 5:
        break
    i += 1


#Example 2
numbers = [1, 3, 5, 7, 9]
index = 0
while index < len(numbers):
    if numbers[index] == 7:
        print(f"Found 7 at position {index}")
        break
    index += 1


#Example 3
count = 0
while True:
    print(f"Loop {count}")
    count += 1
    if count >= 5:
        print("Breaking infinite loop")
        break


#Example 4
# (commented for safety)
# while True:
#     command = input("Enter command (quit to exit): ")
#     if command == "quit":
#         break
#     print(f"Executing: {command}")


#Example 5
total = 0
num = 1
while True:
    total += num
    if total > 20:
        print(f"Sum exceeded 20 at number {num}")
        break
    num += 1