# Example 1
class Car:
    wheels = 4
    
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

# Example 2
class Student:
    school = "Моя школа"
    
    def __init__(self, name):
        self.name = name

# Example 3
class Book:
    total_books = 0
    
    def __init__(self, title):
        self.title = title
        Book.total_books += 1

# Example 4
class Configuration:
    language = "Russian"
    theme = "Light"
    
    def __init__(self, user):
        self.user = user

# Example 5
class Circle:
    PI = 3.14159
    
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return self.PI * self.radius * self.radius