echo '---killing mtr_service.py'
sudo kill -9 `ps -ef | grep "mtr_service.py" | grep -v "grep" | awk '{ print $2 }'`
sleep 1
echo '---killing startup_mtr.sh'
sudo kill -9 `ps -ef | grep "startup_mtr.sh" | grep -v "grep" | awk '{ print $2 }'`
