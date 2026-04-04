"""есть ли x в txt"""

import re

txt = input()
x = input()
r = re.findall(x, txt)

if r:
    print("Yes")
else:
    print("No")