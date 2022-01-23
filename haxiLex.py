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
			pos += 1
			continue
		res, cnt = __lexArr(s[pos:], lexers)
		if cnt < 1:
			break
		yield (pos, res)
		pos += cnt

def __lexArr(string, lexers):
	for lex in lexers:
		res, cnt = lex(string)
		if cnt < 1:
			continue
		return res, cnt
	return None, 0
