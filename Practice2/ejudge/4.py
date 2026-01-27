n = int(input())
l = list(map(int, input().split()))
s = 0
for i in l:
    if i > 0:
        s += 1
print(s)