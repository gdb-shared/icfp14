top = """\
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
"""
  LD   0 0      ; var s ; <<==== step ====<<
  LDC  1
  ADD
  LD   0 0      ; var s
  LDC  8
  DIV
  LD   0 0      ; var s
  LDC  32
  DIV
  LDC  4
  MUL
  SUB
  CONS
  RTN           ; return (s+1, down)
"""
