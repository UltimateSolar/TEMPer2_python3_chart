#!/bin/bash
# take meassurement with TEMPer2 USB thermometer every 3sec

LOGFILE=/home/user/projects/temper/data/$(date '+%Y-%m-%d').TEMPer2.log;
while true;
do
	printf "\n$(date '+%Y-%m-%d===%H:%M:%S')\n" | tee -a $LOGFILE;
	/home/user/projects/temper/temper.py --json|grep "temperature"|tee -a $LOGFILE;
	sleep 60;
	clear;
done
