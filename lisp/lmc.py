#!/usr/bin/env python2.7
from __future__ import print_function
from __future__ import division
import sys, pprint, string, re

def Print(s):
    print(s)

Symbol = str

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms,args))
        self.outer = outer
    def find(self, var, n=0):
        "Find the innermost Env where var appears."
        pprint.pprint([var, n, self])
        if var in self:
            return (n, self[var])
        elif self.outer:
            return self.outer.find(var, n+1)
        else:
            raise RuntimeError("Variable not defined: %s" % var)

global_env = Env()

isa = isinstance

#######################

def Debug(s):
    sys.stderr.write(s + '\n')
def SafeLines(lines):
    return [line for line in lines
            if StripComments(line)]
class Blocks(object):
    def Add(self, sub):
        label = 'LABEL%02d' %len(self.subs)
        self.subs[label] = SafeLines(sub)
        return "${%s}" %label
    def AddMain(self, main):
        self.main = SafeLines(main)
    def Print(self, f=sys.stdout, with_linenos=True):
        linenos = dict()
        lines = list()
        lines.extend(self.main)
        for label, sub in self.subs.items():
            linenos[label] = len(lines)
            lines.extend(sub)
        Debug(pprint.pformat(linenos))
        newlines = list()
        for n, line in enumerate(lines):
            if with_linenos:
                line += "\t ; #%02d" %n
            myline = string.Template(line).substitute(linenos)
            newlines.append(myline)
        for line in newlines:
            f.write('  ' + line + '\n')
    def __init__(self):
        self.subs = dict()

global_blocks = Blocks()
def parse(s):
    "Read a Scheme expression from a string."
    return read_from(tokenize(s))

re_comment = re.compile(r'\s*;.*$', re.MULTILINE)
def StripComments(s):
    """
    >>> StripComments('abc ; comment\\n; another\\nfoo')
    'abc\\nfoo'
    """
    return re_comment.sub('', s)
re_paren = re.compile(r'([()])')
def tokenize(s):
    """Convert a string into a list of tokens.
    >>> tokenize('(x) ; comment\\n; another\\nfoo')
    ['(', 'x', ')', 'foo']
    """
    s = StripComments(s)
    s = re_paren.sub(r' \1 ', s)
    return s.split()
def read_from(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)
prim = {
    '+': 'ADD',
    '-': 'SUB',
    '*': 'MUL',
    '/': 'DIV',
    '=': 'CEQ',
    '>': 'CGT',
    '>=': 'CGTE',
    'atom': 'ATOM',
    'cons': 'CONS',
    'car': 'CAR',
    'cdr': 'CDR',
}

def Compile(x, env=global_env, b=global_blocks):
    "Evaluate an expression in an environment."
    if isa(x, Symbol):             # variable reference
        return ["LD %d %d" % env.find(x)]
    elif not isa(x, list):         # constant literal
        return ["LDC %d" % x]
    elif x[0] == 'quote':          # (quote exp)
        raise RuntimeError("quote unimplmented")
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        code = Compile(test, env)
        l1 = b.Add(Compile(conseq, env) + ["JOIN"])
        l2 = b.Add(Compile(alt, env) + ["JOIN"])
        code.append("SEL %s %s" % (l1, l2))
        return code
    elif x[0] == 'set!':           # (set! var exp)
        (_, var, exp) = x
        code = Compile(exp, env)
        code.append("ST %d %d" % env.find(var))
        return code
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        code = Compile(exp, env)
        env[var] = len(env)
        code.append("ST %d %d" % (0, env[var]))
        return code
    elif x[0] == 'lambda':         # (lambda (var*) exp)
        (_, vars, exp) = x
        block = Compile(exp, Env(vars, range(0, len(vars)), env))
        block.append("RTN")
        l = b.Add(block)
        code = []
        code.append("LDF %s" % l)
        return code
    elif x[0] == 'main':         # (lambda (var*) exp)
        (_, vars, exp) = x
        for var in vars:
            env[var] = len(env)
        code = Compile(exp, env)
        code.append("RTN")
        return code
    elif x[0] == 'begin':          # (begin exp*)
        code = []
        for exp in x[1:]:
            code.extend(Compile(exp, env))
        return code
    elif x[0] in prim:
        code = []
        for exp in x[1:]:
            code.extend(Compile(exp, env))
        code.append(prim[x[0]])
        return code
    else:                          # (proc exp*)
        code = []
        for exp in x[1:]:
            code.extend(Compile(exp, env))
        proc = x[0]
        count = len(x)-1
        code.append("LD %d %d" % env.find(proc))
        code.append("AP %d" % count)
        return code

def boilerplate(step, b=global_blocks):
    code = []
    code.append("LDC 42")
    code.append("LD 0 1")
    code.append("CONS")
    code.append("RTN")
    init = b.Add(code)

    code = []
    code.append("DUM 2")
    code.append("LDC 2")
    code.append("LDF %s" % step)
    code.append("LDF %s" % init)
    code.append("RAP 2")
    code.append("RTN")
    b.AddMain(code)

def main(prog, f=""):
    if f:
        code = open(f).read()
        prog = parse(code)
    else:
        prog = ['add', ['add', 1, 2], 3]
    Debug(pprint.pformat(prog))
    code = Compile(prog)
    global_blocks.AddMain(code)
    global_blocks.Print()

if __name__=="__main__":
    main(*sys.argv)
