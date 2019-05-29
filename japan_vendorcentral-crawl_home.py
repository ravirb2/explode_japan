#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from common_util import *
import requests
import time
import datetime
import csv
from dateutil import parser
import os
import random
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options 

options = Options()
#options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
#options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options, executable_path=r'C:\\driver\\chromedriver.exe')


#connecion string
connection = get_jp_connection()
#connecion string

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
keywords = []
brands = []
locations = []
index = 0
keyword_count = 0


user_email = 'akash.rawat@rb.com'
user_pass =  '123456789'
login_detils = []
login_detils.append(['akash.rawat@rb.com', '123456789'])
login_detils.append(['akash.rawat@rb.com', '123456789'])


vpf_id = '200' 			# VENDORCENTRAL
vcrawl_id = '0'			## MASTER
vkeyword = '0'			## MASTER
vkeyword_id = '0'		## MASTER
vbrand_id = '0'			## MASTER
vbrand_name = '0'		## MASTER
vlocation_id = '0'		## MASTER
vlocation_name = '0'	## MASTER
vpincode = '0'			## MASTER
vcreated_by= 'System'	#$ DEFAULT
update_flag= False
sales_view ='Ordered Revenue'

def vendorcentral_login(user_email,user_pass):
    driver.get('https://arap.amazon.co.jp/')
    time.sleep(7) # Let the user actually see something!   //*[@id="login-button-container"]  
    try:
        driver.find_element_by_xpath( ".//*[@id='ap_email']" ).send_keys(user_email); 
    except NoSuchElementException:
        print('ap_email not found')
        try:
            driver.find_element_by_css_selector('#ap_email').send_keys(user_email); 
        except NoSuchElementException:
            print('ap_email not found again')
            login = random.choice(login_detils)
            vendorcentral_login(login[0],login[1])
    try:
        driver.find_element_by_xpath( ".//*[@id='ap_password']" ).send_keys(user_pass); 
    except NoSuchElementException:
        print('ap_password not found')
        try:
            driver.find_element_by_css_selector('#ap_password').send_keys(user_pass); 
        except NoSuchElementException:
            print('ap_password not found')
            login = random.choice(login_detils)
            vendorcentral_login(login[0],login[1])


    driver.find_element_by_xpath( ".//*[@id='signInSubmit']" ).click()
    time.sleep(6) # Let the user actually see something!
    try:
        driver.get('https://arap.amazon.co.jp/dashboard/salesDiagnostic')
        time.sleep(10)
    except:
        print('no element')
        
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div[2]/div[4]/div[2]/div/div[1]/span[2]/div').click()  # for sales view
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div[2]/div[4]/div[2]/div/div[1]/span[2]/div/awsui-button-dropdown/div/div/ul/li[1]').click()  #for sales view
    time.sleep(5)        
    driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div[2]/div[4]/div[2]/div/div[3]/span[1]/div').click()  # for click on daily view
    time.sleep(5) # Let the user actually see something!
    driver.find_element_by_xpath( '//*[@id="root"]/div/div/div[1]/div[2]/div[4]/div[2]/div/div[3]/span[1]/div/awsui-button-dropdown/div/div/ul/li[1]').click()
    time.sleep(3) # Let the user actually see something!


    # download
    driver.find_element_by_xpath( '//*[@id="root"]/div/div/div[1]/div[2]/div[4]/div[2]/div/div[4]/span/div/awsui-button[2]/button').click()
    time.sleep(3)
    driver.find_element_by_xpath( '//*[@id="root"]/div/div/div[1]/div[2]/div[4]/div[1]/div[2]/div/div[1]/awsui-button-dropdown/div/button').click()
    time.sleep(7)
    try:
        driver.find_element_by_xpath('//*[@id="root"]/div/div/div[1]/div[2]/div[4]/div[1]/div[2]/div[1]/div[1]/awsui-button-dropdown/div/div/ul/li[3]/ul/li[2]').click()
        time.sleep(8) 
    except Exception as e: 
        time.sleep(5) 
        

def crawl_update(update_flag):
    try:
        if update_flag is True:
            with connection.cursor() as cursor:
                print('status updated')
                allasin =[]
                cursor.execute("SELECT DISTINCT asin FROM vendorcentral_crawl where date(created_on) =(select date(max(created_on)) from vendorcentral_crawl)")
                asin_name = cursor.fetchall()
                for  brand  in asin_name:
                    allasin.append(brand['asin'])
                cursor.execute("SELECT (select pf_name from rb_platform where pf_id= sp.pf_id) as pf_name, sp.web_pid as web_pid , (SELECT brand_name FROM rb_brands WHERE brand_id= sp.brand_id) AS brand_name FROM rb_sku_platform sp where sp.pf_id in ('1')")
                brand_dim=[]
                for brand  in cursor.fetchall():
                    brand_dim.append(dict([('pf_name',brand['pf_name']),('web_pid',brand['web_pid']),('brand_name',brand['brand_name'])]))
                
                allbrand=[]
                for brand in brand_dim:
                    allbrand.append(brand['web_pid'])
                web_pid_found =[]       
                web_pid_found= list(set(allbrand)&set(allasin))
                if len(web_pid_found) >=1:
                    for asin_code in web_pid_found:
                        cursor.execute("SELECT * FROM vendorcentral_crawl where asin ='"+asin_code+"' and date(created_on) =(select date(max(created_on)) from vendorcentral_crawl)")
                        sql2_title = cursor.fetchall()
                        for sql2_final_title in sql2_title:
                            vendorcentral_craw_id=sql2_final_title['vendorcentral_craw_id']
                            asin_code=sql2_final_title['asin']
                            for a in brand_dim:
                                pf_name =a['pf_name']
                                if a['web_pid'] == asin_code:                                    
                                    cursor.execute("UPDATE vendorcentral_crawl SET  brand = '"+str(a['brand_name'])+"',pf_name = '"+str(a['pf_name'])+"' WHERE vendorcentral_craw_id='"+str(vendorcentral_craw_id)+"' and asin ='"+str(asin_code)+"'") 
                                    connection.commit()
                            
    except cursor.Error as e:
        e=str(e)
        print(e)
    
try:
	with connection.cursor() as cursor:
		filename ='C:\\Users\\Administrator\\Downloads\\Sales Diagnostic_Detail View_JP.csv' 
		try:
			os.remove(filename)
		except OSError:
			pass  
		sales_view ='Ordered Revenue'
		login = random.choice(login_detils)
		vendorcentral_login(login[0],login[1])
		print('completed')
		time.sleep(1) # Let the user actually see something!
		index=0
		file=open("C:\\Users\\Administrator\\Downloads\\Sales Diagnostic_Detail View_JP.csv", encoding="utf8")
		csv_data = csv.reader(file)
		for row in csv_data:
			if index==0:
				date_arr = str(row[8])
				date_arr = date_arr.split('-')
				date_arr1 = date_arr[0]
				to_date = date_arr1.replace('Viewing=[','').strip()
				date_arr2 = date_arr[1]
				from_date = date_arr2.replace(']','').strip()
				#from_date = parser.parse(from_date).strftime('%Y-%m-%d')
				from_date = datetime.datetime.strptime(from_date, '%d/%m/%y').strftime('%Y-%m-%d')
				to_date = datetime.datetime.strptime(to_date, '%d/%m/%y').strftime('%Y-%m-%d')
				#to_date = parser.parse(to_date).strftime('%Y-%m-%d')
				sql = "SELECT * FROM vendorcentral_crawl WHERE from_date='"+from_date+"'"
				cursor.execute(sql, ())
				result = cursor.fetchall()
				if len(result)>0:
					print('find')
					break
				else:
					print('insert')
					sales_view ='Ordered Revenue'
					update_flag =True
					
			if index > 1:
				asin_name = row[1]
				row[2] = row[2].replace('¥','')
				row[2] = row[2].replace(',','')
				row[6] = row[6].replace(',','')
				if row[2].strip()=='—' or row[2].strip()=='':
					row[2] = '0'
				if row[4].strip()=='—' or row[4].strip()=='':
					row[4] = '0'
				if row[6].strip()=='—' or row[6].strip()=='':
					row[6] = '0'
				if row[5].strip()=='—' or row[5].strip()=='':
					row[5] = '0'
				if row[9].strip=='—' or row[9].strip()=='':
					row[9] = '0'
				if row[10].strip=='—' or row[10].strip()=='':
					row[10] = '0'
				if row[16].strip=='—' or row[16].strip()=='':
					row[16] = '0'
				if row[17].strip=='—' or row[17].strip()=='':
					row[17] = '0'
				if row[18].strip=='—' or row[18].strip()=='':
					row[18] = '0'
				if row[19].strip=='—' or row[19].strip()=='':
					row[19] = '0'
				sql1 = "INSERT INTO `vendorcentral_crawl` (`asin`,`asin_name`,`ordered_revenue`,`ordered_revenu_total`,`ordered_revenu_prior_perod`,`ordered_revenu_last_year`,`ordered_units`,`ordered_units_total`,`ordered_unit_prior_perod`,`ordered_units_prior_last_year`,`subcategory_sales_rank`,`subcategory_better_worse`,`average_sales_price`,`average_sales_price_prior_perod`,`change_in_gv_prior_perod`,`change_in_gv_last_year`,`rep_oss`,`rep_oss_total`,`rep_oss_prior_perod`,`lbb_price`,`from_date`,`to_date`,`sales_view`) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
				try:
					cursor.execute(sql1, (
					row[0],
					asin_name,
					row[2],
					row[3],
					row[4],
					row[5],
					row[6],
					row[7],
					row[8],
					row[9],
					row[10],
					row[11],
					row[12],
					row[13],
					row[14],
					row[15],
					row[16],
					row[17],
					row[18],
					row[19],
					from_date,
					to_date,
					sales_view
					))
				except cursor.Error as e:
					e=str(e)
					print(e)
			index = index+1
		connection.commit()
		crawl_update(update_flag)
except cursor.Error as e:
	print(e)
	#creating error file. it will be replaced with send email function
	# sendmail(e)
	#errorLog.write(e)

finally:
	driver.quit()
	connection.commit()
	connection.close()