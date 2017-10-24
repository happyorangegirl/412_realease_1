echo "into web ui" >> /root/automation/ehc/logs/config.log
cd /root/automation/web/web/ehc_web;source bin/activate && cd /root/automation/web/web/ehc_web/ehc/ui/dist && ((python -m SimpleHTTPServer 8888 2>&1) >> /root/automation/ehc/logs/web_ui.log) 
echo "exit web api" >> /root/automation/ehc/logs/config.log