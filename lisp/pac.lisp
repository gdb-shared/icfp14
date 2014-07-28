(cons
 (+ s 1) ; new lm state
 (if (- (/ s 8) (* (/ s 32) 4)) 0 1) ; direction
)
