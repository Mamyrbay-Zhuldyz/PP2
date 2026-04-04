"""выводит цифры из txt"""

import re

txt = input()
x = re.findall("\d", txt)

print(*x)