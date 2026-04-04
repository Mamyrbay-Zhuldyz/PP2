#Example 1
for num in range(1, 11):
    if num == 6:
        print("Stopping at 6")
        break
    print(num)


#Example 2
names = ["Alice", "Bob", "Charlie", "David"]
for name in names:
    if name == "Charlie":
        print("Found Charlie!")
        break
    print(f"Checking: {name}")


#Example 3
numbers = [15, 23, 8, 42, 4, 16]
for number in numbers:
    if number > 20:
        print(f"Found number > 20: {number}")
        break


#Example 4
for i in range(3):
    for j in range(3):
        if i == j == 1:
            print("Breaking at (1,1)")
            break
        print(f"({i}, {j})")


#Example 5
scores = [85, 92, 78, 60, 45, 95]
for score in scores:
    if score < 50:
        print(f"Failed score found: {score}")
        break
    print(f"Processing score: {score}")