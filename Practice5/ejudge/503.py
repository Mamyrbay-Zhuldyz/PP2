"""сколько раз х встричается в txt"""

import re

txt = input()
x = input()
r = re.findall(x, txt)

print(len(r))