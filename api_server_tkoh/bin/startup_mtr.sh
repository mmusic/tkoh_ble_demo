#!/bin/sh

#sudo iw reg set HK
while true
do
  isRunning=$(ps -ef | grep "mtr_service.py" | grep -v "grep")
  if [ "$isRunning" ] ; then
    echo "mtrServer is running at `date`."
  else
    echo "starting mtrServer ..."
    nohup python3 /home/mtrec/Documents/mtr_server2/mtr_service.py >>/home/mtrec/Documents/mtr_server2/daily_log.out 2>&1 &
    echo "mtrServer starts (PID=$!)."
  fi
  sleep 10
done
