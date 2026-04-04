"""заменяет х на у"""

import re

txt = input()
x = input()
y = input()

r = re.sub(x, y, txt)

print(r)