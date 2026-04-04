n = int(input())
l = list(map(int, input().split()))

l_new = set(l)

print(*sorted(l_new))