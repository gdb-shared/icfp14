fun('main') {
  @mode_counter = 244
  @mode = 245
  @global_counter = 246
  @prev_dir = 247
  @vitality = 248
  @counter = 249
  @rand = 250
  @new_dir = 251
  @pac_x = 252
  @pac_y = 253
  @ghost_x = 254
  @ghost_y = 255
  inc [@global_counter]
  int 3
  int 6 # a,b <= vit,dir
  mov [@vitality], $a
  mov [@prev_dir], $b
  int 3 # a <= ghost
  int 5 # a,b <= x,y ghost
  mov [@ghost_x], $a
  mov [@ghost_y], $b
  int 1 # a,b <= x,y pac
  mov [@pac_x], $a
  mov [@pac_y], $b

  # Choose preferred axis.
  int 3
  and2 $a, 1
  jeq :hunt_horz,$a,0
}
fun('hunt_vert') {
  jlt :RIGHT,[@ghost_x],[@pac_x]
  jlt :GO_DOWN,[@ghost_y],[@pac_y]
  jgt :GO_UP,[@ghost_y],[@pac_y]

  label :GO_LEFT
  mov [@new_dir], $left
  goto :FINISH

  label :GO_DOWN
  mov [@new_dir], $down
  goto :FINISH

  label :GO_UP
  mov [@new_dir], $up
  goto :FINISH

  label :RIGHT
  jlt :GO_DOWN,[@ghost_y],[@pac_y]
  jgt :GO_UP,[@ghost_y],[@pac_y]

  label :GO_RIGHT
  mov [@new_dir], $right
  goto :FINISH
}
fun('hunt_horz') {
  jlt :HDOWN,[@ghost_x],[@pac_x]
  jlt :HGO_RIGHT,[@ghost_y],[@pac_y]
  jgt :HGO_LEFT,[@ghost_y],[@pac_y]

  label :HGO_UP
  mov [@new_dir], $left
  goto :FINISH

  label :HGO_RIGHT
  mov [@new_dir], $down
  goto :FINISH

  label :HGO_LEFT
  mov [@new_dir], $up
  goto :FINISH

  label :HDOWN
  jlt :HGO_RIGHT,[@ghost_y],[@pac_y]
  jgt :HGO_LEFT,[@ghost_y],[@pac_y]

  label :HGO_UP
  mov [@new_dir], $right
  #goto :FINISH
}
fun("FINISH") {
  jeq :REVERSE,[@vitality],1

  #label :RANDOMIZE
  # Compute a random number.
  add [@rand],[@global_counter] # important to move 1s bit
  add [@rand],[@pac_x]
  add [@rand],[@pac_x]
  mov $a,0
  int 5
  add [@rand],$a
  add [@rand],$b
  mov $a,1
  int 5
  add [@rand],$a
  add [@rand],$b
  mov $a,2
  int 5
  add [@rand],$a
  add [@rand],$b
  #add [@rand],[@prev_dir]  # useful?

  # If mode_counter is 0, update mode based
  # on random number. Then flip.
  mov $g,[@mode_counter]
  mov $h,[@mode]
  int 8
  jgt :DEC_MODE_COUNTER,[@mode_counter],0

  # $d := (rand % 3) + ghost_index + 1
  mov $c,[@rand]
  div $c,3
  mul $c,3
  mov $d,[@rand]
  sub $d,$c
  int 3
  add $d,$a
  add $d,1 # divisor cannot be 0!
  #int 8

  # Create more entropy.
  mov $a,3
  int 5
  add [@rand],$a
  add [@rand],$b

  # Now, $e := rand % $d
  mov $c,[@rand]
  div $c,$d
  mul $c,$d
  mov $e,[@rand]
  sub $e,$c
   #mov $f,[@rand]
  #int 8
  mov [@mode_counter],$e

  # flip mode
  xor [@mode],1

  inc [@mode_counter]
  label :DEC_MODE_COUNTER
  dec [@mode_counter]

  # mode 0 => non-random
  jeq :SET_DIR,[@mode],0

  label :RANDOM_MOVE
  mov [@new_dir],[@rand]
  and2 [@new_dir],3
  goto :SET_DIR

  label :REVERSE
  add [@new_dir],2

  label :SET_DIR
  mov $a,[@new_dir]
  int 0  # from $a
  mov $c, [@rand]
  hlt
}
