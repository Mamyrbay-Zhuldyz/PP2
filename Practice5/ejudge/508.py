"""все символы удаляет и вывыодит через запятую"""

import re

s = input().rstrip("\n")
d = input().rstrip("\n")

q = re.split(d, s)

print(",".join(q))