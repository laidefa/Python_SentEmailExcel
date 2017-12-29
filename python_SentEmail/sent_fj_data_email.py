# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import csv
import smtplib
from email.header import Header as _Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import  numpy as np

from mako.template import Template
from mako.lookup import TemplateLookup
import pandas as pd
HERE = os.path.abspath(os.path.dirname(__file__))
SMTP_SERVER = 'smtp.qq.com'

# 使用标准的25端口连接SMTP服务器是明文传输，发送过程中可能会被窃听。
# 这里选择加密SMTP会话， 更安全地发送邮件
SMTP_PORT = 587

############################发件人###########################
FROM_ADDR = '1973536419@qq.com'
######此处填写qq邮箱授权码
PASSWORD = 'XXXXXXXXXXXXXXXXX'


###########################收件人设置#########################
TO_ADDRS = ['defa.lai@cgtz.com','1973536419@qq.com']


#定义模板
def mako_render(data, mako_file, directories):
    mylookup = TemplateLookup(directories=directories, input_encoding='utf-8',
                              output_encoding='utf-8',
                              default_filters=['decode.utf_8'])
    mytemplate = Template('<%include file="{}"/>'.format(mako_file),
                          lookup=mylookup, input_encoding='utf-8',
                          default_filters=['decode.utf_8'],
                          output_encoding='utf-8')
    content = mytemplate.render(**data)
    return content

###定义表头名称
def Header(name):  # noqa
    return _Header(name, 'utf-8').encode()

###定义表头地址
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name), addr))

###定义短信内容
def gen_msg(content, subject, attachments, nick_from=None, nick_to=None):
    if nick_from is None:
        nick_from = FROM_ADDR

    if nick_to is None:
        nick_to=TO_ADDRS

    msg = MIMEMultipart()
    msg['From'] = _format_addr('{} <{}>'.format(nick_from, FROM_ADDR))

    for TO_ADDRS1 in TO_ADDRS:
        #########隐藏收件人
        # msg['To'] = _format_addr('{} <{}>'.format(nick_to, TO_ADDRS1))

        ########显示收件人###################################
        msg['To'] = _format_addr('{} <{}>'.format(TO_ADDRS1, TO_ADDRS1))

    msg['Subject'] = Header(subject)
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    for attachment in attachments:
        attach = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf-8')
        attach['Content-Type'] = 'application/octet-stream'
        attach['Content-Disposition'] = 'attachment; filename="{}"'.format(
        os.path.basename(attachment))
        msg.attach(attach)
    return msg


##发送邮件
def sendmail(content, subject, attachments, nick_from=None):
    msg = gen_msg(content, subject, attachments, nick_from)
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(FROM_ADDR, PASSWORD)
    server.sendmail(FROM_ADDR, TO_ADDRS, msg.as_string())

    server.quit()




###主函数
def main():

    #########################读取csv文件############################

    data = pd.read_excel("c:/pic/wang.xlsx")
    kk = len(data)
    a = np.array(data.iloc[:, 1:7], dtype=str)
    rows_data = a.tolist()

    row_headers=[]

    col_headers = ['日期','排名','平台名称','成交量(万元)','平均利率(%)','平均借款期限(月)','累计待还款金额(万元)']

    for i in range(0,kk):
        # print data.iloc[:,0]
        row_headers.append('2016-05-29')
    data = {'rows_data': rows_data, 'row': col_headers,
            'row_headers': row_headers}


    #################定义文件路径####################
    tmpl_directories = 'c:/pic/tmpl'

    csv_file="c:/pic/wang.xlsx"

    ######渲染数据
    content = mako_render(data, 'statistics.txt', directories=tmpl_directories)
    #######################
    sendmail(content, u'核心用户运营数据', [csv_file], nick_from=u'赖德发')

if __name__ == '__main__':
    main()
    print u'发送邮件完成！'














