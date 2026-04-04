"""проверяет начинаеться ли строка с буквы и заканчиваеться цифрой"""

import re

txt = input()
x = re.findall("^[A-Za-z]*\d$", txt)

if x:
    print("Yes")
else:
    print("No")