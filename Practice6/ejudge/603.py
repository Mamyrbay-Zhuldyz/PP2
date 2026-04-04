n = int(input())
l = list(map(str, input().split()))

result = []

for i, item in enumerate(l):
    result.append(f"{i}:{item}")

print(*result)
