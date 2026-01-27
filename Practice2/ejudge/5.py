n = int(input())
i = 0
a = "NO"
while i <= n:
    if 2**i == n:
        a = "YES"
        break
    i += 1
print(a)