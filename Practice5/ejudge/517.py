"""выводит сколько раз встречается дата"""

import re

txt = input()

r = re.findall("\d.{1}.\d.{1}.\d.{3}", txt)

print(len(r))