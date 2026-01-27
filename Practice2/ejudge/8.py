n = int(input())
i = 0
l = []
while 2**i <= n:
    l.append(2**i)
    i += 1
print(*l)