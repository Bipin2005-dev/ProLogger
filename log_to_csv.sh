#!/usr/bin/env bash

fileName=$1
outputFileName=$2
echo -e "LineId,Time,Level,Content,EventId,EventTemplate\r" > $outputFileName
cat -n $fileName | sed 's/\r//g' | sed -E 's/ *([0-9]+).*\[([A-Za-z0-9: ]*)\] \[([a-z]*)\] (.*)/\1,\2,\3,\4/' | sed -E -f event_append.sed >> $outputFileName