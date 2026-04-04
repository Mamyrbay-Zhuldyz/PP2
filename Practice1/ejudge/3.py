x = input()
try:
    num = int(x)
    if num >= 0:
        print("int")
    else:
        print("str")
except:
    print("str")