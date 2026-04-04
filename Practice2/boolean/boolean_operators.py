#Example 1
x = 5
print("x > 3 and x < 10:", x > 3 and x < 10)    # True
print("x > 3 and x < 4:", x > 3 and x < 4)      # False


#Example 2
print("x > 3 or x < 4:", x > 3 or x < 4)        # True
print("x > 10 or x < 0:", x > 10 or x < 0)      # False


#Example 3
print("not(x > 3):", not(x > 3))                # False
print("not(x > 10):", not(x > 10))              # True


#Example 4
age = 25
has_license = True
can_drive = age >= 18 and has_license
print(f"Age {age}, has license: {has_license}, can drive: {can_drive}")  # True


#Example 5
fruits = ["apple", "banana", "cherry"]
print("'banana' in fruits:", "banana" in fruits)        # True
print("'orange' in fruits:", "orange" in fruits)        # False
print("'mango' not in fruits:", "mango" not in fruits)  # True