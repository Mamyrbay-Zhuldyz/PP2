#Example 1
a, b = 5, 3
if a > b: print("a is greater than b")


#Example 2
age = 20
status = "adult" if age >= 18 else "minor"
print(f"Age {age}: {status}")


#Example 3
number = 10
result = "Positive" if number > 0 else "Zero" if number == 0 else "Negative"
print(f"{number} is {result}")


#Example 4
x = 15
message = "Big" if x > 10 else "Small"
print(f"x={x} is {message}")


#Example 5
score = 75
grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"
print(f"Score {score}: Grade {grade}")