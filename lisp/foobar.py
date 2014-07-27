#!/usr/bin/env python2.7
from __future__ import print_function
from __future__ import division
import sys, pprint

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

def add_globals(env):
    "Add some Scheme standard procedures to an environment."
    import math, operator as op
    env.update(vars(math)) # sin, sqrt, ...
    env.update(
     {'+':op.add, '-':op.sub, '*':op.mul, '/':op.div, 'not':op.not_,
      '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq,
      'equal?':op.eq, 'eq?':op.is_, 'length':len, 'cons':lambda x,y:[x]+y,
      'car':lambda x:x[0],'cdr':lambda x:x[1:], 'append':op.add,
      'list':lambda *x:list(x), 'list?': lambda x:isa(x,list),
      'null?':lambda x:x==[], 'symbol?':lambda x: isa(x, Symbol)})
    return env

global_env = add_globals(Env())

isa = isinstance

#######################
subs = dict()

def Global(l):
    label = 'LABEL%02d' %len(subs)
    subs[label] = l
    return label
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

def Compile(x, env=global_env):
    "Evaluate an expression in an environment."
    if isa(x, Symbol):             # variable reference
        Print("  LD %s %s" % frame_lookup(x, env))
    elif not isa(x, list):         # constant literal
        Print("  LDC %d" %x)
    elif x[0] == 'quote':          # (quote exp)
        (_, exp) = x
        return exp
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        Compile(test, env)
        l1, l2 = ("label1", "label2")
        Print("  SEL %s %s" %(l1, l2))
        Print("label1:")
        Compile(conseq, env)
        Print("  JOIN")
        Print("label2:")
        Compile(alt, env)
        Print("  JOIN")
    elif x[0] == 'set!':           # (set! var exp)
        (_, var, exp) = x
        Compile(exp, f)
        # TODO
        n, i = (0, 0)
        Print("  ST %s %s" %(n, i))
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        #env[var] = Compile(exp, env) # TODO Not written in Perl
    elif x[0] == 'lambda':         # (lambda (var*) exp)
        (_, vars, exp) = x
        return lambda *args: eval(exp, Env(vars, args, env))
    elif x[0] == 'begin':          # (begin exp*)
        for exp in x[1:]:
            val = Compile(exp, env)
        return val
    elif x[0] in prim:
        f = prim[x[0]]
        for i in range(1, len(x)):
            Compile(x[i], f)
        Print("  %s" %f)
    else:                          # (proc exp*)
        exps = [Compile(exp, env) for exp in x]
        Print("  %s" %env)
        #proc = exps.pop(0) # TODO Compile prints, does not return!
        #return proc(*exps)

def main(prog, f=""):
    if f:
        code = open(f).read()
        prog = parse(code)
    else:
        prog = ['add', ['add', 1, 2], 3]
    pprint.pprint(prog)
    Compile(prog)

main(*sys.argv)
