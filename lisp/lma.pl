#!/usr/bin/perl
use strict;
use warnings;

sub parse {
    my @statements;
    my %labels;
    my $pc = 0;
    my $label;
    while (<>) {
        chomp;
        if (/([a-z]\w+):/i) {
            $labels{$label = $1} = $pc;
        } elsif (/^\s+\w/) {
            if ($label) {
                $_ .= " ; <<==== $label ====<<";
                $label = undef;
            }
            push @statements, $_;
            ++$pc;
        }
    }
    return [\@statements, \%labels];
}

sub main {
    my $program = parse();
    for my $statement (@{$program->[0]}) {
        $statement =~ s{(LDF\s+)([a-z]\w+)}{
            $1 . $program->[1]{$2} . " ; >>---- $2 ---->> "
            // die "ERROR: Undefined label to LDF: $1\n"}ie;
        $statement =~ s{((?:LDF|SEL)\s+)([a-z]\w+)\s+([a-z]\w+)}{
            $1 . $program->[1]{$2} . " " . $program->[1]{$3} . 
            " ; >>---- $2 ---->> "
            // die "ERROR: Undefined label to LDF: $1\n"}ie;
        print $statement, "\n";
    }
}

main();
