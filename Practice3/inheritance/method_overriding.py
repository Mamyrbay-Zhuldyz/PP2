# Example 1
class Shape:
    def area(self):
        return 0
    
    def perimeter(self):
        return 0

# Example 2
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# Example 3
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius * self.radius
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

# Example 4
class Vehicle:
    def start(self):
        return "The vehicle is started"

class Car(Vehicle):
    def start(self):
        base_result = super().start()
        return f"{base_result}. The engine is running"

# Example 5
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed