LOG=/root/automation/ehc/logs/config.log
echo "into web api" >> /root/automation/ehc/logs/config.log
cd /root/automation/web/web/ehc_web && source bin/activate && cd /root/automation/web/web/ehc_web/ehc/api && echo "haha" >> ${LOG} && python manage.py runserver 0.0.0.0:8000 >> /root/automation/ehc/logs/web_api.log 2>&1 
echo "exit web api" >> /root/automation/ehc/logs/config.log