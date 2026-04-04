# 1. Correct indents
print("Correct indents")
if 5 > 2:
    print("Five is greater than two!") # <- 4 spaces or Tab
    print("This is also inside if")    # <- equal indentation


# 2. Incorrect indentation (error!)
print("\nExample 2: Indentation error (commented out)")
# if 5 > 2:
# print("This will cause an error")  # SyntaxError!


#Example 3
if 5 > 2:
 print("Five is greater than two!") 
if 5 > 2:
        print("Five is greater than two!") 


#Example 4
if 5 > 2:
 print("Five is greater than two!")
        print("Five is greater than two!") #Syntax Error


#Example 5
print("Hello"); print("How are you?"); print("Bye bye!")