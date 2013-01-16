#!/bin/bash

DOC_ROOT=`pwd`
FILE_LOC=$DOC_ROOT/ontology-bash/Filter.n3
FILE_DEST=/var/tmp/
ONTO=$DOC_ROOT/ontology-bash/
CWM=/usr/lib/pymodules/python2.7/swap/cwm.py
RESULT=$DOC_ROOT/
ONTO_LOC=`echo $3 | perl -pe 's/([^\.]+)\.[^\.]+/$1/g'`

if [ $# -eq 4 ]
then
	ONTO=$ONTO$3
	FILE_DEST=$FILE_DEST$2".n3"	
	RESULT=$RESULT$2".json"
	cp $FILE_LOC $FILE_DEST
	perl -pi -e "s/%1/$ONTO_LOC/g" $FILE_DEST
	perl -pi -e "s/%2/$1/g" $FILE_DEST
	perl -pi -e "s/%3/$4/g" $FILE_DEST
	python $CWM $ONTO --think --filter=$FILE_DEST --strings > $RESULT
else
	echo "Usage: $0 query integer ontology_file relationship"
	exit 1
fi
