n = int(input())
l = list(map(str, input().split()))

r = max(l, key=len)

print(r)