n = int(input())
l = input().split()
k = input().split()
m = input()

for a, b in zip(l, k):
    if m == a:
        print(b)
    else:
        print("Not found")
        break