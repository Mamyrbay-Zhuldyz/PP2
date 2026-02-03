# Example 1
class Printable:
    def print_info(self):
        return "Information for printing"

# Example 2
class Savable:
    def save(self):
        return "Saved"

# Example 3
class Document(Printable, Savable):
    def __init__(self, content):
        self.content = content
    
    def print_info(self):
        return f"Document: {self.content}"

# Example 4
class Flyable:
    def fly(self):
        return "I'm flying!"

class Swimmable:
    def swim(self):
        return "I swim!"

class Duck(Flyable, Swimmable):
    def quack(self):
        return "Quack-quack!"

# Example 5
class Camera:
    def take_photo(self):
        return "Photo taken"

class Phone:
    def make_call(self):
        return "The call has been made"

class SmartPhone(Camera, Phone):
    def use_app(self):
        return "The application has been launched"