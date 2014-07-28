fun('main') {
  run0('fubar')
  hlt()
}
fun('hello') {
  and2($c, $d)
  and2([$c], $d)
}
fun('fubar') {
  and2($c, $d)
  run2('hello', $c, $d)
}
