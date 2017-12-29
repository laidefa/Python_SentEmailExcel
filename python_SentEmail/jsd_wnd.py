# encoding: utf-8
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
time1 = time.time()
import pandas as pd
import pymysql


############################################从数据库读数据###########################################
## 加上字符集参数，防止中文乱码
dbconn=pymysql.connect(
  host="XXXXXXXXXXXX",
  database="cgjr",
  user="XXXXXX",
  password="XXXXXXXXX",
  port=XXXX,
  charset='utf8'
 )

#sql语句
sqlcmd="""



SELECT
SUBDATE(CURDATE(),INTERVAL 1 day) as "日期",
"微农贷" as '产品',
sum(IF(DATE_FORMAT(t.apply_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d'),1,0)) as "当日申请数量",
sum(IF(DATE_FORMAT(t.audit_pass_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d') and t.STATUS in (111,101,202,108,105,106,107),1,0)) as "当日通过数量",
sum(IF(DATE_FORMAT(t.audit_pass_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d') and t.STATUS in (111,101,202,108,105,106,107),t.borrow_amount,0)) as '当日审批金额',
sum(IF(DATE_FORMAT(t.loan_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d') and t.STATUS in (105),t.borrow_amount,0)) as '当日放款金额',
sum(IF(DATE_FORMAT(t.loan_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d') and t.STATUS in (105),1,0)) as '当日放款数量'
FROM t_order_info as t,(SELECT @mytime:=SUBDATE(CURDATE(),INTERVAL 1 day)) t_order_info
 WHERE model_id=6



UNION all

SELECT
DATE_FORMAT(@mytime, '%Y-%m-%d') as "日期",
"及时贷" as '产品',
sum(IF(DATE_FORMAT(t.apply_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d'),1,0)) as "当日申请数量",
sum(IF(DATE_FORMAT(t.audit_pass_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d') and t.STATUS in (111,101,202,108,105,106,107),1,0)) as "当日通过数量",
sum(IF(DATE_FORMAT(t.audit_pass_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d') and t.STATUS in (111,101,202,108,105,106,107),t.borrow_amount,0)) as '当日审批金额',
sum(IF(DATE_FORMAT(t.loan_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d') and t.STATUS in (105),t.borrow_amount,0)) as '当日放款金额',
sum(IF(DATE_FORMAT(t.loan_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d') and t.STATUS in (105),1,0)) as '当日放款数量'
FROM t_order_info as t,(SELECT @mytime:=SUBDATE(CURDATE(),INTERVAL 1 day)) t_order_info
 WHERE model_id=13





union all

SELECT
DATE_FORMAT(@mytime, '%Y-%m-%d') as "日期",
"汇总" as '产品',
sum(IF(DATE_FORMAT(t.apply_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d'),1,0)) as "当日申请数量",
sum(IF(DATE_FORMAT(t.audit_pass_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d') and t.STATUS in (111,101,202,108,105,106,107),1,0)) as "当日通过数量",
sum(IF(DATE_FORMAT(t.audit_pass_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d') and t.STATUS in (111,101,202,108,105,106,107),t.borrow_amount,0)) as '当日审批金额',
sum(IF(DATE_FORMAT(t.loan_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d') and t.STATUS in (105),t.borrow_amount,0)) as '当日放款金额',
sum(IF(DATE_FORMAT(t.loan_time, '%Y-%m-%d') = DATE_FORMAT(@mytime, '%Y-%m-%d') and t.STATUS in (105),1,0)) as '当日放款数量'
FROM t_order_info as t,(SELECT @mytime:=SUBDATE(CURDATE(),INTERVAL 1 day)) t_order_info

WHERE model_id in(6,12,13)





"""

#利用pandas 模块导入mysql数据
data=pd.read_sql(sqlcmd,dbconn)


print data
####################数据框转html#############################
df_html = data.to_html(index=False)


# print df_html



#######################修改html样式##################################
html=str(df_html).replace('<table border="1" class="dataframe">','<table border="0" class="dataframe" style="width:80%" cellspacing="2" cellpadding="2">')

html=str(html).replace('<tr style="text-align: right;">',' <div style="text-align:center;width:78.76%;padding: 8px; line-height: 1.42857; vertical-align: top; border-top-width: 1px; border-top-color: rgb(221, 221, 221); background-color: #3399CC;color:#fff"><strong><font size="4">金爱农运营数据统计日报</font></strong></div><tr style="background-color:#FFCC99;text-align:center;">')

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
# receiver3='fang.chen@lg-finance.com'

#####################设置主题#######################
subject = '金爱农运营数据统计日报'


# print style2+html
#################设置发送内容:1：发送html表格数据########################

msg = MIMEText(style2+html,'html','utf-8')



############################设置一些附属表头参数#############################
msg['From']=formataddr(["运营官",sender])
msg['To']=formataddr(["赖德发",receiver1])
msg['To']=formataddr(["开心果汁",receiver2])



msg['Subject'] = Header(subject, 'utf-8')

###################################登陆邮箱发送##################################
username = '1973536419@qq.com'

#此处填写qq邮箱授权码
password = 'XXXXXXXXXXXXXXXXX'


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








