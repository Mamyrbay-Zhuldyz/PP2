"""показывает сколько заглавных букв"""

import re

txt = input()

r = re.findall("[A-Z]", txt)

print(len(r))