n = int(input())
l = list(map(int, input().split()))

r = all(x>=0 for x in l)

if r:
    print("Yes")
else:
    print("No")