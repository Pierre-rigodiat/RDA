#!/bin/bash

DOC_ROOT=/home/pierre
FILE_LOC=$DOC_ROOT/Documents/ontology/ontology-bash/Filter.n3
FILE_DEST=/var/tmp/
ONTO=$DOC_ROOT/Documents/ontology/ontology-bash/Materials.n3
CWM=/usr/lib/pymodules/python2.7/swap/cwm.py
RESULT=$DOC_ROOT/Documents/ontology/

if [ $# -eq 2 ]
then
	FILE_DEST=$FILE_DEST$2".n3"	
	RESULT=$RESULT$2".json"
	cp $FILE_LOC $FILE_DEST
	perl -pi -e "s/%%/$1/g" $FILE_DEST
	python $CWM $ONTO --think --filter=$FILE_DEST --strings > $RESULT
else
	echo "Usage: $0 query integer"
	exit 1
fi
