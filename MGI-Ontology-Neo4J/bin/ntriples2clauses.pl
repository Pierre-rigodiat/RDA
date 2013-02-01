#!/usr/bin/perl

use warnings;
use strict;
use URI::Escape;
use Digest::SHA1 qw(sha1_hex);

my $DEBUG = 0;

my %node; 
my @fld; 
my ($v1, $e, $v2);

my $codeHeader =<<CodeHeader;
:- dynamic vertex/2.
:- dynamic edge/4.
CodeHeader

my $codeAddVertex =<<CodeAddVertex;
/* 1 */ vertex(name('NNN'), source('SSS')).
CodeAddVertex

my $codeAddEdge =<<CodeAddEdge;
/* 2 */ edge(name('LLL'), name('RRR'), type('EEE'), source('SSS')).
CodeAddEdge

my $codeFooter =<<CodeFooter;
CodeFooter

my %nickname;
my @clause;

sub nickname ($) {
	my $name = shift;
	my ($prefix, $nname);

	if ($name =~ m{http://purl.org}) {
		my @fld = split /\//, $name;
		$nname = $fld[-1];
	} else {
		($prefix, $nname) = split /#/, $name, 2;
	}

	$nname = defined $nname ? $nname : $name;
	$nname = sha1_hex($name) if length($nname) > 40;

	my $n = $nickname{$nname};
	if (!defined $n) {
		$nickname{$nname} = $name;
	} elsif ($n ne $name) {
		$nname .= substr sha1_hex($name), 0, 6;
		$nickname{$nname} = $name;
	}

	return $nname;
}

sub encode_triple ($$$) {
	my $lnode = shift;
	my $edge  = shift;
	my $rnode = shift;

	my $emit = "";
	my ($chunk, $lname, $rname);

	if (!$node{$lnode}) {
		for ($chunk = $codeAddVertex) {
			s/SSS/$lnode/g;
			$lname = nickname $lnode;
			s/NNN/$lname/g;
		}
		$node{$lnode} = 1;
		$emit .= $chunk;
	} else {
		$lname = nickname $lnode;
	}

	if (!$node{$rnode}) {
		for ($chunk = $codeAddVertex) {
			s/SSS/$rnode/g;
			$rname = nickname $rnode;
			s/NNN/$rname/g;
		}
		$node{$rnode} = 1;
		$emit .= $chunk;
	} else {
		$rname = nickname $rnode;
	}

	for ($chunk = $codeAddEdge) {
		s/LLL/$lname/g;
		s/RRR/$rname/g;
		s/SSS/$edge/g;
		$edge = nickname $edge; # for now...
		s/EEE/$edge/g;
		$emit .= $chunk;
	}

	# $emit = $DEBUG ? $emit : uri_escape($emit);
	push @clause, $emit;
}

sub cleanup (\$) {
	my $item = shift;
	for ($$item) {
		s/^"//;
		s/\\"/_/g; 
		s/".*$//;
		s/^^//g;
		s/(\\n)+/ /g;
		s/\'/_/g;
		s/\`/_/g;
		s/_ _/__/g;
		s/\(|\)//g;
	}
}

print $codeHeader;	
while(<>) {
	next if /^\s*$/;
	chomp; chop; chomp;

	s/\s|<|>/ /g;	# make delimiters
	s/ +/ /g;	# dedup
	chop;
	s/^\s+//;	# ltrim
	($v1, $e, $v2) = @fld = split /\s/, $_, 3;
	die if @fld != 3;

	cleanup $v1;
	cleanup $e;
	cleanup $v2;

	encode_triple $v1, $e, $v2;
}

my @sorted_clause = sort(split /\n/, join('', @clause));
print join("\n", @sorted_clause);
print $codeFooter;

