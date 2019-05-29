import pymysql.cursors
import pymysql
#import html
#import HTML
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from xlsxwriter.workbook import Workbook
from common_util import *
import xlwt
import csv
import pandas as pd
import datetime


#connecion string
#from db_jp_connection import get_connection 
connection = get_jp_connection()
#connecion string
date_value = datetime.date.today().strftime("%d-%b-%Y")



#SENDING MAIL
def fun_send_email(vHTML):
    #print 'start mail'
    fromaddr = "support@rbexplode.com"
    '''toaddr = ['aditya.Ahuja@rb.com','Shriram.K@rb.com','Faiz.Ahmed@rb.com','Tarun.Gupta@rb.com','Vanshika.Aggarwal@rb.com','Rohit.Iyer@rb.com','Salil.Mahajan@rb.com','Anusha.S@rb.com','Avin.Piparsania@rb.com','Cauvery.Varma@rb.com','Arpit.Aggarwal@rb.com','Jennifer.Jacob@rb.com' ,'Kalyan.Undinty@rb.com','ManishGirjanand.Jha@rb.com']'''
    toaddr =['suneel.dasila@rb.com']
    #cc = ['Rajendraa.Kumar@rb.com', 'Morajikumar.K@rb.com','prachi.prem@rb.com','Arvind.Kumar@rb.com','lokesh.taneja@rb.com','subhojeet.ghosh@rb.com']
    cc = ['lokesh.taneja@rb.com','subhojeet.ghosh@rb.com','arvind.kumar@rb.com','akash.rawat@rb.com']
    #bccaddrappend = ', '.join(bccaddr)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ",".join(toaddr)
    #msg['To'] = recipients
    msg['CC'] = ",".join(cc)
    #msg['Cc'] = ', '.join(ccaddr)
    #msg['bcc'] = ', '.join(bccaddr)
    #finaladr = toaddr + ccaddr + bccaddr
    #now = datetime.datetime.now()

    subject_value = "Japan ARAP Webpid Not Found " + date_value
    #file_path = "/usr/local/python/projectscraper_client/vendorcentral_data/"
    #os.chdir(file_path)
    filename_value = "WEBPID Not Found " + date_value + ".xlsx"
    msg['Subject'] = subject_value
    body = vHTML
    msg.attach(MIMEText(body, 'html'))
    # now attach the file
    get_attachment_file(filename_value)

    attachment = open(filename_value, "rb")
    #attachment = open("dashBoardReport.xlsx",
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename_value)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "dacc5ervces#rbhealth12@1")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr+cc , text)
    server.quit()
    #print 'end mail'

def get_attachment_file(filename_value):
	date_value_month = datetime.date.today().strftime("%m")
	vendorcentral_crawl_data = "SELECT * FROM vendorcentral_crawl where  brand is NULL and date(from_date) =(select date(max(from_date)) from vendorcentral_crawl)"
	print ('workbok created')

	try:
		cursor = connection.cursor()
		cursor.execute(vendorcentral_crawl_data)
		columns = [desc[0] for desc in cursor.description]
		data = cursor.fetchall()
		df = pd.DataFrame(list(data), columns=columns)
		writer = pd.ExcelWriter(filename_value)
		df.to_excel(writer, sheet_name='ARAP',index=False)
		writer.save()
		print ('workbok closed')
	except cursor.Error as e:
		print(e)
	finally:
		connection.close()

def write_html():
    print ('start')

    Message_TOP = '<html><body><table style="background:#fff;padding:10px;text-align:center" cellpadding="0" cellspacing="0" width="100%">\
                <tbody>\
                <tr>\
                <td colspan="6" style="font-size:13px;font-weight:400;color:#000;text-align:left">Dear Team,<br><br>Please find attach PID not found in master.</td>\
                </tr>\
                </tbody>\
                </table>'
    Message_FOOTER = '<table><tr> \
                        <td colspan="6" style="color:#000;font-weight:400;padding-top:15px;padding-bottom:15px;text-align:left">Regards,<br>RB Explode Support Team</td> \
                        </tr> \
                        </table></body></html>'
    vHTML = Message_TOP \
            + Message_FOOTER
    # new logic 
    subject_value = "Japan ARAP Webpid Not Found " + date_value

    filename_value = "WEBPID Not Found " + date_value + ".xlsx"
    get_attachment_file(filename_value)
    send_email('JVC', 'rbexplode', subject_value, vHTML, filename_value)
    # old
    #fun_send_email(vHTML)
    print ('complete')
    #print 'sucess'

#MAIN BODY
write_html()
#get_attachment_file()
