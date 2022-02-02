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
    * Lexer could be a `string` or an `Regex` object.
        * Let's say we have `export` keyword. It could be a nice token
        * Or we have some tag `#TagName` so we want to parse it with `Regex(s, supplyGroup(n, name))`, like so: `Regex("\\#([a-zA-Z0-9\\_]*)", supplyGroup(1, "TAG"))`
* Also you can do recursive lexing. Just use `lexOne(src, lexers)`, where `src` is a string and `lexers` is a list of lexers
	* It will return `obj, len` if lexer found token, otherwise `None, 0`

# Usage
* Please refer to `test.py`

# Create lexers
## From function
```py
def mylexer(s):
	builder=[]
	for i in s:
		if i == " ":
			break
		builder.append(i)
	return "".join(builder), len(builder)
```
## From Regex
```py
mylexer = Regex("[a-z]*", supplyGroup(0, "WORD")).asLexer()
```
## From String
```py
mylexer = lexFromStr("[")
```
## From multiple other lexers
```py
# lexAnd - combines multiple lexers into chain lexer
# for example abcLexer is a "abc" lexing function and dotLexer is a only "." lexer
# Here we trying to lex: abc.abc
mylexer = lexAnd(abcLexer, dotLexer, abcLexer)

# Or using lexOr(lexer1, lexer2, lexer3...)
mylexer = lexOr(abcLexer, lexer123)
```