import smtplib, json
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import pymysql.cursors
from dateutil import tz
from datetime import datetime
from pytz import timezone
import requests
usa_time = timezone('US/Eastern')
sa_time = datetime.now(usa_time)

def send_email_us(project, subject, email_body, attachment):
    # email_server is used us or rbexplode
    response = requests.get('http://daccservces.com/mail_monitor_us/mail_shoot?mail_type='+project)
    data = response.json()
    to_email = data['data']['to']
    cc_email = data['data']['cc']
    bcc_address = data['data']['bcc']
    link = '<img src='+'"'+str(data['data']['mail_acknowledgment_link'])+'"'+'alt="rb" height="42" width="42">'
    email_body = email_body+link    
    # email server is used rbexplode
    fun_send_email_us(to_email, cc_email, bcc_address, subject, email_body, attachment)
    
def send_email(project, email_server, subject, email_body, attachment):
    # email_server is used us or rbexplode
    response = requests.get('http://daccservces.com/mail_monitor/mail_shoot?mail_type='+project)
    data = response.json()
    to_email = data['data']['to']
    cc_email = data['data']['cc']
    bcc_address = data['data']['bcc']
    link = '<img src='+'"'+str(data['data']['mail_acknowledgment_link'])+'"'+'alt="rb" height="42" width="42">'
    email_body = email_body+link
    if email_server == "rbexplode":
        # email server is used us
        fun_send_email(to_email, cc_email, bcc_address, subject, email_body, attachment)
    if email_server == "us":
        # email server is used rbexplode
        fun_send_email_us(to_email, cc_email, bcc_address, subject, email_body, attachment)

def fun_send_email_us(to_email, cc_email, bcc_address, subject, email_body, attachment):    
    try:
        fromaddr = "ecommerce.us@rb.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ",".join(to_email)
        msg['CC'] = ",".join(cc_email)
        if len(bcc_address) >0:
            msg['Bcc'] =",".join(bcc_address)
        msg['Subject'] = subject

        msg.attach(MIMEText(email_body, 'html',_charset="UTF-8"))
        
        if attachment:        
            attach = open(attachment, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attach).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % attachment)
            msg.attach(part)
        
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(fromaddr, "Passw0rd$2")
        text = msg.as_string()
        server.sendmail(fromaddr, to_email+cc_email+bcc_address , text)
        server.quit()
        return True    
    except Exception as e:
        return str(e)

def fun_send_email(to_email, cc_email, bcc_address, subject, email_body, attachment):
    
    try:
        fromaddr = "support@rbexplode.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ",".join(to_email)
        msg['CC'] = ",".join(cc_email)
        if len(bcc_address) >0:
            msg['Bcc'] =",".join(bcc_address)

        msg['Subject'] = subject
        msg.attach(MIMEText(email_body, 'html',_charset="UTF-8"))
        
        if attachment:        
            attach = open(attachment, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attach).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % attachment)
            msg.attach(part)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "dacc5ervces#rbhealth12@1")
        text = msg.as_string()
        server.sendmail(fromaddr, to_email+cc_email+bcc_address , text)
        server.quit()
        return True    
    except Exception as e:
        return str(e)

        
def send_email_temp(project, email_server, subject, email_body, attachment,attachment1):
    # email_server is used us or rbexplode
    response = requests.get('http://daccservces.com/mail_monitor/mail_shoot?mail_type='+project)
    data = response.json()
    to_email = data['data']['to']
    cc_email = data['data']['cc']
    bcc_address = data['data']['bcc']
    link = '<img src='+'"'+str(data['data']['mail_acknowledgment_link'])+'"'+'alt="rb" height="42" width="42">'
    email_body = email_body+link
    if email_server == "rbexplode":
        # email server is used us
        fun_send_email_temp(to_email, cc_email, bcc_address, subject, email_body, attachment, attachment1)

        
def fun_send_email_temp(to_email, cc_email, bcc_address, subject, email_body, attachment, attachment1):    
    try:
        fromaddr = "support@rbexplode.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ",".join(to_email)
        msg['CC'] = ",".join(cc_email)
        if len(bcc_address) >0:
            msg['Bcc'] =",".join(bcc_address)

        msg['Subject'] = subject
        msg.attach(MIMEText(email_body, 'html',_charset="UTF-8"))
        
        if attachment:        
            attach = open(attachment, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attach).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % attachment)
            msg.attach(part)
            
        if attachment1:        
            attach1 = open(attachment1, "rb")
            part1 = MIMEBase('application', 'octet-stream')
            part1.set_payload((attach1).read())
            encoders.encode_base64(part1)
            part1.add_header('Content-Disposition', "attachment1; filename= %s" % attachment1)
            msg.attach(part1)
            
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "dacc5ervces#rbhealth12@1")
        text = msg.as_string()
        server.sendmail(fromaddr, to_email+cc_email+bcc_address , text)
        server.quit()
        return True    
    except Exception as e:
        return str(e)
        
def get_connection_bfcm_india():
    connection = pymysql.connect(host='3.17.49.11',
    user='bfcm',
    password='Zaqxsw123jhytredknrs',
    db='indiahealth_rt',
    charset='utf8',
    local_infile=True,
    cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_connection_bfcm_latam():
    connection = pymysql.connect(host='3.17.49.11',
    user='bfcm',
    password='Zaqxsw123jhytredknrs',
    #port=2499,
    db='latam',
    charset='utf8',
    local_infile=True,
    cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_connection_rt():
	connection = pymysql.connect(host='3.17.49.11',
	user='bfcm',
	password='Zaqxsw123jhytredknrs',
	#port=2499,
	db='indiahealth_rt',
	charset='utf8',
	local_infile=True,
	cursorclass=pymysql.cursors.DictCursor)
	return connection  
    
def get_connection_bfcn():
	connection = pymysql.connect(host='3.17.49.11',
	user='bfcm',
	password='Zaqxsw123jhytredknrs',
	#port=2499,
	db='bfcm',
	charset='utf8',
	local_infile=True,
	cursorclass=pymysql.cursors.DictCursor)
	return connection
	
def get_connection_explode_us():
	connection = pymysql.connect(host='3.17.49.11',
	user='bfcm',
	password='Zaqxsw123jhytredknrs',
	#port=2499,
	db='rbexplode_us',
	charset='utf8',
	local_infile=True,
	cursorclass=pymysql.cursors.DictCursor)
	return connection


def get_connection_supply_excellence():
    connection = pymysql.connect(host='104.211.227.184',
    user='rbdbuser',
    password='Zaqxsw123!@#UhtR12',
    #port=2499,
    db='supply_excellence',
    charset='utf8',
    local_infile=True,
    cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_connection():
	connection = pymysql.connect(host='104.211.227.184',
	user='rbdbuser',
	password='Zaqxsw123!@#UhtR12',
	#port=2499,
	db='rbexplode_final',
	charset='utf8',
	local_infile=True,
	cursorclass=pymysql.cursors.DictCursor)
	return connection

def get_id_connection():
	connection = pymysql.connect(host='3.18.127.118',
	user='rbuser',
	password='ohr6ePEVJASbrbhealth',
	#port=2499,
	db='rbexplode_id',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection
    
def get_connection_india_home():
	connection = pymysql.connect(host='104.211.227.184',
	user='rbdbuser',
	password='Zaqxsw123!@#UhtR12',
	#port=2499,
	db='india_home',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection
    
def get_sg_connection():
	connection = pymysql.connect(host='3.18.127.118',
	user='rbuser',
	password='ohr6ePEVJASbrbhealth',
	#port=2499,
	db='rbexplode_sg',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection
def get_th_connection():
	connection = pymysql.connect(host='3.18.127.118',
	user='rbuser',
	password='ohr6ePEVJASbrbhealth',
	#port=2499,
	db='rbexplode_th_final',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection

def get_my_connection():
	connection = pymysql.connect(host='3.18.127.118',
	user='rbuser',
	password='ohr6ePEVJASbrbhealth',
	#port=2499,
	db='rbexplode_my',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection

def get_bd_connection():
	connection = pymysql.connect(host='104.211.227.184',
	user='rbdbuser',
	password='Zaqxsw123!@#UhtR12',
	#port=2499,
	db='rbexplode_bd',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection
	
def get_lk_connection():
	connection = pymysql.connect(host='104.211.227.184',
	user='rbdbuser',
	password='Zaqxsw123!@#UhtR12',
	#port=2499,
	db='rbexplode_lk',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection

def get_vn_connection():
	connection = pymysql.connect(host='3.18.127.118',
	user='rbuser',
	password='ohr6ePEVJASbrbhealth',
	#port=2499,
	db='rbexplode_vn',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection

def get_ph_connection():
	connection = pymysql.connect(host='3.18.127.118',
	user='rbuser',
	password='ohr6ePEVJASbrbhealth',
	#port=2499,
	db='rbexplode_ph',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection
	
def get_middle_east_connection():
	connection = pymysql.connect(host='104.211.227.184',
	user='rbdbuser',
	password='Zaqxsw123!@#UhtR12',
	#port=2499,
	db='rbexplode_middle_east',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection
	
def get_sa_connection():
	connection = pymysql.connect(host='104.211.227.184',
	user='rbdbuser',
	password='Zaqxsw123!@#UhtR12',
	#port=2499,
	db='rbexplode_sa',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection
    
def get_ng_connection():
	connection = pymysql.connect(host='104.211.227.184',
	user='rbdbuser',
	password='Zaqxsw123!@#UhtR12',
	#port=2499,
	db='rbexplode_ng',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection

def get_pk_connection():
	connection = pymysql.connect(host='104.211.227.184',
	user='rbdbuser',
	password='Zaqxsw123!@#UhtR12',
	#port=2499,
	db='rbexplode_pk',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection
	

def get_eg_connection():
	connection = pymysql.connect(host='104.211.227.184',
	user='rbdbuser',
	password='Zaqxsw123!@#UhtR12',
	#port=2499,
	db='rbexplode_eg',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection
    
def get_jp_connection():
	connection = pymysql.connect(host='3.18.127.118',
	user='rbuser',
	password='ohr6ePEVJASbrbhealth',
	#port=2499,
	db='rbexplode_jp1',
	charset='utf8',
	cursorclass=pymysql.cursors.DictCursor)
	return connection    
    
def remove_special_chars(original_string,str_type):
    if str_type == '1':
        new_string = re.sub('[^a-zA-Z0-9\n\.\+\-]', ' ', original_string)
    else:
        new_string = re.sub('[^a-zA-Z0-9\n\.\-\/]', '', original_string)
    return new_string

def update_cron_status(kpi_id,kpi_name,run_status):
    response = requests.get('http://3.18.52.77/app/cron_log_status.php?kpi_id='+str(kpi_id)+'&kpi_name='+str(kpi_name)+'&run_status='+str(run_status))
    res = response.content
    print(str(res.decode('utf-8')))

def get_cron_info(kpi_id):
    # this is used to check cron active or inactive
    response = requests.get('http://3.18.52.77/app/cron_details.php?kpi_id='+str(kpi_id))
    try:
        data = json.loads(response.content)
        if data['status'] == "1":
            print("Active");
        else:
            print("Deactive");
            quit();
    except Exception as e:
        print(e)
    






