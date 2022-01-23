# haxiLex - Simple Lexer framework

# Why?
* Easy to use
* No complexity
* Create lexer which accepts `s` and returns `obj, 123` (Object and computed length)

# HowTo
* To lex something, call `lex(string, lexer1, lexer2, ...)`
	* It will return token-list: `(0, token), (10, token), ...`
	* Can throw `Exception("Unknown token at sym-pos ...")` if it will found _unknown token_
* Lexer
	* Accepts string `s` as argument
	* Returns `object` and `len` of consumed content
		* For example if we have `abc` then we return `abc` and len `3`: `return 'abc', 3`
		* Why? Because `len` helps to find out latest lexed position. Also `len` can be different, so you need to return it explicitly
	* Better to use `sb = []` arrays as string builder: `"".join(sb)`

# Usage
```py
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
for tok in lex("abc ab aa 123012 #ThisIsTag #ThisIsTag2 #Tag3 ccc 11 aa", abcLexer, numLexer, tagLexer):
	print(tok)

# Will print:
#
# (0, 'abc')
# (4, 'ab')
# (7, 'aa')
# (10, '123012')
# (17, Tag[ThisIsTag])
# (28, Tag[ThisIsTag2])
# (40, Tag[Tag3])
# (46, 'ccc')
# (50, '11')
# (53, 'aa')
```

# Lex

* `lex(`