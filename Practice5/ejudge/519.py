"""показывает сколько слов в строке"""

import re

txt = input()

r = re.findall("\w+", txt)

print(len(r))