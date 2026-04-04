#Example 1
print(10 > 9)    #True
print(10 == 9)   #False
print(10 < 9)    #False


#Example 2
print(bool("Hello"))   #True
print(bool(0))         #False
print(bool())          #False (empty)


#Example 3
x = "Hello"
y = 15
print(bool(x))    #True
print(bool(y))    #True


#Example 4
print(bool(""))    #False
print(bool([]))    #False
print(bool({}))    #False
print(bool(None))  #False


#Example 5
def f(a):
    return a >= 18
print(f(20))       #True
print(f(16))       #False