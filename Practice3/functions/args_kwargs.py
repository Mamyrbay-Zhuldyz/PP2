# Example 1
def show_items(*items):
    print("Elements:")
    for item in items:
        print(f" - {item}")

# Example 2
def make_pizza(size, *toppings):
    print(f"Pizza {size} с:")
    for topping in toppings:
        print(f"  - {topping}")

# Example 3
def create_person(**details):
    print("Information about a person:")
    for key, value in details.items():
        print(f"  {key}: {value}")

# Example 4
def order_info(customer, *items, **details):
    print(f"Order from: {customer}")
    print("Goods:", items)
    print("Details:", details)

# Example 5
def function_example(a, b, *args, c=10, **kwargs):
    print(f"a = {a}, b = {b}")
    print(f"args = {args}")
    print(f"c = {c}")
    print(f"kwargs = {kwargs}")