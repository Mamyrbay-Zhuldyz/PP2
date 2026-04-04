"""выводит имия и возраст:
input: Name: Alice, Age: 25
output: Alice 25"""

import re

txt = input()

r = re.findall("Name: |, Age:", txt)
q = txt

for i in range(2):
    q = q.replace(r[i], "")

print(q)