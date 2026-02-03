# Example 1
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return "Animal sound"

# Example 2
class Dog(Animal):
    def speak(self):
        return "Woof-woof!"

# Example 3
class Cat(Animal):
    def speak(self):
        return "Meow!"

# Example 4
class Bird(Animal):
    def __init__(self, name, can_fly=True):
        super().__init__(name)
        self.can_fly = can_fly
    
    def speak(self):
        return "Chirp-chirp"

# Example 5
class Puppy(Dog):
    def speak(self):
        return "Woof-woof!"