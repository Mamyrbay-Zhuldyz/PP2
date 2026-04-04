# Example 1: Parental class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"My name is {self.name}, I am {self.age} years old"

# Example 2: Child class with super()
class Student(Person):
    def __init__(self, name, age, student_id):
        # Calling the parent's constructor
        super().__init__(name, age)
        self.student_id = student_id
    
    def introduce(self):
        # Calling a parent method
        parent_intro = super().introduce()
        return f"{parent_intro}. Мой ID: {self.student_id}"

# Example 3
class Employee(Person):
    def __init__(self, name, age, position):
        super().__init__(name, age)
        self.position = position

# Example 4: Using super() in multi-level inheritance
class Manager(Employee):
    def __init__(self, name, age, position, department):
        super().__init__(name, age, position)
        self.department = department

# Example 5: Hierarchy of vehicles
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def get_info(self):
        return f"{self.brand} {self.model}"
    
    def start_engine(self):
        return "The engine is running"

class Car(Vehicle):
    def __init__(self, brand, model, doors):
        super().__init__(brand, model)
        self.doors = doors
    
    def get_info(self):
        base_info = super().get_info()
        return f"{base_info}, {self.doors} doors"
    
    def start_engine(self):
        base_result = super().start_engine()
        return f"{base_result}. The car is ready to go"

class ElectricCar(Car):
    def __init__(self, brand, model, doors, battery_capacity):
        super().__init__(brand, model, doors)
        self.battery_capacity = battery_capacity
    
    def get_info(self):
        car_info = super().get_info()
        return f"{car_info}, Battery: {self.battery_capacity} kWh"
    
    def start_engine(self):
        # We skip the call to Car.start engine() and call Vehicle.start engine()
        vehicle_result = super(Car, self).start_engine()
        return f"{vehicle_result}. The electric car is ready (silently)"