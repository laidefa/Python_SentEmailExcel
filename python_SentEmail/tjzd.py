# encoding: utf-8
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
time1 = time.time()
import pandas as pd
import requests
from lxml import etree
import re
import datetime

url="https://cosx.org/archives/"
html=requests.get(url).content
selector=etree.HTML(html)
# print html
date=[]
url_list=[]
title=[]
date1=re.findall('<span class="date">(.*?)</span>',html,re.S)
for each in date1:
    # print each
    k = datetime.datetime.strptime(str(each), '%Y/%m/%d')
    # print k.strftime('%Y-%m-%d')
    date.append(k)


url_list1=selector.xpath('/html/body/div/article/main/ul/li/a/@href')
for each in url_list1:
    # print     "https://cosx.org"+str(each
    url_list.append("https://cosx.org"+each)
title1 = selector.xpath('/html/body/div/article/main/ul/li/a/text()')
for each in title1:
    # print each
    title.append(each)

print len(url_list),len(date),len(title)

pd.set_option('display.max_rows',None)
pd.set_option('display.max_colwidth',500)

df=pd.DataFrame({"日期":date,"标题":title,"链接":url_list})
# print df


####################数据框转html#############################
df_html = df.to_html(index=True)


# print df_html



#######################修改html样式##################################
html=str(df_html).replace('<table border="1" class="dataframe">','<table border="0" class="dataframe" style="width:100%" cellspacing="2" cellpadding="2">')

html=str(html).replace('<tr style="text-align: right;">',' <div style="text-align:center;width:100%;padding: 8px; line-height: 1.42857; vertical-align: top; border-top-width: 1px; border-top-color: rgb(221, 221, 221); background-color: #3399CC;color:#fff"><strong><font size="4">统计之都文章列表</font></strong></div><tr style="background-color:#FFCC99;text-align:center;">')

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

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

####################设置发送人#######################
sender = '1973536419@qq.com'

######################设置接收人#######################
receiver1 = 'defa.lai@cgtz.com'
receiver2 = '1973536419@qq.com'


#####################设置主题#######################
subject = '统计之都文章列表'


# print style2+html
#################设置发送内容:1：发送html表格数据########################

msg = MIMEText(style2+html,'html','utf-8')



############################设置一些附属表头参数#############################
msg['From']=formataddr(["推送君",sender])
msg['To']=formataddr(["赖德发",receiver1])
msg['To']=formataddr(["开心果汁",receiver2])



msg['Subject'] = Header(subject, 'utf-8')

###################################登陆邮箱发送##################################
username = '1973536419@qq.com'

########qq授权码(此处需要填写qq授权码)
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
print u'总共耗时：' + str(time2 - time1) + 's'








