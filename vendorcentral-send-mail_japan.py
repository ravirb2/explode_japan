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
import numpy as np
import datetime


#connecion string
#from db_jp_connection import get_connection 
connection = get_jp_connection()
#connecion string

date_value = datetime.date.today().strftime("%d-%b-%Y")
date_value_day = datetime.date.today().strftime("%d")

date_value_month = datetime.date.today().strftime("%m")

yesterday = datetime.date.today() - datetime.timedelta(1)
last_day = yesterday.strftime('%d-%b-%Y')


first_day = yesterday.replace(day=1)
first_day = first_day.strftime('%d-%b-%Y')

now = datetime.datetime.now()
last_month = now.month-1 if now.month > 1 else 12
last_year=now.year
if last_month == 12:
	last_year=last_year-1
num_rec=1


vendorcentral_crawl_chk = "select vendorcentral_craw_id,from_date  from vendorcentral_crawl WHERE MONTH(from_date) =  MONTH(CURRENT_DATE()) AND YEAR(from_date) = YEAR(CURRENT_DATE()) ORDER BY from_date DESC"
cursor = connection.cursor()
cursor.execute(vendorcentral_crawl_chk)
data_chk = cursor.fetchall()
num_rec = len(data_chk)
num_rec1 = num_rec
if num_rec >0:
	last_date = data_chk[0]['from_date'].strftime('%d-%b-%Y')
else:
	vendorcentral_crawl_chk = "select vendorcentral_craw_id,from_date  from vendorcentral_crawl WHERE MONTH(from_date) =  "+str(last_month)+" AND YEAR(from_date) = "+str(last_year)+" ORDER BY from_date DESC"
	cursor = connection.cursor()
	cursor.execute(vendorcentral_crawl_chk)
	data_chk = cursor.fetchall()
	num_rec = len(data_chk)
	if num_rec >0:
		#last_date = cursor.fetchone()
		last_date = data_chk[0]['from_date'].strftime('%d-%b-%Y')
		first_day = data_chk[0]['from_date'].replace(day=1)
		first_day = first_day.strftime('%d-%b-%Y')


#SENDING MAIL
def fun_send_email(vHTML):
    print ('start mail')
    fromaddr = "support@rbexplode.com"
    #toaddr = ['aditya.Ahuja@rb.com','Shriram.K@rb.com','Faiz.Ahmed@rb.com','Tarun.Gupta@rb.com','Vanshika.Aggarwal@rb.com','Rohit.Iyer@rb.com','Salil.Mahajan@rb.com','Anusha.S@rb.com','Avin.Piparsania@rb.com','Cauvery.Varma@rb.com','Arpit.Aggarwal@rb.com','Jennifer.Jacob@rb.com' ,'Kalyan.Undinty@rb.com','ManishGirjanand.Jha@rb.com','priyanka.gaur@rb.com','Subhav.Joshi@rb.com']
    toaddr =['suneel.dasila@rb.com']
    #cc = ['suneel.dasila@rb.com']
    cc = ['Arvind.Kumar@rb.com','lokesh.taneja@rb.com','subhojeet.ghosh@rb.com','suneel.dasila@rb.com','akash.rawat@rb.com']
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

    subject_value = "Japan ARAP Data " + date_value
    #file_path = "/usr/local/python/projectscraper_client/vendorcentral_data/"
    #os.chdir(file_path)
    filename_value = "Japan ARAP Data " + date_value + ".xlsx"
    if date_value_day=='01':
        subject_value = "Japan ARAP Data " + first_day+" to "+last_date
        filename_value = "Japan ARAP Data " + first_day+"_to_"+last_date +".xlsx"
    if num_rec1==0:
        subject_value = "Japan ARAP Data Last month data"
        filename_value = "Japan ARAP Data" + str(last_month)+"_"+str(last_year) +".xlsx"
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
    print ('end mail')

def get_attachment_file(filename_value):
    date_value_month = datetime.date.today().strftime("%m")
    if date_value_day=='01':
        condition = " MONTH(from_date) = '"+str(last_month)+"' AND YEAR(from_date) ='"+str(last_year)+"'"
    else:
        condition = " MONTH(from_date) = MONTH(CURRENT_DATE()) AND YEAR(from_date) = YEAR(CURRENT_DATE())"

    if num_rec1==0:
        condition = " MONTH(from_date) = '"+str(last_month)+"' AND YEAR(from_date) ='"+str(last_year)+"'"
    vendorcentral_crawl_data ="select * from vendorcentral_crawl WHERE"+str(condition)
    print ('workbok created')

    try:
        cursor = connection.cursor()
        cursor.execute(vendorcentral_crawl_data)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(list(data), columns=columns)
        writer = pd.ExcelWriter(filename_value)
        df.to_excel(writer, sheet_name='vendor central',index=False)
        writer.save()
        print ('workbok closed')
    except cursor.Error as e:
        print(e)

def write_html():
    print ('start')
    date_value_month = datetime.date.today().strftime("%m")
    if date_value_day=='01':
        condition = " MONTH(from_date) = '"+str(last_month)+"' AND YEAR(from_date) ='"+str(last_year)+"'"
    else:
        condition = " MONTH(from_date) = MONTH(CURRENT_DATE()) AND YEAR(from_date) = YEAR(CURRENT_DATE())"

    if num_rec1==0:
        condition = " MONTH(from_date) = '"+str(last_month)+"' AND YEAR(from_date) ='"+str(last_year)+"'"
    vendorcentral_crawl_data ="select * from vendorcentral_crawl WHERE"+str(condition)
    #print 'workbok created'

    try:
        cursor = connection.cursor()
        cursor.execute(vendorcentral_crawl_data)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(list(data), columns=columns)
        df1 = df[['ordered_units','ordered_revenue','brand']]      
        df1['ordered_units']= df1['ordered_units'].apply(lambda x: float(x))
        df1['ordered_units']= df1['ordered_units'].apply(lambda x: round(x,2))
        df1['ordered_revenue']= df1['ordered_revenue'].apply(lambda x: float(x))
        df1['ordered_revenue']= df1['ordered_revenue'].apply(lambda x: round(x,2))
        df1.columns=['ORDERED UNITS','ORDERED REVENUE','BRAND']
        df1 = pd.pivot_table(df1,index=["BRAND"],values=["ORDERED UNITS","ORDERED REVENUE"],aggfunc=np.sum,fill_value=0,margins=True)
        col_order = ['ORDERED UNITS', 'ORDERED REVENUE']
        df1 = df1[col_order].rename(index=dict(All='Grand Total'))
        pivot_table_html= df1.to_html().replace('<table border="1" class="dataframe">','<table border="1" cellpadding="10" cellspacing="0">')
    except cursor.Error as e:
        print(e)
    print ('start')
    if date_value_day=='01' or num_rec1==0:
        Message_TOP = '<html><body><table style="background:#fff;padding:10px;text-align:center" cellpadding="0" cellspacing="0" width="100%">\
                    <tbody>\
                    <tr>\
                    <td colspan="6" style="font-size:13px;font-weight:400;color:#000;text-align:left">Dear Team,<br><br>Please review attached Amazon vendor central data ('+str(first_day)+' to  '+str(last_date)+').</td>\
                    </tr>\
                    </tbody>\
                    </table>' + pivot_table_html
        Message_FOOTER = '<table><tr> \
                            <td colspan="6" style="color:#000;font-weight:400;padding-top:15px;padding-bottom:15px;text-align:left">Regards,<br>RB Explode Support Team</td> \
                            </tr> \
                            </table></body></html>'
        vHTML = Message_TOP \
                + Message_FOOTER
    else:
        Message_TOP = '<html><body><table style="background:#fff;padding:10px;text-align:center" cellpadding="0" cellspacing="0" width="100%">\
                    <tbody>\
                    <tr>\
                    <td colspan="6" style="font-size:13px;font-weight:400;color:#000;text-align:left">Dear Team,<br><br>Please find the Japan ARAP data ('+str(first_day)+' to  '+str(last_date)+').</td>\
                    </tr>\
                    </tbody>\
                    </table>' + pivot_table_html
        Message_FOOTER = '<table><tr> \
                            <td colspan="6" style="color:#000;font-weight:400;padding-top:15px;padding-bottom:15px;text-align:left">Regards,<br>RB Explode Support Team</td> \
                            </tr> \
                            </table></body></html>'
        vHTML = Message_TOP \
                + Message_FOOTER
    #with open("email_output1.html", "w") as my_file:
        #my_file.write(vHTML)
    # new logic
    subject_value = "Japan ARAP Data " + date_value
    filename_value = "Japan ARAP Data " + date_value + ".xlsx"
    if date_value_day=='01':
        subject_value = "Japan ARAP Data " + first_day+" to "+last_date
        filename_value = "Japan ARAP Data " + first_day+"_to_"+last_date +".xlsx"
    if num_rec1==0:
        subject_value = "Japan ARAP Data Last month data"
        filename_value = "Japan ARAP Data" + str(last_month)+"_"+str(last_year) +".xlsx"
    get_attachment_file(filename_value)
    send_email('JVC', 'rbexplode', subject_value, vHTML, filename_value)

    # old logic
    #fun_send_email(vHTML)
    print ('complete')
    #print 'sucess'

#MAIN BODY
write_html()
connection.close()
#get_attachment_file()
