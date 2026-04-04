"""показывает сколко слов в предложений"""

import re

txt = input()

r = re.findall("\w+", txt)

print(len(r))