#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from common_util import * 
import re
import requests
import time
#import datetime
from dateutil import parser
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from datetime import datetime, timedelta
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
driver = webdriver.Chrome(options=options, executable_path=r'C:\\driver\\chromedriver.exe')
#driver = webdriver.Chrome()

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
def clean(x, loc=2):
    return str(x)[loc:][:-loc]
    
## review function to crawl all reviews of one product
def review_capture(product_crawl_id,web_pid):
    # code for product review
    driver.get(" https://lohaco.jp/product/"+web_pid+"/review/?int_id=product_reviewList")
    time.sleep(7)
    html_container = None
    try:
        html_container = driver.find_element_by_id("main").get_attribute('innerHTML')       
    except NoSuchElementException:
        time.sleep(2)
        
    if html_container is not None:
        mainDiv = BeautifulSoup(html_container, 'html.parser')
        mainDiv_final = mainDiv.find("div", {"class": "reviewContentBody"}, recursive=True)
        if mainDiv_final is not None:
            reviewDivs = mainDiv_final.findAll("div", {"class": "userReviewBottom"})           
            for reviewDiv in reviewDivs:
                if reviewDiv is not None:
                    reviewWebId = '0'
                   
                    reviewTitle_div = reviewDiv.find("div", {"class": "general mb10"}, recursive=True)
                    if reviewTitle_div is not None:
                        reviewTitle1 = reviewTitle_div.find("dt",recursive=True)
                        if reviewTitle1 is not None:
                            reviewTitle = reviewTitle1.text
                    else:
                        reviewTitle=' '
                    
                    reviewDetail = reviewDiv.find("div", {"class": "userCommentInner"}, recursive=True)
                    if reviewDetail is not None:
                        reviewDetail = reviewDetail.text.strip()[:65535]
                    else:
                        reviewDetail=' '
                    
                    rate = reviewDiv.find("div", {"class": "general mb10"}, recursive=True)
                    if rate is not None:
                        rating = rate.find("dd", {"class": "numeric"}, recursive=True)
                        if rating is not None:
                            rating = rating.text.strip()
                            print(rating)
                            rating = rating
                        else:
                            rating='0'
                    else:
                        rating='0'
                    
                    #print(rating)
                    reviewed_by = reviewDiv.find("div", {"class": "userReview bgNone"}, recursive=True)
                    if reviewed_by is not None:
                        reviewed_by_final = reviewed_by.find("a")
                        if reviewed_by_final is not None:
                            reviewed_by_name = reviewed_by_final.text.strip()
                    else:
                        reviewed_by_name='0'
                    
                    reviewed_date_span = reviewDiv.find("div", {"class": "score"}, recursive=True)
                    if reviewed_date_span is not None:
                        try:
                            reviewed_date_span = re.findall(r'(?is)<div class="userReview bgNone">.*?<p>投稿日時：(.*?)</p>', str(reviewed_date_span));
                            reviewed_date_span = clean(re.sub(r'(?is)<div class="userReview bgNone">.*?<p>投稿日時：(.*?)</p>',r'\1',str(reviewed_date_span)));
                            reviewed_date = reviewed_date_span.replace('\\xe5\\xb9\\xb4','-')
                            reviewed_date = reviewed_date.replace('\\xe6\\x9c\\x88','-')
                            reviewed_date = reviewed_date.replace('\\xe6\\x97\\xa5','')
                            reviewed_date = reviewed_date.replace('年','-')
                            reviewed_date = reviewed_date.replace('月','-')
                            reviewed_date = reviewed_date.replace('日','')
                            reviewed_date = parser.parse(reviewed_date).strftime('%Y-%m-%d')
                        except NoSuchElementException:
                            reviewed_date_span='0'
                        
                    else:
                        reviewed_date='0'
                    print(reviewed_date)
                    #reviewed_date=datetime.datetime.strptime(reviewed_date, '%Y %m %d').strftime('%Y-%m-%d')
                    pre_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
                    if reviewed_date == pre_date:
                        print("product_crawl_id::"+str(product_crawl_id))
                        print("web_pid::"+str(web_pid))
                        print("rating::"+str(rating))
                        print("reviewTitle::"+str(reviewTitle))
                        print("reviewDetail::"+str(reviewDetail))
                        print("reviewWebId::"+str(reviewWebId))
                        print("reviewed_date::"+str(reviewed_date))
                        print("reviewed_by_name::"+str(reviewed_by_name))
                        sql1 = "INSERT INTO `lohaco_crawl_review_info` (`crawl_id`, `web_pid`, `star_rating`, `content_1`, `content_2`, `web_review_ID`, `review_time`, `reviewed_by`,`created_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
                        try:
                            cursor.execute(sql1, (product_crawl_id, web_pid, rating, reviewTitle, reviewDetail, reviewWebId, reviewed_date, reviewed_by_name,timestamp))
                            connection.commit()
                        except cursor.Error as e:
                            print(e)

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
    #vpdp_page_url = 'https://lohaco.jp/product/8368206'
    #driver.get(vpdp_page_url)
    #review_capture(vcrawl_id,vweb_pid)
    ## END :: INSERT QUERY BLOCK  ##	


try:
	with connection.cursor() as cursor:
		try:
		    sql0 = "SELECT l.location_id,l.location,l.pincode FROM `rb_platform` as p, rb_location as l where p.pf_id='"+vpf_id+"' and p.pf_id=l.pf_id and l.status=1 limit 1"
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

		sql1 = "SELECT * FROM `rb_sku_platform` as sp, `rb_brands` as b WHERE sp.pf_id='"+vpf_id+"' and sp.brand_id=b.brand_id and sp.status=1 AND sp.web_pid !='' GROUP BY sp.web_pid"
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
		    #set_location(zip_code)            
		    vlocation_id = locationArr['location_id']
		    vlocation_name = locationArr['location']
		    vpincode = locationArr['pincode']

		    for sku in amazon_sku:
		    	review_capture(vcrawl_id,sku['web_pid'])
		
			
except cursor.Error as e:
	print(e)

finally:
	driver.quit()
	connection.close()
    