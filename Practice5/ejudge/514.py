"""проверяет состоит ли строка только из цифр"""

import re

txt = input()

r = re.compile(r"\d")
q = r.findall(txt)

if len(q) == len(txt):
    print("Match")
else:
    print("No match")