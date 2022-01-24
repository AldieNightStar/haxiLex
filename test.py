from haxiLex import *

# Simple lexer
def abcLexer(s):
	sb = []
	for c in s:
		if c in "abc":
			sb.append(c)
		else:
			break
	return "".join(sb), len(sb)

def numLexer(s):
	sb = []
	for c in s:
		if c in "01234567890":
			sb.append(c)
		else:
			break
	return "".join(sb), len(sb)

# Let's create some real token
class Tag:
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return f"Tag[{self.name}]"

# This decor says that we parse only values which starts with: "#" or "@"
# Better to make all prefixes same size. No need to verify then
@decorPrefixes("#", "@")
def tagLexer(s):
	# This Lexer will return Tag(name) class.
	sb = []
	for c in s[1:]:
		if c in " \t\r\n":
			break
		sb.append(c)
	return Tag("".join(sb)), len(sb) + 1 # Why + 1? Because we started from s[1:] pos, and skipped first symbol.


# Now collect tokens
for tok, cnt in lex("abc ab aa 123012 #ThisIsTag #ThisIsTag2 #Tag3 ccc 11 aa", abcLexer, numLexer, tagLexer):
	# Let's skip the spaces
	# All spaces converted to " "
	if tok == " ": continue
	# Now let's print actual tokens
	print(tok, cnt)

# Will print:
#
# abc 3
# ab 2
# aa 2
# 123012 6
# Tag[ThisIsTag] 10
# Tag[ThisIsTag2] 11
# Tag[Tag3] 5
# ccc 3
# 11 2
# aa 2

# Now let's lex only one token
# It will return token and it's len
# If token not found, then tok == None and cnt == 0
tok, cnt = lexOne("abcccbbba 123", [abcLexer, numLexer])
if cnt > 0:
	print("The token is: " + tok)

# Will print:
#
# The token is: abcccbbba