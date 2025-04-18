echo "PWD is: $(pwd)" >&2

#!/usr/bin/env bash
input_file=$1
start_datetime=$2
end_datetime=$3
output_file=$4

#Debug
echo $input_file
echo $start_datetime
echo $end_datetime
echo $output_file

#Firstly, remove header and carriage return from the file, and make a new file.
tail -n +2 "$input_file" | sed 's/\r//g' > cleaned.log

#Now, get the time stamps from the log.
cut -d, -f2 cleaned.log > timestamps.txt

#Use the date command to convert the timestamps to iso format.
date -I'seconds' --file=timestamps.txt > iso.txt

#Append these iso formats to cleaned.log
cat cleaned.log | paste -d, - iso.txt > appended.log

#Debug
echo "Start: $start_datetime | End: $end_datetime" >&2
head -n 3 appended.log >&2

#Conditionally append the lines of the file which correspond to ISO times between start_date and end_date.
awk -f ./scripts/filter.awk -v start_datetime="$start_datetime" -v end_datetime="$end_datetime" < appended.log > "$4"

#Cleanup
rm cleaned.log timestamps.txt iso.txt appended.log
