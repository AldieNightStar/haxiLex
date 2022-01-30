import re

class Regex:
    def __init__(self, name, t) -> None:
        self.pattern = re.compile(t)
        self.name = name
    def match(self, s):
        return self.pattern.match(s)

def decorPrefixes(*prefixes):
	def deco(f):
		def wrp(s):
			for pref in prefixes:
				if s.startswith(pref):
					return f(s)
			return None, 0
		return wrp
	return deco

def lex(s, *lexers):
	pos = 0
	while True:
		if pos >= len(s):
			break
		if s[pos] in " \t\r\n":
			yield " ", 1
			pos += 1
			continue
		res, cnt = lexOne(s[pos:], lexers)
		if cnt < 1: # Unknown token
			raise Exception(f"Unknown token at sym-pos {pos}: {s[pos:pos+10]}")
		yield res, cnt
		pos += cnt

def lexOne(string, lexers):
	for lex in lexers:
		if type(lex) is str:
			lexStr = lex
			def lx(s):
				if s.startswith(lexStr):
					return lexStr, len(lexStr)
				return None, 0
			lex=lx
		elif type(lex) is Regex:
			regex = lex
			def lx(s):
				m = regex.match(s)
				if m == None:
					return None, 0
				return (regex.name, m), len(m.group(0))
			lex = lx
		res, cnt = lex(string)
		if cnt < 1:
			continue
		return res, cnt
	return None, 0
