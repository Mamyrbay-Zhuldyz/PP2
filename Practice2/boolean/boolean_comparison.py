#Example 1
a = 5
b = 10
print("a == b:", a == b)    # False
print("a != b:", a != b)    # True
print("a > b:", a > b)      # False
print("a < b:", a < b)      # True
print("a >= b:", a >= b)    # False
print("a <= b:", a <= b)    # True


#Example 2
print("'apple' == 'apple':", "apple" == "apple")      # True
print("'apple' == 'Apple':", "apple" == "Apple")      # False
print("'apple' != 'orange':", "apple" != "orange")    # True


#Example 3
list1 = [1, 2, 3]
list2 = [1, 2, 3]
list3 = [1, 2, 4]
print("list1 == list2:", list1 == list2)    # True
print("list1 == list3:", list1 == list3)    # False


#Example 4
x = 5
print("3 < x < 7:", 3 < x < 7)                # True
print("x == 5 or x == 6:", x == 5 or x == 6)  # True


#Example 5
list_a = [1, 2, 3]
list_b = [1, 2, 3]
list_c = list_a
print("list_a is list_b:", list_a is list_b)    # False
print("list_a is list_c:", list_a is list_c)    # True