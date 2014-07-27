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
    JOIN    - dpop i. c=i
    LDF f   - push CLOSURE(f. e)
    AP n    - pop f. e=newFrame(pop n values)


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
