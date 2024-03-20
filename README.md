## Overview
This repo has two files:

1. new\_entry.sh: a bash script that writes to a spreadsheet called time\_management\_sheet.csv
in your home directory.

2. get\_daily\_messages.py: a python script that takes a date as argument,
pulls messages from that day from chat\_db file on your computer,
and then calls (1) to put these into the spreadsheet.

The function of these files is to make easy the process of tracking your day.
This only works with a mac computer and iMessage.
