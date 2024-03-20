#!/bin/bash
#writes to time management csv file, by Avik Garg
#entries should have form [date] [thing] [start_time] [end_time]
#date can have format MMDDYYYY, MM-DD-YYYY, MM/DD/YYYY, and a few more
#time should have format XX:XX in 24-hour time
if [ $# != 5 ]
then
    exit 1
fi

clean_date=$( echo $1 | sed 's/[/:\]/-/g' )
if [ ${#clean_date} -eq 8 ]
then
    if [ ${clean_date:2:0} = '-' ]
    then
        clean_date="${clean_date:0:2}-${clean_date:2:2}-${clean_date:4:4}"
    else
        clean_date="${clean_date:0:6}20${clean_date:6:2}"
    fi
fi

#let end_min=${4:0:2}\*60+${4:3:2}
#let start_min=${3:0:2}\*60+${3:3:2}
#let time_spent=$end_min-$start_min

echo "$clean_date,$2,$3,$4,$5" >> ~/Desktop/projects/time_management_sheet/time_management_sheet.csv
