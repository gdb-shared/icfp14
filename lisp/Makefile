lambdaman.gcc: 
	./lma.pl pac.lma > $@

pac: syn
	./lmc.py pac.lisp

test: syn
	./lmc.py simple7.lisp

pb:
	./lma.pl pac.lma | pbcopy
suite: 
	#./lmc.py simple.lisp
	./lmc.py simple2.lisp
	./lmc.py simple3.lisp
	./lmc.py simple4.lisp
	./lmc.py simple5.lisp
	./lmc.py simple6.lisp
	./lmc.py simple7.lisp
	./lmc.py simple8.lisp
	./lmc.py pac.lisp
t:
	py.test -v --doctest-modules --ignore=keep/
tall: suite t
syn:
	python -c "import lmc"
good:
	@./lmc.py pac.lisp
.PHONY: t suite
