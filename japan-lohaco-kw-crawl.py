#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from common_util import *
get_cron_info(61) 
import json
import re
import requests
import time
import datetime
import logging
import pymysql.cursors
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options 

options = Options()
# options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options, executable_path=r'C:\\driver\\chromedriver.exe') 
'''display = Display(visible=0, size=(1000, 1000))
display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)'''

#driver = webdriver.Chrome()  
#driver = webdriver.Firefox() # Optional

#connecion string
connection = get_jp_connection()

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')



vpf_id = '4' 			# lohaco japan
vcrawl_id = '0'			## MASTER
vkeyword = '0'			## MASTER
vkeyword_id = '0'		## MASTER
vbrand_id = '0'			## MASTER
vbrand_name = '0'		## MASTER
vlocation_id = '0'		## MASTER
vlocation_name = '0'	## MASTER
vpincode = '0'			## MASTER
vcreated_by= 'System'	#$ DEFAULT
keywords = []
brands = []
locations = []
index = 0
keyword_count = 0

def crawl_datacapture(keywordArr):
    vkeyword = keywordArr['keyword']		## MASTER
    vkeyword_id = keywordArr['kw_id']		## MASTER
    vbrand_name = keywordArr['brand_name']	## MASTER
    vbrand_id = keywordArr['brand_id']		## MASTER
    vsponsored_brand = '0'
    driver.get("https://lohaco.jp/ksearch/?searchWord="+vkeyword)
    #driver.get("https://lohaco.jp/ksearch/?searchWord=Dr Scholl")
    time.sleep(5)
    soup = None
    try:
        html_container = driver.find_element_by_id("container" ).get_attribute('innerHTML')
        soup = BeautifulSoup(html_container, 'html.parser')
    except NoSuchElementException:
        time.sleep(2)

    scrapedDataList = []
    productSection = None
    productList = []
    sponsored_productList = []
    if soup is not None:
        productSection =  soup.find("ul", {"class" : "lineupItemList"}, recursive=True)
        
    if productSection is not None:
        productList = productSection.findAll("li", recursive=True)
        
    if len(productList)==0:
        print('no products found response')
        #INSERT QUERY FOR NO PRODUCT FOUND
        print('no products found response')
        sql = "INSERT INTO `lohaco_crawl_kw` (`pf_id`,`crawl_id`, `keyword`, `keyword_id`,`brand_id`,`brand_name`, `brand_crawl`,`web_pid`, `pdp_title_value`,`position`, `price_sp`, `pdp_rating_value`, `pdp_rating_count`, `pdp_image_url`,`pdp_page_url`,`pdp_discount_value`, `location_id`,`location_name`,`pincode`,`created_by`,`is_rb`,`url_code_crawl`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s,%s)"
        try:
            cursor.execute(sql, (
            vpf_id
            , vcrawl_id
            , vkeyword
            , vkeyword_id
            , vbrand_id
            , vbrand_name
            , '0'
            , '0'
            , '0'
            , '0'
            , '0'
            , '0'
            , '0'
            , '0'
            , '0'
            , '0'
            , vlocation_id
            , vlocation_name
            , vpincode
            , vcreated_by
            , 0
            , 0
            ))
        except cursor.Error as e:
            e=str(e)
            logging.info('database error:'+e)
            print(e)
            # creating error file. it will be replaced with send email function
            # sendmail(e)
            #errorLog.write(e)
            return '1'
    vposition = '0'
    index = 0
    vpdp_best_seller_tag='0'
    cursor.execute("SELECT brand_name,is_rb, brand_name_th FROM `rb_brands`")
    allBrands= cursor.fetchall()
    for product in productList:
        vpdp_title_value = '0'
        vbrand_crawl = '0'
        vweb_pid = '0'
        vprice_sp = '0'
        vprice_rp = '0'
        vpdp_rating_value = '0'
        vpdp_rating_count = '0'
        vpdp_image_url = '0'
        vpdp_page_url = '0'
        vpdp_discount_value = '0'
        vpdp_sponsored = 0
        vsubscribe_save ='0'
        vsponsored_brand='0'
        is_rb=0
        
        ## START :: TITLE BLOCK  ##
        title = product.find("p", {"class": "itemName"}, recursive=True)
        if title is not None:
            title = title.text
            title = title.strip()
            title = (title[:450] + '..') if len(title) > 450 else title
            vpdp_title_value = title
            index = index+1
        else:
            continue
        if index>20:
            break
        ## END :: TITLE BLOCK  ##	
        
        ## START :: BRAND CRAWL BLOCK  ##
        '''if vpdp_title_value !=  '0':
            titlemaster=[]
            vpdp_title_value=vpdp_title_value
            brand = vpdp_title_value.split(" ")
            for  brand_name  in brand:
                titlemaster.append(brand_name)
     
            cursor.execute("SELECT brand_name,is_rb, brand_name_th FROM `rb_brands`")
            allbrand =[]
            brand_dim=[]
            for brand  in cursor.fetchall():
                brand_dim.append(dict([('brand_name_th',brand['brand_name_th']),('is_rb',brand['is_rb'])]))
            
            for brand in brand_dim:
                allbrand.append(brand['brand_name_th'])
            brandcode_not_found =[]       
            brandcode_not_found= list(set(titlemaster)&set(allbrand))
            if len(brandcode_not_found) >=1:
                for brand_code in brandcode_not_found:
                    vbrand_crawl= brand_code
                    for a in brand_dim:
                        if a['brand_name_th'] == vbrand_crawl:
                            is_rb= a['is_rb']
                        
            else:            
                titlemaster=[]
                vpdp_title_value = vpdp_title_value.replace("-",'')
                vpdp_title_value = vpdp_title_value.replace("Air Wick",'Airwick')
                vpdp_title_value = vpdp_title_value.replace("AIR WICK",'Airwick')
                vpdp_title_value = vpdp_title_value.replace("Kama Sutra",'KamaSutra')
                vpdp_title_value = vpdp_title_value.replace("Man Force",'ManForce')
                brand = vpdp_title_value.split(" ")
                for  brand_name  in brand:
                    titlemaster.append(brand_name.lower())
         
                cursor.execute("SELECT brand_name,is_rb FROM `rb_brands`")
                allbrand =[]
                brand_dim=[]
                for brand  in cursor.fetchall():
                    brand_dim.append(dict([('brand_name',brand['brand_name'].lower()),('is_rb',brand['is_rb'])])) 
                for brand in brand_dim:
                    allbrand.append(brand['brand_name'].lower())
                brandcode_not_found =[]       
                brandcode_not_found= list(set(titlemaster)&set(allbrand))
                if len(brandcode_not_found) >=1:
                    for brand_code in brandcode_not_found:
                        vbrand_crawl= brand_code.capitalize()
                        for a in brand_dim:
                            if a['brand_name'] == vbrand_crawl.lower():
                                is_rb= a['is_rb']
                else:
                    vbrand_crawl ='Others'
                
        else:
            vbrand_crawl='0' '''
        if vpdp_title_value !=  '0':
            for brand  in allBrands:
                if brand['brand_name'] in vpdp_title_value:
                    vbrand_crawl = brand['brand_name']
                    is_rb = brand['is_rb']
                    continue
                    
                if brand['brand_name_th'] in vpdp_title_value:
                    vbrand_crawl = brand['brand_name_th']
                    is_rb = brand['is_rb']
                    continue
        if vbrand_crawl == '0':
            vbrand_crawl = 'Others'
        ## END :: BRAND CRAWL BLOCK  ##
        
        ## START :: POSITION CRAWL BLOCK  ##
        vposition = index
        ## END :: POSITION CRAWL BLOCK  ##
        
        
        ## START :: PIRCE BLOCK  
        pricein = product.find("div", {"class": "cartBtnBlcInner"}, recursive=True)
        if pricein is not None:
            price = pricein.find("p", {"class": "price"}, recursive=True)
            if price is not None:
                price1 = price.find("strong")
                price1 = price1.text
                price1 = price1.strip()
                vprice_sp = price1.replace('￥','')
                vprice_sp = vprice_sp.replace(',','')
            else:
                vprice_sp = '0' 
                      
        else:
            pricein = product.find("div", {"class": "priceBlc"}, recursive=True)
            if pricein is not None:
                price = pricein.find("p", {"class": "price"}, recursive=True)
                if price is not None:
                    price1 = price.find("strong")
                    price1 = price1.text
                    price1 = price1.strip()
                    vprice_sp = price1.replace('￥','')
                    vprice_sp = vprice_sp.replace(',','')
                else:
                    vprice_sp = '0' 
        vprice_rp ='0'
        
        if vprice_sp=='0':
            vprice_sp = vprice_rp
        if vprice_rp == '0':
            vprice_rp = vprice_sp   

        discount = product.find("span", {"class": "offRate"})
        if discount is not None:
            discount = discount.text
            discount = discount.replace('OFF','')
            discount = discount.replace('%','')
            vpdp_discount_value = discount
        else:
            vpdp_discount_value = '0'
        
        ## START :: RATING BLOCK  ##
        rate = product.find("ul", {"class": "reviewStar"}, recursive=True)
        if rate is not None:
            ratings = rate.findAll("li")
            rate=0
            for ratings_data in ratings:
                rating = ratings_data["class"]
                rating = rating[0]
                if rating == 'full':
                    rate =rate +1
                if rating == 'half':
                    rate =rate +0.5
                vpdp_rating_value = rate
        else:
            vpdp_rating_value = '0'
            
        rating_count = product.find("span", {"class": "reviewCount"})
        if rating_count is not None:
            vpdp_rating_count = rating_count.text.strip()
            vpdp_rating_count = vpdp_rating_count.replace('（','')
            vpdp_rating_count = vpdp_rating_count.replace('）','')
        ## END :: RATING BLOCK  ##
            
        ## START :: IMAGE BLOCK  ##
        image = product.find("img", {"class": " lazyloaded"}, recursive=True)
        if image is not None:
            vpdp_image_url = image["src"]
        else:
            imageur = product.find("div", {"class": "prodImgBlc"}, recursive=True)
            if imageur is not None:
                imageur_tag = imageur.find("img")
                if imageur_tag is not None:
                    vpdp_image_url = imageur_tag["src"]
        ## START :: IMAGE BLOCK  ##
        
        ## START :: PAGE URL BLOCK  ##
        linkurl = product.find("p", {"class": "itemName"}, recursive=True)
        if linkurl is not None:
            linkurl_tag = linkurl.find("a")
            if linkurl_tag is not None:
                vpdp_page_url = 'https://lohaco.jp'  + linkurl_tag['href']
            else:
                linkurl_tag1 = product.find("a", {"rel": "nofollow"}, recursive=True)
                if linkurl_tag1 is not None:
                    vpdp_page_url = linkurl_tag1['href']
                else:
                    vpdp_page_url = '0'
        ## START :: PAGE URL BLOCK  ##
        ## START :: WEB PID CRAWL BLOCK  ##
        vurl_code_crawl = '0'
        if vpdp_page_url != '0':
            try:
                vpdp_page_arr = vpdp_page_url.split('/product/')
                if len(vpdp_page_arr) >1:
                    vpdp_page_arr= vpdp_page_arr[1]
                    vpdp_page_arr = vpdp_page_arr.split('/')
                    vpdp_page_arr=vpdp_page_arr[0]
                    vweb_pid = vpdp_page_arr
            except Exception as e:
                vpdp_page_arr = vpdp_page_url.split('pid=')
                if len(vpdp_page_arr) >1:
                    vpdp_page_arr= vpdp_page_arr[1]
                    vpdp_page_arr = vpdp_page_arr.split('&')
                    vpdp_page_arr=vpdp_page_arr[0]
                    vweb_pid = vpdp_page_arr                
        else:
            vweb_pid = '0'
        vurl_code_crawl = vweb_pid
        ## START :: INSERT QUERY BLOCK  ##
        print('pf_id::'+str(vpf_id))
        print('crawl_id::'+str(vcrawl_id))
        print('keyword::'+str(vkeyword).strip()[:65535])
        print('keyword_id::'+str(vkeyword_id))
        print('brand_id::'+str(vbrand_id))
        print('brand_name::'+str(vbrand_name))
        print('brand_crawl::'+str(vbrand_crawl))
        print('web_pid::'+str(vweb_pid))
        print('pdp_title_value::'+str(vpdp_title_value).strip()[:65535])
        print('position::'+str(vposition))
        print('price_sp::'+str(vprice_sp))
        print('pdp_rating_value::'+str(vpdp_rating_value))
        print('pdp_rating_count::'+str(vpdp_rating_count))
        print('pdp_image_url::'+str(vpdp_image_url))
        print('pdp_page_url::'+str(vpdp_page_url))
        print('pdp_discount_value::'+str(vpdp_discount_value))
        print('location_id::'+str(vlocation_id))
        print('location_name::'+str(vlocation_name))
        print('pincode::'+str(vpincode))
        sql = "INSERT INTO `lohaco_crawl_kw` (`pf_id`,`crawl_id`, `keyword`, `keyword_id`,`brand_id`,`brand_name`, `brand_crawl`,`web_pid`, `pdp_title_value`,`position`, `price_sp`, `pdp_rating_value`, `pdp_rating_count`, `pdp_image_url`,`pdp_page_url`,`pdp_discount_value`, `pdp_sponsored`, `sponsored_brand`, `location_id`,`location_name`,`pincode`,`created_by`,`is_rb`,`url_code_crawl` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s,%s)"
        try:
            cursor.execute(sql, (
            vpf_id
            , vcrawl_id
            , vkeyword
            , vkeyword_id
            , vbrand_id
            , vbrand_name
            , vbrand_crawl
            , vweb_pid
            , vpdp_title_value
            , vposition
            , vprice_sp
            , vpdp_rating_value
            , vpdp_rating_count
            , vpdp_image_url
            , vpdp_page_url
            , vpdp_discount_value
            , vpdp_sponsored
            , vsponsored_brand
            , vlocation_id
            , vlocation_name
            , vpincode
            , vcreated_by
            , is_rb
            , vurl_code_crawl
            ))
        except cursor.Error as e:
            e=str(e)
            #logging.info('database error:'+e)
            print(e)
            # creating error file. it will be replaced with send email function
            # sendmail(e)
            #errorLog.write(e)
            return '1'
        ## END :: INSERT QUERY BLOCK  ## 
 
try:
    with connection.cursor() as cursor:

        sql0 = "SELECT l.location_id,l.location,l.pincode FROM `rb_platform` as p, rb_location as l where p.pf_id='"+vpf_id+"' and p.pf_id=l.pf_id"
        cursor.execute(sql0)
        result0 = cursor.fetchall()
        for location in result0:
            locations.append(location)
        if len(locations):
            vlocation_id = locations[0]['location_id']
            vlocation_name = locations[0]['location']
            vpincode = locations[0]['pincode']

        sql1 = "SELECT k.kw_id,k.keyword, b.brand_id,b.brand_name FROM `rb_keyword` AS k, rb_brands AS b WHERE k.brand_id=b.brand_id and k.status='1' AND k.keyword_type='1'"
        cursor.execute(sql1, ())
        result2 = cursor.fetchall()
        for keyword in result2:
            keywords.append(keyword)

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO `rb_crawl` (`pf_id`, `start_time`,`no_of_sku_parsed`, `crawl_type`) VALUES (%s, %s, %s, %s)"
        try:
            #print('testing')
            cursor.execute(sql, (vpf_id,timestamp,'0','2'))
            vcrawl_id = connection.insert_id()
            connection.commit()
        except cursor.Error as e:
            e=str(e)
            print(e)
            #logging.info('database error:'+e)
            # creating error file. it will be replaced with send email function
            #errorLog.write(e)
        for keywordArr in keywords:
            val = crawl_datacapture(keywordArr)
            while val=='2':
                val = crawl_datacapture(keywordArr)
            keyword_count = keyword_count+1

        keyword_count = str(keyword_count)

        vcrawl_id = str(vcrawl_id)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        try:
            print('completed')
            cursor.execute("UPDATE rb_crawl SET status=1, end_time = '"+timestamp+"',no_of_sku_parsed='"+keyword_count+"' WHERE crawl_id='"+vcrawl_id+"'")
        except cursor.Error as e:
            e=str(e)
            #logging.info('database error:'+e)
            print(e)
            # creating error file. it will be replaced with send email function
            # sendmail(e)
            #errorLog.write(e)
        try:
            print('completed')
            cursor.execute("UPDATE rb_platform SET  kw_crawl_data_date = '"+timestamp+"', kw_crawl_data_id='"+vcrawl_id+"' WHERE pf_id='"+vpf_id+"'")
        except cursor.Error as e:
            e=str(e)
            #logging.info('database error:'+e)
            print(e)
        try:
            kpi_id = '61'
            kpi_name = 'JP_Lohaco_kw'
            run_status = 'success'
            update_cron_status(kpi_id,kpi_name,run_status);
        except Exception as e:
            e=str(e)
            # creating error file. it will be replaced with send email function
        try:
            u_sql = "UPDATE lohaco_crawl_kw SET brand_crawl = 'Dr Scholl'  , is_rb ='1'  WHERE pdp_title_value LIKE '%Dr.Scholl%'"
            cursor.execute(u_sql)
        except cursor.Error as e:
            e=str(e)
            print(e)


except cursor.Error as e:
	e=str(e)
	#logging.info('database error:'+e)
	print(e)
	#creating error file. it will be replaced with send email function
	# sendmail(e)
	#errorLog.write(e)
finally:
	driver.quit()
	connection.commit()
	connection.close()
