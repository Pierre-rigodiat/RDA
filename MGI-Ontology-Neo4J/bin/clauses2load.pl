#!/usr/bin/perl

use warnings;
use strict;
use URI::Escape;
use Digest::SHA1 qw(sha1_hex);

my $DEBUG = 0;


my $codeHeader =<<CodeHeader;
curl -X POST \\
http://localhost:7474/db/data/ext/GremlinPlugin/graphdb/execute_script \\
-H "content-type:application/x-www-form-urlencoded" \\
-d "script=
CodeHeader

my $codeAddVertex =<<CodeAddVertex;
g.addVertex([name:NNN, source:SSS])
CodeAddVertex

my $codeAddEdge =<<CodeAddEdge;
v1 = g.V.filter{it.name==LLL}.next()
v2 = g.V.filter{it.name==RRR}.next()
g.addEdge(v1, v2, EEE, [source:SSS])
CodeAddEdge

my $codeFooter =<<CodeFooter;
"
CodeFooter

sub emit($) {
	my $line  = shift;
	my $emit = "";
	my $chunk;

	for ($line) {
		if (m/^vertex/) {
			my ($name, $source) = m/vertex\(name\((.*)\),source\((.*)\)\)/;

			for ($chunk = $codeAddVertex) {
				s/SSS/$source/;
				s/NNN/$name/;
				$emit .= $chunk;
			}
		} elsif (m/^edge/) {
			my ($left, $right, $type, $source) = m/^edge\(name\((.*)\),name\((.*)\),type\((.*)\),source\((.*)\)\)/;

			for ($chunk = $codeAddEdge) {
				s/LLL/$left/;
				s/RRR/$right/;
				s/EEE/$type/;
				s/SSS/$source/;
				$emit .= $chunk;
			}

		} else {
			die "Huh?: " . $_;
		}
	}


	chomp $codeHeader;
	$emit = $DEBUG ? $emit : uri_escape($emit);
	printf "%s%s%s\n", $codeHeader, $emit, $codeFooter;
}


while(<>) {
	emit $_;
}

