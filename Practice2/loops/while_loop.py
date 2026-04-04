#Example 1
count = 1
while count <= 5:
    print(f"Count: {count}")
    count += 1


#Example 2
total = 0
num = 1
while num <= 10:
    total += num
    num += 1
print(f"Sum 1-10: {total}")


#Example 3
timer = 5
while timer > 0:
    print(f"T-minus {timer}")
    timer -= 1
print("Liftoff!")


#Example 4
# (commented for safety, uncomment to use)
# password = ""
# while password != "secret":
#     password = input("Enter password: ")
# print("Access granted!")


#Example 5
n = 5
i = 1
while i <= 10:
    print(f"{n} × {i} = {n * i}")
    i += 1