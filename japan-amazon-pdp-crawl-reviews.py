#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from common_util import *
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

# for local time
from pytz import timezone
japan_time = timezone('Japan')
sa_time = datetime.now(japan_time)
date = sa_time.strftime('%Y-%m-%d')
timestamp = sa_time.strftime('%Y-%m-%d %H:%M:%S')


amazon_sku = []
locations = []
sleeptime = 2
vpf_id = '1'				    #$ DEFAULT
vcrawl_id = '0'				    ## MASTER
vlocation_id = '0'			    ## MASTER
vlocation_name = '0'		    ## MASTER
vcreated_by= 'System'			#$ DEFAULT

def crawl_datacapture(sku):

    vsku_id = sku['sku_id']			# from MASTER
    vweb_pid = sku['web_pid'] 		# from MASTER
    vbrand_id = sku['brand_id']		# from MASTER
    vbrand_name = sku['brand_name']	# from MASTER
    vsku_name = sku['sku_name']		# from MASTER
    vgroup_id = sku['group_id']		# from MASTER

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
    vec_number_of_image= '0'                #** CRAWL **
    vpdp_bullet_count_no= '0'               #** CRAWL **
    vpdp_bullet_value= '0'                  #** CRAWL **
    vreseller_name_crawl='0'                #** CRAWL **
    banner1_img=''                           #** CRAWL **
    banner2_img=''                           #** CRAWL **
    banner1_brand=''                         #** CRAWL **
    banner2_brand=''                         #** CRAWL **
    vdp_shipping_type ='0'
    vpdp_page_url = 'https://www.amazon.co.jp/dp/'+str(vweb_pid)
    driver.get(vpdp_page_url)
    time.sleep(5)
    try:
        goto  = driver.find_element_by_id("purchase-sims-feature" )
        driver.execute_script("return arguments[0].scrollIntoView();", goto)
        time.sleep(5)
    except NoSuchElementException:
        time.sleep(2)
    #print driver.title

    try:
        html_container = driver.find_element_by_id("dp" ).get_attribute('innerHTML')
    except NoSuchElementException:
        time.sleep(2)

    
    driver.switch_to_default_content()

    vweb_pid = vweb_pid.strip()[:65535]
    vgroup_id = vgroup_id.strip()[:65535]

    if html_container is not None:
        soup = BeautifulSoup(html_container, 'html.parser')
        #print soup
        #if soup.find('noResultsTitle'):
        #	return 1
        if soup is not None:
            try:
                no_result = soup.find("h1", {"id" : "noResultsTitle"}, recursive=True)
            except NoSuchElementException:
                time.sleep(2)
            if no_result is not None:
                print('not found')
                return 1
            else:
                try:
                    html_container = driver.find_element_by_id("dp-container" ).get_attribute('innerHTML');
                except NoSuchElementException:
                    time.sleep(2)
                pdp_soup = BeautifulSoup(html_container, 'html.parser')
                        ## START :: OSA BLOCK  ##
                           
                review_capture(vcrawl_id,vweb_pid)

    ## END :: INSERT QUERY BLOCK  ##	
				
## review function to crawl all reviews of one product
def review_capture(product_crawl_id,web_pid):
    # code for product review
    driver.get("https://www.amazon.co.jp/product-reviews/"+web_pid+"/sortBy=recent&filterByStar=all_stars&pageNumber=1/ref=cm_cr_arp_d_viewopt_srt?sortBy=recent&pageNumber=1")
    time.sleep(5)
    html_container = None
    try:
        html_container = driver.find_element_by_id("cm_cr-review_list" ).get_attribute('innerHTML')
        
    except NoSuchElementException:
        time.sleep(2)

    #print(html_container)
    #quit()
    if html_container is not None:
        mainDiv = BeautifulSoup(html_container, 'html.parser')
        #pdp_soup1 = soup.encode('utf8')
        #print(mainDiv)
        #quit()
        #mainDiv = pdp_review_soup.find("div", {"id": "cm_cr-review_list"}, recursive=True)
        if mainDiv is not None:
            reviewDivs = mainDiv.findAll("div", {"data-hook": "review"}, recursive=True)
            for reviewDiv in reviewDivs:
                if reviewDiv is not None:
                    reviewWebId = reviewDiv.get('id')
                    
                    reviewTitle = reviewDiv.find("a", {"data-hook": "review-title"}, recursive=True)
                    if reviewTitle is not None:
                        reviewTitle = reviewTitle.text.strip()[:65535]
                    else:
                        reviewTitle=' '
                    
                    reviewDetail = reviewDiv.find("span", {"data-hook": "review-body"}, recursive=True)
                    if reviewDetail is not None:
                        reviewDetail = reviewDetail.text.strip()[:65535]
                    else:
                        reviewDetail=' '
                    
                    rate = reviewDiv.find("i", {"data-hook": "review-star-rating"}, recursive=True)
                    if rate is not None:
                        rating = rate.find("span", {"class": "a-icon-alt"}, recursive=True)
                        if rating is not None:
                            rating = rating.text.strip()
                            rating = rating.replace('5つ星のうち','')
                            print(rating)
                            rating = rating
                        else:
                            rating='0'
                    else:
                        rating='0'
                    
                    #print(rating)
                    reviewed_by = reviewDiv.find("span", {"class": "a-profile-name"}, recursive=True)
                    if reviewed_by is not None:
                        reviewed_by_name = reviewed_by.text.strip()
                    else:
                        reviewed_by_name='0'
                    
                    reviewed_date_span = reviewDiv.find("span", {"class": "review-date"}, recursive=True)
                    if reviewed_date_span is not None:
                        reviewed_date = reviewed_date_span.text.strip()
                        reviewed_date = reviewed_date.replace('年','-')
                        reviewed_date = reviewed_date.replace('月','-')
                        reviewed_date = reviewed_date.replace('日','')
                    else:
                        reviewed_date='0'
                    reviewed_date = parser.parse(reviewed_date).strftime('%Y-%m-%d')
                    #reviewed_date=datetime.datetime.strptime(reviewed_date, '%Y %m %d').strftime('%Y-%m-%d')

                    sql_2 = "SELECT web_review_ID FROM `amazon_crawl_review_info` WHERE web_review_ID='"+reviewWebId+"' AND web_pid='"+web_pid+"'"
                    try:
                        cursor.execute(sql_2, ())
                        result2 = cursor.fetchall()
                        if len(result2)>0:
                            print('found')
                            continue
                    except cursor.Error as e:
                        e=str(e)
                        print(e)
                    
                    print("product_crawl_id::"+str(product_crawl_id))
                    print("web_pid::"+str(web_pid))
                    print("rating::"+str(rating))
                    print("reviewTitle::"+str(reviewTitle))
                    print("reviewDetail::"+str(reviewDetail))
                    print("reviewWebId::"+str(reviewWebId))
                    print("reviewed_date::"+str(reviewed_date))
                    print("reviewed_by_name::"+str(reviewed_by_name))
                    
                    sql1 = "INSERT INTO `amazon_crawl_review_info` (`crawl_id`, `web_pid`, `star_rating`, `content_1`, `content_2`, `web_review_ID`, `review_time`, `reviewed_by`,`created_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
                    try:
                        cursor.execute(sql1, (product_crawl_id, web_pid, rating, reviewTitle, reviewDetail, reviewWebId, reviewed_date, reviewed_by_name,timestamp))
                        connection.commit()
                    except cursor.Error as e:
                        print(e)


                        
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
		try:
		    sql0 = "SELECT l.location_id,l.location,l.pincode FROM `rb_platform` as p, rb_location as l where p.pf_id='"+vpf_id+"' and p.pf_id=l.pf_id and l.status=1"
		    cursor.execute(sql0)
		    result0 = cursor.fetchall()
		    for location in result0:
		        locations.append(location)

		except cursor.Error as e:
			e=str(e)
			print(e)

		sql = "select crawl_id from rb_crawl where pf_id='"+vpf_id+"' and crawl_type=1 order by start_time desc limit 1"
		try:
		    cursor.execute(sql, ())
		    vcrawl_id = cursor.fetchone()
		    vcrawl_id= str(vcrawl_id['crawl_id'])
		except cursor.Error as e:
		    e=str(e)

		sql1 = "SELECT * FROM `rb_sku_platform` as sp, `rb_brands` as b WHERE sp.pf_id='1' and sp.brand_id=b.brand_id and sp.status=1 AND sp.web_pid !='' GROUP BY sp.web_pid"
		try:
			cursor.execute(sql1, ())
			result1 = cursor.fetchall()
			for skus in result1:
				amazon_sku.append(skus)
		except cursor.Error as e:
			e=str(e)
			print(e)


		for locationArr in locations:
		    zip_code = locationArr['pincode']
		    set_location(zip_code)            
		    vlocation_id = locationArr['location_id']
		    vlocation_name = locationArr['location']
		    vpincode = locationArr['pincode']
		    for sku in amazon_sku:
		    	review_capture(vcrawl_id,sku['web_pid'])
		
			
except cursor.Error as e:
	print(e)

finally:
	driver.quit()
	#connection.commit()
	connection.close()