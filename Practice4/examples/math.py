#Example 1
numbers = [5, 2, 8, 1, 9]
print(min(numbers))
print(max(numbers))
print(abs(-10))
print(round(3.14159, 2))
print(pow(2, 3))

#Example 2
import math

print(math.sqrt(16))
print(math.ceil(4.2))
print(math.floor(4.7))
print(math.pi)
print(math.sin(math.pi/2))

#Example 3
import random

print(random.random())
print(random.randint(1, 10))
print(random.choice(['red', 'blue', 'green']))

#Example 4
import random

cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
random.shuffle(cards)
print(cards)

#Example 5
import random

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sample = random.sample(numbers, 3)