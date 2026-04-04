a = int(input())
numbers = map(int, input().split())
new = list(map(lambda x:x**2, numbers))

result = sum(new)

print(result)