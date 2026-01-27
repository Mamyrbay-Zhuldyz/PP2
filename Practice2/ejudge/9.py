n = int(input())
l = list(map(int, input(). split()))
m1 = l[0]
m2 = l[0]
for i in l:
    if m1 > i:
        m1 = i
for i in l:
    if m2 < i:
        m2 = i
for i in range(n):
    if l[i] == m2:
        l[i] = m1
print(*l)