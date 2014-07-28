(begin
 (define x 1)
 (define f (lambda (y) (+ x y)))
 (define v1 (f 3))
 (set! x 2)
 (define v2 (f 3))
 (cons v1 (cons v2 0))
)
