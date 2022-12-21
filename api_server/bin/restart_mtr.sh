#!/bin/shi
echo '-restarting'
echo '--kill all process'
sh kill_all_mtr.sh
echo '--startup'
nohup sh startup_mtr.sh >/dev/null 2<&1 &
echo '-restarted!'
