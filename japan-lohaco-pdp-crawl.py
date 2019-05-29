#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from common_util import *
get_cron_info(57); 
#import json
import re
import requests
import time
#import datetime
#import logging
from dateutil import parser
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from datetime import datetime, timedelta
#from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options 

options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options, executable_path=r'C:\\driver\\chromedriver.exe') 


#connecion string
connection = get_jp_connection()
#connecion string

from pytz import timezone
japan_time = timezone('Japan')
sa_time = datetime.now(japan_time)
timestamp = sa_time.strftime('%Y-%m-%d %H:%M:%S')


amazon_sku = []
locations = []
sleeptime = 2
vpf_id = '4'				#$ DEFAULT
vcrawl_id = '0'				## MASTER
vlocation_id = '0'			## MASTER
vlocation_name = '0'		## MASTER
vcreated_by= 'System'	    #$ DEFAULT
review_flag= True

def crawl_datacapture(sku):
    vsku_id = sku['sku_id']			# from MASTER
    vweb_pid = sku['web_pid'] 		# from MASTER
    vbrand_id = sku['brand_id']		# from MASTER
    vbrand_name = sku['brand_name']	# from MASTER
    vsku_name = sku['sku_name']		# from MASTER
    vgroup_id = sku['group_id']		# from MASTER
    vpdp_page_url = sku['url']  # from MASTER
    vosa = '0'					#** CRAWL **
    vosa_remark = '0'			#** CRAWL **
    vprice_rp = '0'				#** CRAWL **
    vprice_sp = '0'				#** CRAWL **
    vpdp_discount_value = '0'	#** CRAWL **
    vpdp_title_value = '0' 		#** CRAWL **
    vpdp_desc_value = '0'		#** CRAWL **
    vpdp_image_count = '0'		#** CRAWL **
    vpdp_image_url= '0'			#** CRAWL **
    vpdp_rating_value = '0'		#** CRAWL **
    vpdp_rating_count = '0'		#** CRAWL **
    vpdp_review_count = '0'		#** CRAWL **
    vpdp_qa_count = '0'			#** CRAWL **
    html_container = None 
    vec_number_of_image= '0'                    #** CRAWL **
    vpdp_bullet_count_no= '0'                   #** CRAWL **
    vpdp_bullet_value= '0'                      #** CRAWL **
    vreseller_name_crawl='0'                    #** CRAWL **
    lad_date = 'NA'                             #** CRAWL **
    pdp_soup = None
    #vpdp_page_url = 'https://lohaco.jp/product/8368206'
    driver.get(vpdp_page_url)
    time.sleep(5)        
    try:
        html_container = driver.find_element_by_id("container").get_attribute('innerHTML')
    except NoSuchElementException:
        time.sleep(1)
        
    if html_container is not None:
        pdp_soup = BeautifulSoup(html_container, 'html.parser')
        
    if pdp_soup is not None:

        ## STRAT :: OSA BLOCK  ##
        inStockSpan = pdp_soup.find("p", {"class": "btn-basket basketBtn"}, recursive=True)
        if inStockSpan is not None:
            vosa = '1'
            vosa_remark = '1'
        else:
            vosa = '0'
            vosa_remark = '0'           
        ## END :: OSA BLOCK  ##
            
        ## START :: PRICE BLOCK  ##
        pricein = pdp_soup.find("p", {"class": "elmPriceDetail stronger"}, recursive=True)
        if pricein is not None:
            price = pricein.find("span", {"class": "elmBigger"}, recursive=True)
            if price is not None:
                price1 = price.text
                price1 = price1.strip()
                vprice_sp = price1.replace('￥','')
                vprice_sp = vprice_sp.replace(',','')
            else:
                vprice_sp = '0' 
                      
        else:
            vprice_sp = '0'
            
        priceout = pdp_soup.find("p", {"class": "elmDefaultPrice"}, recursive=True)
        if priceout is not None:
            price1 = priceout.find("span", {"class": "elmPrice textStrike"}, recursive=True)
            if price1 is not None:
                price1 = price1.text
                vprice_rp = price1.replace('（税込）','')
                vprice_rp = vprice_rp.replace('￥','')
                vprice_rp = vprice_rp.replace(',','')
                vprice_rp = vprice_rp.strip()
            else:
                vprice_rp = '0' 
                      
        else:
            vprice_rp = '0' 
        if vprice_sp=='0':
            vprice_sp = vprice_rp
        if vprice_rp == '0':
            vprice_rp = vprice_sp   

        discount = pdp_soup.find("span", {"class": "elmOffRateIcon"})
        if discount is not None:
            discount1 = discount.find("span", {"class": "icon"})
            if discount1 is not None:
                discount = discount1.text
                discount = discount.replace('OFF','')
                discount = discount.replace('%','')
                vpdp_discount_value = discount
        else:
            discount = float(vprice_rp) - float(vprice_sp)
            if discount >0:
                vpdp_discount_value = round((float(discount)/float(vprice_rp))*100,2)
            else:
                vpdp_discount_value = '0'
        ## END :: PRICE BLOCK  ##
            
        ## START :: PDP - TITLE BLOCK  ##
            
        title = pdp_soup.find("h1", {"class": "elmTitle"}, recursive=True)
        if title is not None:
            vpdp_title_value = title.text.strip()
            vpdp_title_value  = vpdp_title_value.strip()[:65535]
        else:
            vpdp_title_value ='0'
        ## END :: PDP - TITLE BLOCK  ##
        
        ## START :: PDP - DESCRIPTION BLOCK  ##			        
        detailv = pdp_soup.find("div", {"class": "blcProdSpec sectionWrapper"}, recursive=True)
        if detailv is not None:
            vpdp_desc_value = detailv.text.strip()
            vpdp_desc_value  = vpdp_desc_value.strip()[:65535]      
        ## END :: PDP - DESCRIPTION BLOCK  ##	

        ## START :: PDP - IMAGE BLOCK  ##
        no_of_images = pdp_soup.find("ul", {"id": "mainThumbsList"}, recursive=True)
        if no_of_images is not None:
            no_of_images = no_of_images.findAll("img")
            vpdp_image_count = len(no_of_images)
        else:
            vpdp_image_count = '0'
        
        
        imageDiv = pdp_soup.find("p", {"id": "elmModalMainImg"}, recursive=True)
        if imageDiv is not None:
            image = imageDiv.find("img", {"class": "active"}, recursive=True)
            if image is not None:
                vpdp_image_url = image["src"]
            else:
                vpdp_image_url = '0'
        else:
            vpdp_image_url = '0'
        ## END :: PDP - IMAGE BLOCK  ##
        
        ## START :: PDP - REVIEW COUNT BLOCK  ##
        revcount = pdp_soup.find("p", {"class": "elmReviewRate"})
        if revcount is not None:
            revcountArr = revcount.text.split('（')
            vpdp_review_count = revcountArr[1]
            vpdp_review_count = vpdp_review_count.replace('件のレビュー）','')
            vpdp_review_count = vpdp_review_count.replace(',','')
            vpdp_review_count =vpdp_review_count.strip()
            vpdp_rating_count =vpdp_review_count
        else:
            vpdp_review_count = '0'
            vpdp_rating_count = '0'

        ## END :: PDP - REVIEW COUNT BLOCK  ##
            
        ## START :: PDP - RATING VALUE BLOCK  ##
        not_rated = pdp_soup.find("p", {"class": "elmReviewRate"})
        if not_rated is not None:
            revcountArr = not_rated.text.split('（')
            vpdp_rating_value = revcountArr[0]
            vpdp_rating_value = vpdp_rating_value.strip()
       
        else:
            vpdp_rating_value = '0'
        ## END :: PDP - RATING VALUE BLOCK  ##

        ##START:: ec_number_of_image ##
                 
        no_of_images = pdp_soup.find("div", {"class": "externalFileArea"}, recursive=True)
        if no_of_images is not None:
            images_count = no_of_images.findAll("img")
            if len(images_count) != 0:
                vec_number_of_image=len(images_count)
            else:
                vec_number_of_image='0'                  
        ##end:: ec_number_of_image ##
            
        ##START:: pdp_number_of_bulletin ## 
        vpdp_bullet_count_no='0'               
        ## END :: pdp_number_of_bulletin  ##


        ##START:: pdp_bulletin_value ##
        vpdp_bullet_value='0'
                
        ## END :: pdp_bulletin_value  ##
        vreseller_div =pdp_soup.find("span", {"class": "blcStoreName"}, recursive=True)
        if vreseller_div is not None:
            vreseller_name_crawl= vreseller_div.text.strip()
        else:
            vreseller_name_crawl = '0'
       ## END :: vreseller_name_crawl BLOCK  ##  
    if vpdp_title_value == '0':
        vosa_remark = '2' 
        vosa = '0'
        
    print('pf_id::  '  + str(vpf_id))
    print('crawl_id::  '  + str(vcrawl_id))
    print('sku_id::  '  + str(vsku_id))
    print('web_pid::  '  + str(vweb_pid))
    print('pdp_title_value::  '  + str(vpdp_title_value).strip()[:65535])
    print('brand_id::  '  + str(vbrand_id))
    print('brand_name::  '  + str(vbrand_name))
    print('price_rp::  '  + str(vprice_rp))
    print('price_sp::  '  + str(vprice_sp))
    print('pdp_rating_value::  '  + str(vpdp_rating_value))
    print('pdp_review_count::  '  + str(vpdp_review_count))
    print('pdp_rating_count::  '  + str(vpdp_rating_count))
    print('pdp_qa_count::  '  + str(vpdp_qa_count))
    #print('pdp_desc_value::  '  + str(vpdp_desc_value).encode('utf-8').strip()[:65535])
    print('pdp_image_count::  '  + str(vpdp_image_count))
    print('pdp_image_url::  '  + str(vpdp_image_url).strip()[:65535])
    print('osa::  '  + str(vosa))
    print('osa_remark::  '  + str(vosa_remark))
    print('pdp_page_url::  '  + str(vpdp_page_url))
    print('pdp_discount_value::  '  + str(vpdp_discount_value))
    print('location_id::  '  + str(vlocation_id))
    print('location_name::  '  + str(vlocation_name))
    print('group_id::  '  + str(vgroup_id))
    print('created_by::  '  + str(vcreated_by))
    print ('ec_number_of_images:: '+str(vec_number_of_image))
    print ('pdp_number_of_bulletin::'+str(vpdp_bullet_count_no))
    print ('pdp_bulletin_value::'+str(vpdp_bullet_value))
    print ('reseller_name_crawl::' +str(vreseller_name_crawl).strip()[:65535])
    ## START :: INSERT QUERY BLOCK  ##
    sql1 = """INSERT INTO `lohaco_crawl_pdp` (`pf_id`,`crawl_id`, `sku_id`,`web_pid`, `pdp_title_value`, `brand_id`,`brand_name`,
           `price_rp`,`price_sp`, `pdp_rating_value`, `pdp_review_count`,`pdp_rating_count`,`pdp_qa_count`,
           `pdp_desc_value`, `pdp_image_count`,`pdp_image_url`, `osa`,`osa_remark`,`pdp_page_url`,`pdp_discount_value`,
           `location_id`,`location_name`,`group_id`,`created_by`,`ec_number_of_images`,`pdp_number_of_bulletin`,
           `pdp_bulletin_value`,`reseller_name_crawl`,`lad`,`created_on`) VALUES (%s,%s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s,
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"""
    try:
        cursor.execute(sql1, (
        vpf_id,
        vcrawl_id,
        vsku_id,
        vweb_pid,
        vpdp_title_value.strip()[:65535],
        vbrand_id,
        vbrand_name.strip()[:65535],
        vprice_rp,
        vprice_sp,
        vpdp_rating_value,
        vpdp_review_count,
        vpdp_rating_count,
        vpdp_qa_count,
        vpdp_desc_value.strip()[:65535],
        vpdp_image_count,
        vpdp_image_url,
        vosa,
        vosa_remark,
        vpdp_page_url,
        vpdp_discount_value,
        vlocation_id,
        vlocation_name,
        vgroup_id,
        vcreated_by,
        vec_number_of_image,
        vpdp_bullet_count_no,
        vpdp_bullet_value,
        vreseller_name_crawl,
        lad_date,
		timestamp
        ))
        connection.commit()
    except cursor.Error as e:
        e=str(e)
        print(e)
        #errorLog.write(e)

    ## END :: INSERT QUERY BLOCK  ##	



    
try:
    with connection.cursor() as cursor:
        vpf_id = str(vpf_id)
        sql0 = "SELECT l.location_id,l.location,l.pincode FROM `rb_platform` as p, rb_location as l where p.pf_id='"+vpf_id+"' and p.pf_id=l.pf_id"
        cursor.execute(sql0)
        result0 = cursor.fetchall()
        for location in result0:
        	locations.append(location)
        if len(locations):
        	vlocation_id = locations[0]['location_id']
        	vlocation_name = locations[0]['location']
        	vpincode = locations[0]['pincode']
        	
        sql1 = "SELECT * FROM `rb_sku_platform` as sp, `rb_brands` as b WHERE sp.pf_id='"+vpf_id+"' and sp.brand_id=b.brand_id  AND sp.web_pid !='' and sp.status=1"
        cursor.execute(sql1, ())
        result1 = cursor.fetchall()
        for skus in result1:
        	amazon_sku.append(skus)

        sql = "INSERT INTO `rb_crawl` (`pf_id`, `start_time`,`no_of_sku_parsed`, `crawl_type`) VALUES (%s, %s, %s, %s)"
        try:
        	#print('testing')
        	cursor.execute(sql, (vpf_id,timestamp,'0','1'))
        	vcrawl_id = connection.insert_id()
        	connection.commit()
        except cursor.Error as e:
        	e=str(e)
        	print(e)

        #vcrawl_id =0
        product_count = 0
        for skuArr in amazon_sku:
        		crawl_datacapture(skuArr)
        		product_count = product_count+1
        vcrawl_id = str(vcrawl_id)
        product_count = str(product_count)
        sa_time = datetime.now(japan_time)
        timestamp = sa_time.strftime('%Y-%m-%d %H:%M:%S')
        try:
        	print('completed')
        	cursor.execute("UPDATE rb_crawl SET status=1, end_time = '"+timestamp+"',no_of_sku_parsed='"+product_count+"' WHERE crawl_id='"+vcrawl_id+"'")
        	connection.commit()
        except cursor.Error as e:
        	e=str(e)
        	#logging.info('database error:'+e)
        	print(e)
        	#errorLog.write(e)
        try:
        	print('completed')
        	cursor.execute("UPDATE rb_platform SET  pdp_crawl_data_date = '"+timestamp+"', pdp_crawl_data_id='"+vcrawl_id+"' WHERE pf_id='"+vpf_id+"'")
        	connection.commit()
        except cursor.Error as e:
        	e=str(e)
        	#logging.info('database error:'+e)
        	print(e)
        try:
            kpi_id = '57'
            kpi_name = 'JP_Lohaco_pdp'
            run_status = 'success'
            update_cron_status(kpi_id,kpi_name,run_status);
        except Exception as e:
            e=str(e)
        	#errorLog.write(e)
except cursor.Error as e:
	e=str(e)
	#logging.info('database error:'+e)
	print(e)
	#creating error file. it will be replaced with send email function
	# sendmail(e)
	#errorLog.write(e)
finally:
	driver.quit()
	#connection.commit()
	connection.close()

