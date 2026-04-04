n = int(input())
l = input().split()
k = input().split()
m = input()

flag = False

for a, b in zip(l, k):
    if m == a:
        print(b)
        flag = True

if not flag:
    print("Not found")