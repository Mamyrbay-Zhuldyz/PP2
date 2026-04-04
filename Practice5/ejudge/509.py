"""выводить сколько слов имеет 3 букв"""

import re

txt = input()

r = re.split(" ", txt, len(txt))
s = 0

for i in r:
    if len(i) == 3:
        s += 1

print(s)