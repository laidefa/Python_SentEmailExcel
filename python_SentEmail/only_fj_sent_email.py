#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


########导入样式模板库
from mako.template import Template
from mako.lookup import TemplateLookup

#######导入邮件库
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from email.mime.multipart import MIMEMultipart

#####导入数据处理相关库
import pandas as pd
import numpy as np
import  pymysql

####################设置发送人#######################
sender = '297409674@qq.com'

######################设置接收人#######################
receiver1 = '297409674@qq.com'
receiver2='fang.chen@lg-finance.com'

#####################设置主题#######################
subject = '催收数据'



#################设置发送内容:1：发送html表格数据########################
# 创建连接
conn = pymysql.connect(host='XXXX', port=XXXX,user='XX', password='XXXX', database='cgjr', charset='utf8')

sql1="""
#此处填写sql语句
"""


sql2="""
#此处填写sql语句
"""


##########利用pandas 模块导入mysql数据
data1=pd.read_sql(sql1,conn)
data2=pd.read_sql(sql2,conn)


########把数据写到本地excel，这里写到E盘
writer = pd.ExcelWriter("E:/overdue_data.xlsx")
data1.to_excel(writer,'Sheet1',index=False)
data2.to_excel(writer,'Sheet2',index=False)


###关闭所有连接
writer.save()
conn.close()

############################设置一些附属表头参数#############################
msg = MIMEMultipart()
msg['From']=formataddr(["测试邮件",sender])
msg['To']=formataddr(["陈芳",receiver1])
msg['To']=formataddr(["陈芳2",receiver2])


msg['Subject'] = Header(subject, 'utf-8')

msg.attach(MIMEText('这是菜鸟教程Python 邮件发送测试……', 'plain', 'utf-8'))


# 构造附件1，传送当前目录下的 test.txt 文件
att1 = MIMEText(open('E:/overdue_data.xlsx', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'


# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename="overdue_data.xlsx"'
msg.attach(att1)



###################################登陆邮箱发送##################################

username = '297409674@qq.com'

##此处填写qq邮箱授权码
password = 'XXXXXXXXX'


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
smtp.quit()
print "邮件已发送成功"























