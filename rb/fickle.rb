=begin
mov a,255
mov b,0
mov c,255

inc c
jgt 7,[c],a

mov a,[c]
mov b,c
jlt 3,c,3

mov a,b
int 0

int 3
int 6
inc [b]
hlt


; lyren
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
=end

fun('main') {
  mov $a,255
  mov $b,0
  mov $c,255

  label :FICKLE_INC
  inc $c
  jgt :FICKLE_LOOP,[$c],$a

  mov $a,[$c]
  mov $b,$c
  label :FICKLE_LOOP
  jlt :FICKLE_INC,$c,3

  mov $a,$b
  int 0

  int 3
  int 6
  inc [$b]
  hlt
}
