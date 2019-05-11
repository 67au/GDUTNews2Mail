# GDUTNews2Mail

## 计划来源

为了方便查看学校的通知，制作了此定时抓取通知网信息并以邮件形式通知的爬虫。

## 准备工作

- 本程序运行环境是 python3 

- 安装依赖

```bash
pip3 install lxml
pip3 install requests
```

- 修改登陆用的帐号密码，位于 NewsLogin.py

```python
post_data = {
    'ctl00$ContentPlaceHolder1$userEmail':'********',   #帐号密码请通过学校获取
    'ctl00$ContentPlaceHolder1$userPassWord':'********',
    'ctl00$ContentPlaceHolder1$CheckBox1':'on',
    'ctl00$ContentPlaceHolder1$Button1':'登录',
    '__VIEWSTATE':'',
    '__EVENTVALIDATION':''
}
```

- 将 config.sample.ini 重命名为 config.ini 并按要求修改该配置

```bash
[SMTP]
HostServer = smtp.example.com   ;SMTP服务器
Sender = admin@example.com      ;发件人邮箱
Password = yourpasswd           ;密码

[Profile]
SenderName = admin@example.com  ;发件人邮箱
ReceiverList = user1@example.com,user2@example.com  ;发件人列表，请使用","分隔
```

## 通过系统的定时任务运行脚本

如果是使用 GNU/Linux 系统可以使用 systemd 或 cron 定时运行脚本