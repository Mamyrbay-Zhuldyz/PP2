#Example 1
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)


#Example 2
word = "Python"
for char in word:
    print(char)


#Example 3
for i in range(5):
    print(i)

for i in range(2, 6):
    print(f"Number: {i}")

for i in range(1, 10, 2):  # step 2
    print(f"Odd: {i}")


#Example 4
colors = ["red", "green", "blue"]
for index, color in enumerate(colors):
    print(f"Index {index}: {color}")


#Example 5
person = {"name": "Alice", "age": 25, "city": "NYC"}
for key, value in person.items():
    print(f"{key}: {value}")