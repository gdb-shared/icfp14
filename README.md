ICFP 2014
=========

Lambda Man Quick Ref
--------------------

    LDC n   - push constant int a
    LD n i  - push i'th element of frame n
    ADD     - pop x, y. push addend: x+y
    SUB     - pop x, y. push difference: x-y
    MUL     - pop x, y. push multiplicand: x*y
    DIV     - pop x, y. push dividend: x/y
    CEQ     - pop x, y. if x==y then push 1 else push 0
    CGT     - pop x, y. if x>y then push 1 else push 0
    CGTE    - pop x, y. if x>=y then push 1 else push 0
    ATOM    - pop value. if x is int then push 1 else push 0
    CONS    - pop x, y. push pointer to new CONS cell (x, y)
    CAR     - pop pointer to CONS cell. push first element
    CDR     - pop pointer to CONS cell. push second element
    SEL t f - pop i. dpush c+1. if i==0 then c=f else c=t
    TSEL t f -pop i. if i==0 then c=f else c=t
    JOIN    - dpop i. c=i
    LDF f   - push CLOSURE(f, e)
    AP n    - pop x. (f,e)=x. fp=newFrame(pop n values, e). dpush e. dpush c+1. e=fp. c=f
    TAP n   - pop x. (f,e)=x. fp=newFrame(pop n values, e). e=fp. c=f
    RTN     - dpop x, y. e=y. c=x.
    DUM n   - e=newFrame(n)
    RAP n   - pop x. (f,fp)=x. addFrame(pop n values). dpush parent(e). dpush c+1. e=fp. c=f
    TRAP n  - pop x. (f,fp)=x. addFrame(pop n values). e=fp. c=f
    STOP    - stop
    ST n i  - pop x. set i'th element of frame n to x
    DBUG    - pop x. show x in debug window
    BRK     - breakpoint

GCC
---

    MOV dest,src  - dest = src
    INC dest      - ++dest
    DEC dest      - --dest
    ADD dest,src  - dest += src
    SUB dest,src  - dest -= src
    MUL dest,src  - dest *= src
    DIV dest,src  - dest /= src
    AND dest,src  - dest &= src
    OR dest,src   - dest |= src
    XOR dest,src  - dest ^= src
    JLT targ,x,y  - if (x < y) goto targ
    JEQ targ,x,y  - if (x == y) goto targ
    JGT targ,x,y  - if (x > y) goto targ
    INT i         - interrupt i
    HLT           - halt

fickle
------

    mov a,255
    mov b,0
    mov c,4

    dec c
    jgt 7,[c],a

    mov a,[c]
    mov b,c
    jgt 3,c,0

    mov a,b
    int 0

    int 3
    int 6
    inc [b]
    hlt

Ghost Language
--------------

    (define f (lambda (x) (* x x)))
    (defn f (x) (* x x))

    if x:
        y = 2
    else:
        y = 1

    (define y (if (x) 2 1))

    if("x",
        set("y",1),
        set("y",2))
    fun(["x","y"],add("x","y"))
