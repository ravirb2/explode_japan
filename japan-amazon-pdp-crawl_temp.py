#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from common_util import * 
import json
import re
import requests
import time
import datetime
import logging
from dateutil import parser
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from pyvirtualdisplay import Display
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
driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\\driver\\chromedriver.exe') 

#driver = webdriver.Firefox()
# #driver = webdriver.Chrome()

#connecion string
connection = get_jp_connection()
#connecion string

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#logging.basicConfig(filename='log/amazon-pdp-crawl'+date+'.log',level=logging.DEBUG)
#logging.info('Crawling starts at:'+timestamp)
#logging.debug('This message should go to the log file')
#logging.warning('And this, too')
#errorLog = open('amazon-pdp-error_log.txt', 'w')


amazon_sku = []
locations = []
sleeptime = 2
vpf_id = '1'				#$ DEFAULT
vcrawl_id = '0'				## MASTER
vlocation_id = '0'			## MASTER
vlocation_name = '0'		## MASTER
vcreated_by= 'System'	    #$ DEFAULT
review_flag= True

def crawl_datacapture(sku):

    vpdp_oos_message = ''
    vpdp_delivery_time = '0'
    vpdp_delivery_message = '0'
    vsku_id = '0'		# from MASTER
    vweb_pid = sku['web_pid'] 		# from MASTER
    vbrand_id = '0'		# from MASTER
    vbrand_name = '0'	# from MASTER
    vsku_name = '0'		# from MASTER
    vgroup_id = '0'		# from MASTER
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
    vpdp_page_url = '0'			#** CRAWL **
    html_container = None 
    vec_number_of_image= '0'                    #** CRAWL **
    vpdp_bullet_count_no= '0'                   #** CRAWL **
    vpdp_bullet_value= '0'                      #** CRAWL **
    vreseller_name_crawl='0'                    #** CRAWL **
    lad_date = 'NA'                             #** CRAWL **
    vpdp_page_url = 'https://www.amazon.co.jp/dp/'+str(vweb_pid)
    driver.get(vpdp_page_url)
    time.sleep(5)
    try:
        goto  = driver.find_element_by_id("purchase-sims-feature" )
        driver.execute_script("return arguments[0].scrollIntoView();", goto)
        time.sleep(2)
    except NoSuchElementException:
        time.sleep(1)
        
    try:
        html_container = driver.find_element_by_id("dp" ).get_attribute('innerHTML')
    except NoSuchElementException:
        time.sleep(1)
    driver.switch_to_default_content()
    vweb_pid = vweb_pid.encode('utf-8').strip()[:65535]
    vgroup_id = vgroup_id.encode('utf-8').strip()[:65535]

    if html_container is not None:
        soup = BeautifulSoup(html_container, 'html.parser')
        if soup is not None:
            try:
                no_result = soup.find("h1", {"id" : "noResultsTitle"}, recursive=True)
            except NoSuchElementException:
                time.sleep(1)
            if no_result is not None:
                print('not found')
                return 1
            else:
                try:
                    html_container = driver.find_element_by_id("dp-container" ).get_attribute('innerHTML');
                except NoSuchElementException:
                    time.sleep(1)
                pdp_soup = BeautifulSoup(html_container, 'html.parser')
                
                ## START :: OSA BLOCK  ##
                try:	
                    inStockDiv = pdp_soup.find("div", {"id": "availability"}, recursive=True)
                except NoSuchElementException:
                    time.sleep(1)
                # 	vosa_remark = '0'

                inStockSpan = pdp_soup.find("input", {"id": "add-to-cart-button"}, recursive=True)
                if inStockSpan is not None:
                    vosa = '1'
                    vosa_remark = '1'
                else:
                    vosa = '0'
                    vosa_remark = '0'
                
                
                ## END :: OSA BLOCK  ##
                
                ## START :: PRICE BLOCK  ##
                
                price_span_ourprice = pdp_soup.find("span", {"id": {"priceblock_ourprice"}}, recursive=True)
                if price_span_ourprice is not None:
                    vprice_sp = price_span_ourprice.text
                    vprice_sp = vprice_sp.replace(',','')
                    vprice_sp = vprice_sp.replace('￥','')
                    vprice_sp = float(vprice_sp)
                    vprice_rp = float(vprice_sp)

                deal_price = pdp_soup.find("span", {"id": {"priceblock_dealprice"}}, recursive=True)
                if deal_price is not None:
                    deal_price = deal_price.text
                    vprice_sp = deal_price.replace(',','')
                    vprice_sp = vprice_sp.replace('￥','')
                    if vprice_rp =='0':
                        vprice_rp = float(vprice_sp)

                deal_price = pdp_soup.find("span", {"id": {"priceblock_saleprice"}}, recursive=True)
                if deal_price is not None:
                    deal_price = deal_price.text
                    vprice_sp = deal_price.replace(',','')
                    vprice_sp = vprice_sp.replace('￥','')
                    if vprice_rp =='0':
                        vprice_rp = float(vprice_sp)					
                        
                price_span_strike = pdp_soup.find("span", {"class": {"a-text-strike"}}, recursive=True)
                if price_span_strike is not None:
                    price_span_strike = price_span_strike.text
                    vprice_rp = price_span_strike.replace(',','')
                    vprice_rp = vprice_rp.replace('￥','')
                    vprice_rp = float(vprice_rp)					

                discount = pdp_soup.find("td", {"class": "a-span12 a-color-price a-size-base"})
                if discount is not None:
                    discount = discount.text
                    discountarr = discount.split('(')
                    if len(discountarr) > 1:
                        discountarr1 = discountarr[1].split('%')
                        vpdp_discount_value = discountarr1[0];
                    else:
                        vpdp_discount_value = '0'
                                #print(vpdp_discount_value)
                else:
                    vpdp_discount_value = '0'
                    
                #print(vpdp_discount_value)
                if vprice_sp=='0':
                    deal_price = pdp_soup.find("div", {"id": "olp_feature_div"}, recursive=True)
                    if deal_price is not None and vosa_remark=='1':
                        deal_price_span = deal_price.find("span", {"class": "a-color-price"}, recursive=True)
                        if deal_price_span is not None:
                            deal_price_arr = deal_price_span.text.split(' ')
                            if len(deal_price_arr)>0:
                                vprice_sp = deal_price_arr[len(deal_price_arr)-1].replace(',','')
                                if vprice_rp =='0':
                                    vprice_rp = float(vprice_sp)
                ## END :: PRICE BLOCK  ##
                
                ## START :: PDP - TITLE BLOCK  ##
                
                title = pdp_soup.find("span", {"id": "productTitle"}, recursive=True)
                if title is not None:
                    vpdp_title_value = title.text.strip()
                    vpdp_title_value  = vpdp_title_value.encode('utf-8').strip()[:65535]
                else:				
                    robot = pdp_soup.find("title", recursive=True)
                    if robot is not None:
                        robot = robot.text.strip()
                        if robot == 'Robot Check':
                            vosa_remark = '0' 
                            vosa = '0' 
                            print(robot)						
                        else:
                            vosa_remark = '2' 
                            vosa = '0' 
                            print('not robot')
                    else:
                        vosa_remark = '2'
                        vosa = '0' 					
                        print('not robot')					

                ## END :: PDP - TITLE BLOCK  ##
                
                ## START :: PDP - DESCRIPTION BLOCK  ##			
                
                detailv = pdp_soup.find("div", {"id": "productDescription"}, recursive=True)
                if detailv is not None:
                    #detail = detailv.find("p", recursive=True)
                    #if detail is not None:
                    vpdp_desc_value = detailv.text.strip()
                    vpdp_desc_value  = vpdp_desc_value.encode('utf-8').strip()[:65535]
                    #vpdp_desc_value = re.sub('[^a-zA-Z0-9\n\.]', ' ', vpdp_desc_value)
                
                
                ## END :: PDP - DESCRIPTION BLOCK  ##	

                ## START :: PDP - IMAGE BLOCK  ##
                no_of_images = pdp_soup.find("div", {"id": "altImages"}, recursive=True)
                if no_of_images is not None:
                    #print(no_of_images.text)
                    no_of_images = no_of_images.findAll("img")
                    vpdp_image_count = len(no_of_images)
                else:
                    vpdp_image_count = '0'
                
                
                imageDiv = pdp_soup.find("div", {"id": "imgTagWrapperId"}, recursive=True)
                if imageDiv is not None:
                    image = imageDiv.find("img", {"class": "a-dynamic-image"}, recursive=True)
                    if image is not None:
                        vpdp_image_url = image["src"]
                        if len(vpdp_image_url) > 200:
                            vpdp_image_url = image["data-old-hires"]
                    else:
                        vpdp_image_url = ''
                else:
                    vpdp_image_url = ''
                vpdp_image_url = (vpdp_image_url[:250] + '..') if len(vpdp_image_url) > 250 else vpdp_image_url
                ## END :: PDP - IMAGE BLOCK  ##
                
                ## START :: PDP - REVIEW COUNT BLOCK  ##
                revcount = pdp_soup.find("span", {"id": "acrCustomerReviewText"})
                if revcount is not None:
                    revcountArr = revcount.text.split(' ')
                    vpdp_review_count = revcountArr[0].replace(',','')
                    vpdp_review_count = vpdp_review_count.replace('件のカスタマーレビュー','')
                    vpdp_rating_count = vpdp_review_count.replace(',','')
                    vpdp_rating_count = vpdp_review_count.replace('件のカスタマーレビュー','')
                else:
                    vpdp_review_count = '0'
                    vpdp_rating_count = '0'

                ## END :: PDP - REVIEW COUNT BLOCK  ##
                    
                ## START :: PDP - RATING VALUE BLOCK  ##
                not_rated = pdp_soup.find("span", {"id": "acrCustomerWriteReviewText"}, recursive=True)
                if not_rated is not None:
                    vpdp_rating_value = '0'
                else:
                    rate = pdp_soup.find("i", {"class": "a-icon-star"}, recursive=True)
                    if rate is not None:
                        ratings = rate.find("span", {"class": "a-icon-alt"}, recursive=True)
                        if ratings is not None:
                            rating = ratings.text
                            vpdp_rating_value = rating[0:-15]
                        else:
                            vpdp_rating_value = '0'
                    else:
                        vpdp_rating_value = '0'
                ## END :: PDP - RATING VALUE BLOCK  ##

                ##START:: ec_number_of_image ##
                         
                no_of_images = pdp_soup.find("div", {"class": "aplus-v2 desktop celwidget"}, recursive=True)
                if no_of_images is not None:
                        #print(no_of_images.text)
                        images_count = no_of_images.findAll("img")
                        if len(images_count) != 0:
                                vec_number_of_image=len(images_count)
                        else:
                              vec_number_of_image='0'  
                        
                ##end:: ec_number_of_image ##
                try:
                    av= pdp_soup.find('div', {'id':'availability'}, recursive=True)
                    if av is not None:
                        vpdp_oos_message= av.text.encode('utf-8').strip()
                except Exception as e:
                    print str(e)
                    
                ##START:: pdp_number_of_bulletin ##
                try:
                        bullet_count=driver.find_elements_by_css_selector("#feature-bullets > ul > li")
                        if bullet_count is not None:
                                for indx, bullet in enumerate(bullet_count,1):
                                        bullet= bullet.get_attribute('innerHTML')
                                        #print product_image
                                        vpdp_bullet_count_no=indx
                                
                except NoSuchElementException:
                        vpdp_bullet_count_no='0'
                        
                ## END :: pdp_number_of_bulletin  ##


                ##START:: pdp_bulletin_value ##
                try:
                        bullet_value=driver.find_element_by_css_selector("#feature-bullets > ul")
                        if bullet_value is not None:
                                vpdp_bullet_value= bullet_value.text
                                #print vpdp_bullet_value
                        
                except NoSuchElementException:
                        vpdp_bullet_value='0'
                        
                ## END :: pdp_bulletin_value  ##
                try:
                    vreseller_name_crawl=driver.find_element_by_id("merchant-info")
                    
                    if vreseller_name_crawl is not None:
                        vreseller_name_crawl1= vreseller_name_crawl.text
                        if len(vreseller_name_crawl1) > 1:
                            vreseller_name_crawl=vreseller_name_crawl1.split("by ")
                            vreseller_name_crawl = vreseller_name_crawl[1].split(" (")
                            vreseller_name_crawl = vreseller_name_crawl[0].replace(".","")
                        else:
                            vreseller_name_crawl = '0';
                except Exception as e:
                    vreseller_name_crawl='0'
               ## END :: vreseller_name_crawl BLOCK  ## 
        

                ## START :: PDP - Q & A BLOCK  ##
                answered_questions1 = pdp_soup.find("a", {"id": "askATFLink"})
                if answered_questions1 is not None:
                    answered_questions1 = answered_questions1.find("span", {"class": "a-size-base"})
                    answered_questions1 = answered_questions1.text.strip()
                    answered_questionsArr = answered_questions1.split(' ')
                    vpdp_qa_count = answered_questionsArr[0]
                else:
                    vpdp_qa_count = '0'
                
                vbrand_name1 = pdp_soup.find("a", {"id": "bylineInfo"}, recursive=True)
                if vbrand_name1 is not None:
                    #print(no_of_images.text)
                    vbrand_name = vbrand_name1.text.strip()
                else:
                    vbrand_name = '0'
                ## END :: PDP - Q & A BLOCK  ##	
         
            if vpdp_title_value=='' or vpdp_title_value=='0':
                vpdp_title_value = vsku_name
        else:
            vosa_remark='2'
    else:
        vosa_remark='2'

    if vprice_sp=='0' and vosa_remark=='1':
        vosa = '0'
        vosa_remark = '0'
    if vosa == '0':
        sql_lad = "SELECT date(created_on) as lad FROM `rb_pdp`  WHERE pf_id='"+vpf_id+"' and osa = 1 and  web_pid ='"+vweb_pid+"' and status=1  order by date(created_on) desc limit 1"
        cursor.execute(sql_lad, ())
        result15 = cursor.fetchall()
        for dt in result15:
            lad_date = dt['lad']
    elif vosa == '1':
        lad_date = date
    print('pf_id::  '  + str(vpf_id))
    print('crawl_id::  '  + str(vcrawl_id))
    print('sku_id::  '  + str(vsku_id))
    print('web_pid::  '  + str(vweb_pid))
    print('pdp_title_value::  '  + str(vpdp_title_value).encode('utf-8').strip()[:65535])
    ## START :: INSERT QUERY BLOCK  ##
    sql1 = """INSERT INTO `amazon_crawl_pdp_temp` (`pf_id`,`crawl_id`, `sku_id`,`web_pid`, `pdp_title_value`, `brand_id`,`brand_name`,
           `price_rp`,`price_sp`, `pdp_rating_value`, `pdp_review_count`,`pdp_rating_count`,`pdp_qa_count`,
           `pdp_desc_value`, `pdp_image_count`,`pdp_image_url`, `osa`,`osa_remark`,`pdp_page_url`,`pdp_discount_value`,
           `location_id`,`location_name`,`group_id`,`created_by`,`ec_number_of_images`,`pdp_number_of_bulletin`,
           `pdp_bulletin_value`,`reseller_name_crawl`,`lad`) VALUES (%s,%s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s,
           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    try:
        cursor.execute(sql1, (
        vpf_id,
        vcrawl_id,
        vsku_id,
        vweb_pid,
        vpdp_title_value.encode('utf-8').strip()[:65535],
        vbrand_id,
        vbrand_name.encode('utf-8').strip()[:65535],
        vprice_rp,
        vprice_sp,
        vpdp_rating_value,
        vpdp_review_count,
        vpdp_rating_count,
        vpdp_qa_count,
        vpdp_desc_value.encode('utf-8').strip()[:65535],
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
        lad_date
        ))
        connection.commit()
    except cursor.Error as e:
        e=str(e)
        print(e)
        #errorLog.write(e)

    ## END :: INSERT QUERY BLOCK  ##

def set_location(zip_code):
    try:
        zipcode=zip_code.split("-")
        zipcode1= zipcode[0]
        zipcode2= zipcode[1]
        driver.get('https://www.amazon.co.jp/')
        time.sleep(5)
        driver.find_element_by_xpath("//*[@id='glow-ingress-line2']").click()
        time.sleep(2) # Let the user actually see something!       
        driver.find_element_by_xpath("//*[@id='GLUXZipUpdateInput_0']").send_keys(zipcode1); 
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='GLUXZipUpdateInput_1']").send_keys(zipcode2); 
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='GLUXZipUpdate']/span").click();
        #driver.find_element_by_xpath("//*[@id='GLUXZipUpdate']/span/input").click()
        time.sleep(2) # Let the user actually see something!
        driver.find_element_by_xpath("//*[@id='a-popover-4']/div/div[3]/span/span").click()
        time.sleep(2)
    except:
        print('no element')	
				
try:
    with connection.cursor() as cursor:
        vpf_id = str(vpf_id)
        try:
            sql0 = "SELECT l.location_id,l.location,l.pincode FROM `rb_platform` as p, rb_location as l where p.pf_id='"+vpf_id+"' and p.pf_id=l.pf_id and l.status=1"
            cursor.execute(sql0)
            result0 = cursor.fetchall()
            for location in result0:
                locations.append(location)

        except cursor.Error as e:
            e=str(e)
            print(e)
            
        sql1 = "SELECT * FROM amazon_temp_master"
        cursor.execute(sql1, ())
        result1 = cursor.fetchall()
        for skus in result1:
            amazon_sku.append(skus)
            
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO `rb_crawl` (`pf_id`, `start_time`,`no_of_sku_parsed`, `crawl_type`) VALUES (%s, %s, %s, %s)"
        try:
            print('testing')
            #cursor.execute(sql, (vpf_id,timestamp,'0','1'))
            #vcrawl_id = connection.insert_id()
            #connection.commit()
        except cursor.Error as e:
            e=str(e)
            print(e)

        vcrawl_id =112
        product_count = 0
        for locationArr in locations:
            zip_code = locationArr['pincode']
            set_location(zip_code) 
            vlocation_id = locationArr['location_id']
            vlocation_name = locationArr['location']
            vpincode = locationArr['pincode']
            for skuArr in amazon_sku:
                    crawl_datacapture(skuArr)
                    product_count = product_count+1
        vcrawl_id = str(vcrawl_id)
        product_count = str(product_count)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        try:
            print('completed')
            #cursor.execute("UPDATE rb_crawl SET status=1, end_time = '"+timestamp+"',no_of_sku_parsed='"+product_count+"' WHERE crawl_id='"+vcrawl_id+"'")
        except cursor.Error as e:
            e=str(e)
            #logging.info('database error:'+e)
            print(e)
            #errorLog.write(e)
        try:
            print('completed')
            #cursor.execute("UPDATE rb_platform SET  pdp_crawl_data_date = '"+timestamp+"', pdp_crawl_data_id='"+vcrawl_id+"' WHERE pf_id='"+vpf_id+"'")
        except cursor.Error as e:
            e=str(e)
            #logging.info('database error:'+e)
            print(e)
            #errorLog.write(e)
        try:
            print('status updated')
            #cursor.execute("UPDATE amazon_crawl_pdp SET  status = '1' WHERE crawl_id='"+vcrawl_id+"'")
        except cursor.Error as e:
            e=str(e)
            print(e)
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
	connection.commit()
	connection.close()

