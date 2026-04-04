"""input: 123
output: 112233"""

import re

q = re.compile(r"\d")

def f(i):
    return i.group() * 2

txt = input().rstrip("\n")
r = q.sub(f, txt)

print(r)