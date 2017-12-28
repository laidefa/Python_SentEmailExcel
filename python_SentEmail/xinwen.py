# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
import time
start_time = time.time()
import re
import requests
import pandas as pd

##############打印昨天####################
import datetime
now_time = datetime.datetime.now()
yes_time =now_time +datetime.timedelta(days=-1)
yes_time_nyr = yes_time.strftime('%Y%m%d')
print yes_time_nyr

url="http://tv.cctv.com/lm/xwlb/day/"+str(yes_time_nyr)+".shtml"

head={
    "Host": "tv.cctv.com",
    "Connection": "keep-alive",
    "Accept": "text/html, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
    "Referer": "http://tv.cctv.com/lm/xwlb/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8"
}

html=requests.get(url).content
# print html
title=[]
title1=re.findall('<div class="text"><div class="title">(.*?)</div><div class="bottom"',str(html),re.S)

for each in title1:
    # print each.replace("[视频]","")
    title.append(each.replace("[视频]",""))


data=pd.DataFrame({"主要内容":title})
data=data.iloc[1:,]

print data
####################数据框转html#############################
df_html = data.to_html(index=True)



#######################修改html样式##################################
html=str(df_html).replace('<table border="1" class="dataframe">','<table border="0" class="dataframe" style="width:100%" cellspacing="2" cellpadding="2">')

html=str(html).replace('<tr style="text-align: right;">',' <div style="text-align:center;width:100%;padding: 8px; line-height: 1.42857; vertical-align: top; border-top-width: 1px; border-top-color: rgb(221, 221, 221); background-color: #3399CC;color:#fff"><strong><font size="4">新闻联播日报</font></strong></div><tr style="background-color:#FFCC99;text-align:center;">')

html=str(html).replace('<tr>','<tr style="text-align:center">')

html=str(html).replace('<th></th>','<th>num</th>')
# print html


style1="""
<style type="text/css">
table {
border-right: 1px solid #CCCCCC;
border-bottom: 1px solid #CCCCCC;
}
table td {
border-left: 1px solid #CCCCCC;
border-top: 1px solid #CCCCCC;
}

</style>


"""



style2="""
<style type="text/css">
table {
border-right: 1px solid #99CCFF;
border-bottom: 1px solid #99CCFF;
}
table td {
border-left: 1px solid #99CCFF;
border-top: 1px solid #99CCFF;
}

table th {
border-left: 1px solid #99CCFF;
border-top: 1px solid #99CCFF;
}

</style>


"""


###################################发送电子邮件###################################
####################设置发送人#######################
sender = '1973536419@qq.com'

######################设置接收人#######################
receiver1 = 'defa.lai@cgtz.com'
receiver2 = '1973536419@qq.com'
#receiver3='laidefa@dingtalk.com'



#####################设置主题#######################
subject = '【新闻联播】带你看世界'



#################设置发送内容:1：发送html表格数据########################

msg = MIMEText(style2+html,'html','utf-8')

############################设置一些附属表头参数#############################
msg['From']=formataddr(["赖德发",sender])
msg['To']=formataddr(["赖德发",receiver1])
msg['To']=formataddr(["开心果汁",receiver2])


msg['Subject'] = Header(subject, 'utf-8')

###################################登陆邮箱发送##################################
###登录qq邮箱账号
username = '1973536419@qq.com'
####qq授权码(此处需要填写授权码)
password = 'XXXXXXXXXXXXXX'


#################默认传输#################
# smtp = smtplib.SMTP_SSL("smtp.qq.com")


############################加密传送###################
smtp_server = 'smtp.qq.com'
smtp_port = 587
smtp = smtplib.SMTP(smtp_server, smtp_port)
smtp.starttls()
###########################################


smtp.login(username, password)
smtp.sendmail(sender, [receiver1,receiver2], msg.as_string())

# smtp.sendmail(sender, [receiver1,receiver2,receiver3], msg.as_string())
smtp.quit()

print '发送电子邮件完成...'

time2=time.time()
print u'总共耗时：' + str(time2 - start_time) + 's'
