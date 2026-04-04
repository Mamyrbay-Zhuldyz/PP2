"""выводить цифры"""

import re

txt = input()

r = re.findall("\d+\d", txt)

print(*r)