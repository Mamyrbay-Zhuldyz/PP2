n = int(input())
l = list(map(int, input().split()))
r = list(map(lambda x: x!=0, l))
print(sum(r))