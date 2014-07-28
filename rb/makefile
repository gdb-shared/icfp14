R=ruby1.9 -w

default:
	$R grub.rb < test.rb
%: %.rb
	$R grub.rb < $@.rb
%.pb: %.rb
	$R grub.rb < $*.rb | pbcopy
