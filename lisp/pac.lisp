(main (world ghosts)
    (begin
        (define init (lambda (down step) (cons 42 step)))
        (init 2
            (lambda (s)
                (cons
                    (+ s 1) ; new lm state
                    (- (/ s 8) (* (/ s 32) 4)) ; direction
                )
            )
        )
    )
)
