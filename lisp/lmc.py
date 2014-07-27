#!/usr/bin/env python2.7
from __future__ import print_function
from __future__ import division
import sys, pprint, string

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
class Blocks(object):
    def Add(self, sub):
        label = 'LABEL%02d' %len(self.subs)
        self.subs[label] = sub
        return "${%s}" %label
    def AddMain(self, sub):
        self.main = sub
    def Print(self, f=sys.stdout):
        linenos = dict()
        lines = list()
        lines.extend(self.main)
        for label, sub in self.subs.items():
            linenos[label] = len(lines)
            lines.extend(sub)
        Debug(pprint.pformat(linenos))
        lines = [string.Template(line).substitute(linenos) for line in lines]
        for line in lines:
            f.write('  ' + line + '\n')
    def __init__(self):
        self.subs = dict()
global_blocks = Blocks()
def parse(s):
    "Read a Scheme expression from a string."
    return read_from(tokenize(s))
def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()
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

def frame_lookup(name, f):
    n, i = (0, 0);
    return (n, i);

def Compile(x, env=global_env, b=global_blocks):
    "Evaluate an expression in an environment."
    if isa(x, Symbol):             # variable reference
        return ["LD %d %d" % env.find(x)[x]]
    elif not isa(x, list):         # constant literal
        return ["LDC %d" % x]
    elif x[0] == 'quote':          # (quote exp)
        raise RuntimeError("quote unimplmented")
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        code = Compile(test)
        l1 = b.Add(Compile(conseq) + ["RTN"])
        l2 = b.Add(Compile(alt) + ["RTN"])
        code.append("SEL %s %s" % (l1, l2))
        return code
    elif x[0] == 'set!':           # (set! var exp)
        (_, var, exp) = x
        code = Compile(exp)
        code.append("ST %d %d" % env.find(var)[var])
        return code
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        code = Compile(exp)
        code.append("ST %d %d" % frame_add(var, env))
        return code
    elif x[0] == 'lambda':         # (lambda (var*) exp)
        (_, vars, exp) = x
        #return lambda *args: eval(exp, Env(vars, args, env))
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
        code.append("LD %d %d" % frame_lookup(x[0], env))
        code.append("AP %d" % (len(x)-1))
        return code

def main(prog, f=""):
    if f:
        code = open(f).read()
        prog = parse(code)
    else:
        prog = ['add', ['add', 1, 2], 3]
    pprint.pprint(prog)
    global_blocks.AddMain(Compile(prog))
    global_blocks.Print()

if __name__=="__main__":
    main(*sys.argv)
