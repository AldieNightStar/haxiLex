# haxiLex - Simple Lexer framework

# Why?
* Easy to use
* No complexity
* Create lexer which accepts `s` and returns `obj, 123` (Object and computed length)

# HowTo
* To lex something, call `lex(string, lexer1, lexer2, ...)`
	* It will return token-list
	* Can throw `Exception("Unknown token at sym-pos ...")` if it will found _unknown token_
* Lexer
	* Accepts string `s: string` as an argument
	* Returns `object` and `len` of consumed content
		* For example if we have `abc` then we return `abc` and len `3`: `return 'abc', 3`
		* Why? Because `len` helps to find out latest lexed position. Also `len` can be different, so you need to return it explicitly
	* Better to use `sb = []` arrays as string builder: `"".join(sb)`
    * Lexer could be a `string` or an _regex_. Just to match
* Also you can do recursive lexing. Just use `lexOne(src, lexers)`, where `src` is a string and `lexers` is a list of lexers
	* It will return `obj, len` if lexer found token, otherwise `None, 0`

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






# Now let's try next:
# What if lexer could be a string?
# This could help us to indentify couple of keywords without creating lexers
# Let's say that words be: 'export', 'import', 'call'
for tok, cnt in lex("export abbc call 11111", "export", "import", "call", abcLexer, numLexer):
	# Skip all the spaces
	if tok == " ": continue
	print(tok)
# Will output:
#
# export
# abbc
# call
# 11111




# Also we can try to use RegExp as an lexer
# To identify token we need to check token type is `re.Match`
for tok, cnt in lex("#Hello #Hi #HashTag3 123", re.compile("\\#([a-zA-Z0-9\\_]*)"), numLexer):
	# Skip the spaces
	if tok == " ": continue
	# Print out the tokens
	if type(tok) is re.Match:
		# Print out the token info
		#   tok.group(0) - is all matched text
		#   tok.group(1) - is a captured group by () in regexp
		# so we getting tok.group(1) as in regexp we have ()
		print("Token: ", tok.group(1))
		continue
	# Print other tokens
	print(tok)


# This will print:
#
# Token:  Hello
# Token:  Hi
# Token:  HashTag3
# 123
```

# Create lexers
## Create functions
```py
def mylexer(s):
	builder=[]
	for i in s:
		if i == " ":
			break
		builder.append(i)
	return "".join(builder), len(builder)
```