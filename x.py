import re

s = re.compile("\\#([a-z]*)([0-9]*)")

print(s.match("#abc123 111").group(2))