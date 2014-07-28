$debug = nil

def ind(x)
  puts "ind #{x}"
  return "[#{x}]"
end

$a = 'a'
$b = 'b'
$c = 'c'
$d = 'd'
$e = 'e'
$f = 'f'
$g = 'g'
$h = 'h'
$up = 0
$right = 1
$down = 2
$left = 3

class Compiler
  attr_reader :funcs
  def initialize()
    @lineno = 0
    @lines = []  # index does *not* correspond to lineno
    @labels = Hash.new
  end
  def addr(x)
    if x.is_a?(Array)
      "[#{addr(x[0])}]"
    elsif x.is_a?(Symbol)
      "%{#{x}}"
    else
      x
    end
  end
  def emit(x)
    @lines.push(x.ljust(20) + "\t ;line #{@lineno}")
    @lineno += 1
    @lineno - 1
  end
  def hlt()
    emit("#{__method__.upcase}")
  end
  def int(i)
    i, = [i].map {|x| addr(x)}
    emit("#{__method__.upcase} #{i}")
  end
  def mov(dst,src)
    dst, src = [dst,src].map {|x| addr(x)}
    emit("#{__method__.upcase} #{dst},#{src}")
  end
  def add(dst,src)
    dst, src = [dst,src].map {|x| addr(x)}
    emit("#{__method__.upcase} #{dst},#{src}")
  end
  def sub(dst,src)
    dst, src = [dst,src].map {|x| addr(x)}
    emit("#{__method__.upcase} #{dst},#{src}")
  end
  def mul(dst,src)
    dst, src = [dst,src].map {|x| addr(x)}
    emit("#{__method__.upcase} #{dst},#{src}")
  end
  def div(dst,src)
    dst, src = [dst,src].map {|x| addr(x)}
    emit("#{__method__.upcase} #{dst},#{src}")
  end
  def xor(dst,src)
    dst, src = [dst,src].map {|x| addr(x)}
    emit("#{__method__.upcase} #{dst},#{src}")
  end
  def inc(dst)
    dst, = [dst].map {|x| addr(x)}
    emit("#{__method__.upcase} #{dst}")
  end
  def dec(dst)
    dst, = [dst].map {|x| addr(x)}
    emit("#{__method__.upcase} #{dst}")
  end
  def and2(x, y)
    x, y = [x,y].map {|_| addr(_)}
    emit("AND #{x},#{y}")
  end
  def or2(x, y)
    x, y = [x,y].map {|_| addr(_)}
    emit("AND #{x},#{y}")
  end
  def jeq(targ, x, y)
    targ, x, y = [targ,x,y].map {|_| addr(_)}
    emit("#{__method__.upcase} #{targ},#{x},#{y}")
  end
  def jgt(targ, x, y)
    targ, x, y = [targ,x,y].map {|_| addr(_)}
    emit("#{__method__.upcase} #{targ},#{x},#{y}")
  end
  def jlt(targ, x, y)
    targ, x, y = [targ,x,y].map {|_| addr(_)}
    emit("#{__method__.upcase} #{targ},#{x},#{y}")
  end
  def trace()
    emit("int 8")
  end
  def goto(label)
    emit("jeq %{#{label}},0,0 ; goto '#{label}'")
  end
  def run0(func)
    emit("jeq %{#{func}},0,0 ; '#{func}'")
  end
  def run2(func, x, y)
    emit("jeq %{#{func}},0,0 ; '#{func}'")
  end
  def label(name)
    @lines.push("; '#{name}'")
    @labels[name.to_sym] = @lineno
  end
  #def var(name, addr)
    # Or just assign.
    #instance_variable_set(name, addr)
  #end
  def fun(name, &blk)
    # TODO: Push to stack.
    @lines.push("; func '#{name}'")
    @labels[name.to_sym] = @lineno
    self.instance_eval(&blk)
    # TODO: Pop from stack.
  end
  def finalize()
    $stderr.puts @labels if $debug
    for line in @lines
      if line.include?('%{')
        puts line % @labels
      else
        puts line
      end
    end
  end
  def get_binding
    binding
  end
end
comp = Compiler.new

program = <<eos
fun('main') {
  run0('fubar')
  hlt()
}
fun('fubar') {
  and2(:c, :d)
  #run2('hello', :c, :d)
}
eos
program = $stdin.read
eval(program, comp.get_binding)
comp.finalize
