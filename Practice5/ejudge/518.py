"""выводит сколько раз встречается х"""

import re

txt = input()
x = input()

r = re.escape(x)
q = re.findall(r, txt)

print(len(q))