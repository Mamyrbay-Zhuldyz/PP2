#Example 2
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
print(f"Score: {score}, Grade: {grade}")


#Example 2
hour = 14
if hour < 12:
    period = "morning"
elif hour < 18:
    period = "afternoon"
elif hour < 22:
    period = "evening"
else:
    period = "night"
print(f"At {hour}:00 it's {period}")


#Example 3
age = 25
if age < 13:
    category = "child"
elif age < 20:
    category = "teenager"
elif age < 65:
    category = "adult"
else:
    category = "senior"
print(f"Age {age}: {category}")


#Example 4
num = 0
if num > 0:
    print("Positive number")
elif num < 0:
    print("Negative number")
else:
    print("Zero")


#Example 5
amount = 150
if amount >= 200:
    discount = 20
elif amount >= 100:
    discount = 10
else:
    discount = 0
print(f"Purchase: ${amount}, Discount: {discount}%")