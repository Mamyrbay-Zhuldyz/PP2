# Example 1
def square(n):
    return n * n

# Example 2
def get_greeting(name):
    return f"Привет, {name}!"

# Example 3
def get_min_max(numbers):
    return min(numbers), max(numbers)

# Example 4
def create_squares_list(n):
    squares = []
    for i in range(1, n + 1):
        squares.append(i * i)
    return squares

# Example 5
def check_value(x):
    if x > 0:
        return "Positive"
    elif x < 0:
        return "Negative"
    else:
        return "Ziro"