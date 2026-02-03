# Example 1
def student_info(name, age):
    print(f"Name: {name}, Age: {age}")

# Example 2
def greet_user(name="Guest"):
    print(f"Welcome, {name}!")

# Example 3
def create_user(username, email, is_active=True):
    print(f"User created: {username}, email: {email}")
    if is_active:
        print("Status: active")

# Example 4
def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

# Example 5
def build_profile(**info):
    for key, value in info.items():
        print(f"{key}: {value}")