# Example 1
class Dog:
    """A class representing a dog"""
    pass


# Example 2
class Book:
    """A class reperesenting a book"""
    
    def __init__(self, title, author):
        self.title = title
        self.author = author
    
    def get_info(self):
        """Returns information about a book"""
        return f"Book: '{self.title}' authorship {self.author}"
    
    def read(self, pages):
        """Simulates reading a book"""
        return f"Reading '{self.title}' - {pages} pages read"


# Example 3
class BankAccount:
    """A class representing a bank account"""
    
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance
    
    def deposit(self, amount):
        """Account replenishment"""
        if amount > 0:
            self.balance += amount
            return f"Account replenished by {amount}. New balance: {self.balance}"
        return "Amount must be positive"
    
    def withdraw(self, amount):
        """Withdrawal from account"""
        if 0 < amount <= self.balance:
            self.balance -= amount
            return f"Withdrawn {amount}. Remaining: {self.balance}"
        return "Insufficient funds or invalid amount"
    
    def get_balance(self):
        """Getting the current balance"""
        return f"Account balance: {self.balance}"


# Example 4
class Rectangle:
    """Класс, представляющий прямоугольник"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        """Вычисляет площадь"""
        return self.width * self.height
    
    def perimeter(self):
        """Вычисляет периметр"""
        return 2 * (self.width + self.height)
    
    def is_square(self):
        """Проверяет, является ли прямоугольник квадратом"""
        return self.width == self.height


# Example 5
class Student:
    """Class representing a student"""
    
    def __init__(self, name, student_id):
        self.name = name
        self.__student_id = student_id  # Private attribute
        self.__grades = [] # Private attribute
    
    def add_grade(self, grade):
        """Adds a grade"""
        if 0 <= grade <= 100:
            self.__grades.append(grade)
            return f"Grade {grade} added"
        return "Grade must be between 0 and 100"
    
    def get_average(self):
        """Calculates the average grade"""
        if not self.__grades:
            return 0
        return sum(self.__grades) / len(self.__grades)
    
    def get_student_info(self):
        """Returns student information (without private data)"""
        return f"Student: {self.name}, GPA: {self.get_average():.2f}"