echo '---killing mtr_service.py'
sudo kill -9 `ps -ef | grep "mtr_service.py" | grep -v "grep" | awk '{ print $2 }'`
