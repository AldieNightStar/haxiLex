import re

class Regex:
    def __init__(self, pattern, supplierFn=None) -> None:
        self.pattern = re.compile(pattern)
        self.supplier = supplierFn
    def match(self, s):
        m = self.pattern.match(s)
        if m == None:
            return None, None
        if self.supplier != None:
            return self.supplier(m), m
        return None, m
    def asLexer(self):
        def lx(s):
            supplied, m = self.match(s)
            if m == None:
                return None, 0
            LEN = len(m.group(0))
            if supplied == None:
                return m, LEN
            return supplied, LEN
        return lx

def lexFromStr(string, name="undef"):
    def lx(s):
        if s.startswith(string):
            return (name, string), len(string)
        return None, 0
    return lx

def lexAnd(*lexers):
    def lx(s):
        arr = []
        pos = 0
        for l in lexers:
            res, cnt = l(s[pos:])
            if cnt < 1:
                return None, 0
            pos += cnt
            arr.append(res)
        return arr, pos
    return lx

def lexOr(*lexers):
    def lx(s):
        for l in lexers:
            res, cnt = l(s)
            if cnt < 1:
                continue
            return res, cnt
    return lx

def supplyGroup(n, name="undef"):
    def supp(m):
        try:
            return (name, m.group(n))
        except:
            return None
    return supp

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
            lex=lexFromStr(lex)
        elif type(lex) is Regex:
            lex = lex.asLexer()
        res, cnt = lex(string)
        if cnt < 1:
            continue
        return res, cnt
    return None, 0
