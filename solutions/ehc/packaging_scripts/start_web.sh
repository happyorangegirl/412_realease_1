# Script used to start web server
firewall-cmd --zone=public --add-service=http --permanent
firewall-cmd --zone=public --add-port=8000/tcp --permanent
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --zone=public --add-port=8888/tcp --permanent
firewall-cmd --reload
echo "start web api server on port 8000..." >> /root/automation/ehc/logs/config.log
./start_web_api.sh &
echo "start web api server on port 8888..." >> /root/automation/ehc/logs/config.log
./start_web_ui.sh &
