a = int(input())
numbers = list(map(int, input().split()))

def only_even(arr):
    return arr%2==0

result = list(filter(only_even, numbers))

print(len(result))