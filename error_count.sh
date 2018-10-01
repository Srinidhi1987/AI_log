#!/usr/bin/sh

grep -i 'ERROR' out.log | cut -c1-16 | uniq -c  > .error_count

#awk '$1~/^[0-9]+$/' 'out.log' | cut -d ' ' -f 1,2,5 > .resp_time
# | cut -d ' ' -f 1,2,5 > .resp_time
