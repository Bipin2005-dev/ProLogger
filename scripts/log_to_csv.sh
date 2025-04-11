#!/usr/bin/env bash

# Checking validity of log file: Can only check the date and time format, as well as if the event type is notice or error for each line, rest of the things can be put outside of E1-E6 if their corresponding Re's don't match.
# grep -E "^\[(Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s{1}(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s{1}(0[1-9]|1[0-9]|2[0-9]|30|31)\s{1}(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\s{1}(19|20)[0-9]{2}\]\s{1}\[(notice|error)\]\s{1}.*" Apache_2k.log | diff Apache_2k.log -


fileName=$1
outputFileName=$2
echo -e "LineId,Time,Level,Content,EventId,EventTemplate\r" > $outputFileName
cat -n $fileName | sed 's/\r//g' | sed -E 's/ *([0-9]+).*\[([A-Za-z0-9: ]*)\] \[([a-z]*)\] (.*)/\1,\2,\3,\4/' | sed -E -f ./scripts/event_append.sed >> $outputFileName
