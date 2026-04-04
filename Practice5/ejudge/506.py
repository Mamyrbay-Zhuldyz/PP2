"""выводит почту"""

import re

txt = input()
x = re.search("\S+@+[a-z]+[.]\S*", txt)

if x:
    print(x.group())
else:
    print("No email")