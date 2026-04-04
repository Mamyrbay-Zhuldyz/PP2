#Example 1
my_list = [1, 2, 3, 4, 5]
my_iter = iter(my_list)
print(next(my_iter))  # 1
print(next(my_iter))  # 2

#Example 2
class CountDown:
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        self.n = self.start
        return self
    
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        current = self.n
        self.n -= 1
        return current

#Example 3
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

#Example 4
def fibonacci_generator(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

#Example 5
squares = (x * x for x in range(1, 6))