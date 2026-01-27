n = int(input())
l = list(map(int, input().split()))
m = l[0]
for i in l:
    if m < i:
        m = i
for i in range(n):
    if m == l[i]:
        print(i + 1)
        break