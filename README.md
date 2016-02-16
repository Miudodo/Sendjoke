笑话来源：易源_笑话大全http://apistore.baidu.com/apiworks/servicedetail/864.html

短信功能：使用139邮箱的免费发短信功能，需要实现139邮箱的登录

定时发送：
使用Linux 定时任务工具crontab

Vi /etc/crontab
在文件最后一行添加

00 9    * * *   root    python /root/Sendjoke.py
每天早上9:00 发送短信
