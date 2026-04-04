n = input()
v = ["a", "e", "i", "u", "o", "A", "O", "E", "U", "I"]

q = any(x in v for x in n)

if q:
    print("Yes")
else:
    print("No")