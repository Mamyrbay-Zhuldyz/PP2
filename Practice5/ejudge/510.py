"""проверяет есть ли собака или кот"""

import re

txt = input()

r = re.findall("cat|dog", txt)

if r:
    print("Yes")
else:
    print("No")