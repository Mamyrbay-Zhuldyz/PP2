n = int(input())
#l = list(map(int, input().split()))
l = []
sum = 0
for i in range(n):
    x = int(input())
    l.append(x)
for i in l:
    sum = sum + i
print(sum)