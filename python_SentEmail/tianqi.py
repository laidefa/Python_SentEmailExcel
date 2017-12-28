# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json
import jinja2
import os.path as pth
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

HEFEN_D = pth.abspath(pth.dirname(__file__))
LOCATION = '杭州'
ORIGINAL_URL =  'https://free-api.heweather.com/s6/weather/forecast?parameters'


def get_data():
  new_data = []
  parametres = {
    'location': LOCATION,
    'key': 'dd6acb5c29a0437e84708e9b82c46e83  ', #注册和风天气会给你一个KEY
    'lang': 'zh',
    'unit': 'm'
  }

  try:
    response = requests.get(ORIGINAL_URL,params=parametres)
    r = json.loads(json.dumps(response.text,ensure_ascii=False,indent=1))
    r = json.loads(response.text)
  except Exception as err:
    print(err)

  weather_forecast = r['HeWeather6'][0]['daily_forecast']
  for data in weather_forecast:
    new_obj = {}
    # 日期
    new_obj['date'] = data['date']
    # 日出时间
    new_obj['sr'] = data['sr']
    # 日落时间
    new_obj['ss'] = data['ss']
    # 最高温度
    new_obj['tmp_max'] = data['tmp_max']
    # 最低温度
    new_obj['tmp_min'] = data['tmp_min']
    # 白天天气状况描述
    new_obj['cond_txt_d'] = data['cond_txt_d']
    # 风向
    new_obj['wind_dir'] = data['wind_dir']
    # 风力
    new_obj['wind_sc'] = data['wind_sc']
    # 降水概率
    new_obj['pop'] = data['pop']
    # 能见度
    new_obj['vis'] = data['vis']

    new_data.append(new_obj)
  return new_data



def render_mail(data):
  env = jinja2.Environment(
      loader = jinja2.FileSystemLoader(HEFEN_D)
    )
  return env.get_template('hefentianqi.html').render({'data': data})


###################################发送电子邮件###################################



####################设置发送人#######################
sender = '1973536419@qq.com'

######################设置接收人#######################
# receiver1 = 'defa.lai@cgtz.com'
# receiver2 = '1973536419@qq.com'
receiver3='laidefa@dingtalk.com'


#####################设置主题#######################
subject = '别走，我给你看个宝贝'



#################设置发送内容:1：发送html表格数据########################
data = get_data()
body = render_mail(data)
msg = MIMEText(body,'html','utf-8')



############################设置一些附属表头参数#############################
msg['From']=formataddr(["赖德发",sender])
# msg['To']=formataddr(["赖德发",receiver1])
# msg['To']=formataddr(["开心果汁",receiver2])
msg['To']=formataddr(["赖德发",receiver3])


msg['Subject'] = Header(subject, 'utf-8')

###################################登陆邮箱发送##################################
username = '1973536419@qq.com'

#此处需要填写qq授权码
password = 'XXXXXXXXXXXXXXXX'


#################默认传输#################
# smtp = smtplib.SMTP_SSL("smtp.qq.com")


############################加密传送###################
smtp_server = 'smtp.qq.com'
smtp_port = 587
smtp = smtplib.SMTP(smtp_server, smtp_port)
smtp.starttls()
###########################################


smtp.login(username, password)
# smtp.sendmail(sender, [receiver1,receiver2,receiver3,receiver4], msg.as_string())

smtp.sendmail(sender, [receiver3], msg.as_string())
smtp.quit()

print '发送电子邮件完成...'

