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
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if var in self else self.outer.find(var)

global_env = Env()

isa = isinstance

#######################

def Debug(s):
    sys.stderr.write(s + '\n')
boilerplate = """\
  DUM  2        ; 2 top-level declarations
  LDC  2        ; declare constant down
  LDF  10 ; >>---- step ---->>      ; declare function step
  LDF  6 ; >>---- init ---->>      ; init function
  RAP  2        ; load declarations into environment and run init
  RTN           ; final return
  LDC  42 ; <<==== init ====<<
  LD   0 1      ; var step
  CONS
  RTN           ; return (42, step)
"""
def SafeLines(lines):
    return [line for line in lines
            if StripComments(line)]
class Blocks(object):
    def Add(self, sub):
        label = 'LABEL%02d' %len(self.subs)
        self.subs[label] = SafeLines(sub)
        return "${%s}" %label
    def AddMain(self, main=None):
        if main is None:
            main = [line for line in
                    StripComments(boilerplate).split('\n')]
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
        #return ["LD %d %d" % (0, env.find(x)[x])]
        return ["LD %d %d" % (0, 0)]
    elif not isa(x, list):         # constant literal
        return ["LDC %d" % x]
    elif x[0] == 'quote':          # (quote exp)
        raise RuntimeError("quote unimplmented")
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        code = Compile(test)
        l1 = b.Add(Compile(conseq) + ["JOIN"])
        l2 = b.Add(Compile(alt) + ["JOIN"])
        code.append("SEL %s %s" % (l1, l2))
        return code
    elif x[0] == 'set!':           # (set! var exp)
        (_, var, exp) = x
        code = Compile(exp)
        v = env.find(var)[var]
        code.append("ST %d %d" % (0, v))
        return code
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        code = Compile(exp)
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
        code.append("LDC %d %d" % (0, env.find(proc)[proc]))
        code.append("AP %d" % (len(x)-1))
        return code

def main(prog, f=""):
    if f:
        code = open(f).read()
        prog = parse(code)
    else:
        prog = ['add', ['add', 1, 2], 3]
    Debug(pprint.pformat(prog))
    global_blocks.AddMain() # default boilerplate
    code = Compile(prog)
    code.append("RTN")
    global_blocks.Add(code)
    global_blocks.Print()

if __name__=="__main__":
    main(*sys.argv)
