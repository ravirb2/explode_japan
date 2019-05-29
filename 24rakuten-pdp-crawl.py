#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from common_util import *
get_cron_info(58)
import json
import re
import requests
import time
#import datetime
import logging
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

#connecion string 
connection = get_jp_connection()

#connecion string
from pytz import timezone
japan_time = timezone('Japan')
sa_time = datetime.now(japan_time)
timestamp = sa_time.strftime('%Y-%m-%d %H:%M:%S')

lazada_sku = []
locations = []
sleeptime = 10
vpf_id = '5'				#$ DEFAULT
vcrawl_id = '0'				## MASTER
vlocation_id = '0'			## MASTER
vlocation_name = '0'		## MASTER
vcreated_by= 'System'			#$ DEFAULT


def crawl_datacapture(action,sku):
	vsku_id = sku['sku_id']						# from MASTER
	vweb_pid = sku['web_pid'] 					# from MASTER
	vbrand_id = sku['brand_id']					# from MASTER
	vbrand_name = sku['brand_name']				# from MASTER
	vreseller_id = sku['reseller_id']			# from MASTER
	vgroup_id = sku['group_id']					# from MASTER
	vreseller_type = sku['reseller_type']		# from MASTER
	vpdp_url_code = sku['url_code']				# from MASTER
	vpdp_page_url = sku['url']					# from MASTER

	vosa = '0'					#** CRAWL **
	vosa_remark = '0'			#** CRAWL **
	vprice_rp = 0			    #** CRAWL **
	vprice_sp = 0			    #** CRAWL **
	vpdp_discount_value = 0	#** CRAWL **
	vpdp_title_value = '0' 		#** CRAWL **
	vpdp_desc_value = '0'		#** CRAWL **
	vpdp_image_count = 0		#** CRAWL **
	vpdp_image_url= '0'			#** CRAWL **
	vpdp_rating_value = 0		#** CRAWL **
	vpdp_rating_count = 0		#** CRAWL **
	vpdp_review_count = 0		#** CRAWL **
	vpdp_qa_count = 0			#** CRAWL **
	vpdp_bulletin_value = '0'
	vpdp_number_of_bulletin = '0'
	vec_keyvisuals = '0'   		#** CRAWL **
	vec_comp_table = '0'		#** CRAWL **
	vec_faq = '0'				#** CRAWL **
	vec_howtouse = '0'			#** CRAWL **
	vec_vidio = '0'				#** CRAWL **
	vec_rwd = '0'				#** CRAWL **
	vreseller_name = ''		    #** CRAWL **
	#vpdp_page_url = 'https://item.rakuten.co.jp/soukai/12478/' #** CRAWL **
	if vpdp_page_url.strip() == '':
		print('no url found')
	else:
		pdp_html_doc = None
		pdp_soup = None
		driver.get(vpdp_page_url)
		time.sleep(4) 
		html_doc = None
		try:
			pdp_html_doc = driver.find_element_by_id("pagebody").get_attribute('innerHTML')
			time.sleep(3)
		except NoSuchElementException:
			time.sleep(1)
		if pdp_html_doc is not None:
			pdp_soup = BeautifulSoup(pdp_html_doc, 'html.parser')
			if pdp_soup is not None:
				title = pdp_soup.find("span", {"class": "item_name"}, recursive=True)
				if title is not None:
					vpdp_title_value = title.text.strip()
					vpdp_title_value  = vpdp_title_value
					vpdp_title_value = (vpdp_title_value[:500] + '..') if len(vpdp_title_value) > 500 else vpdp_title_value
			   
				vprice_rp = 0
				price_in = pdp_soup.find("div", {"id": "priceCalculationConfig"}, recursive=True)
				if price_in is not None:
					price = price_in['data-price']
					if price is not None:
						vprice_sp = price.replace(',','')
				else:
					vprice_sp = 0

				if vprice_sp==0:
					vprice_sp = vprice_rp
				if vprice_rp == 0:
					vprice_rp = vprice_sp
				
				
				rate = pdp_soup.find("span", {"class": "item-review"})
				if rate is not None:
					rate_table= rate.findAll('li', {'class':'review-star star-full'})
					vpdp_rating_count= len(rate_table)

					review_cnt= rate.find('span', {'id':'js-item-review-count-link'})
					review_cnt= review_cnt.text.strip()
					vpdp_review_count= ''.join(filter(str.isdigit, review_cnt))
				else:
					vpdp_rating_value=0
					vpdp_review_count = 0

				productImageBox = pdp_soup.find("a", {"data-ratid": "itempopup_1"})
				if productImageBox is not None:
					image= productImageBox.find("img")
					if image is not None:
						vpdp_image_url = image['src']
					else:
						vpdp_image_url = '0'
				else:
					vpdp_image_url = '0'
				
				productImageBox = pdp_soup.findAll("a", {"class": "rakutenLimitedId_ImageMain1-3"})
				if productImageBox is not None:
					vpdp_image_count = len(productImageBox) -1
				else:
					vpdp_image_count = 1
					
				reseller_name_div =pdp_soup.find("div", {"class": "seller-name__detail"}, recursive=True) 
				if reseller_name_div is not None:
					vreseller_name= reseller_name_div.find("a", {"class": "pdp-link pdp-link_size_l pdp-link_theme_black seller-name__detail-name"}, recursive=True)
					vreseller_name=vreseller_name.text
				else:
					vreseller_name ='0'
					
				add_to_cart =pdp_soup.find("button", {"class": "add-cart"}, recursive=True)  
				if add_to_cart is not None:
					vosa_remark = '1'
					vosa = '1'
				else:
					vosa_remark = '0'
					vosa = '0'
				
				details = pdp_soup.find("span", {"class": "item_desc"})
				if details is not None:
					details = details.text.strip()
					vpdp_desc_value = details

					
				discount = pdp_soup.find("span", {"class": "pdp-product-price__discount"}, recursive=True)
				if discount is not None:
					discount_txt = discount.text
					discount_txt =discount_txt.replace('%','')
					discount_txt =discount_txt.replace('-','')
					vpdp_discount_value = discount_txt
				else: 
					vpdp_discount_value = 0
					
				try:
					review_capture(vcrawl_id,vweb_pid)
				except Exception as e:
					print('No review')
			else:
				vosa_remark = '2'
		else:
			vosa_remark = '2'

	print('pf_id::  '  + str(vpf_id))
	print('crawl_id::  '  + str(vcrawl_id))
	print('sku_id::  '  + str(vsku_id))
	print('web_pid::  '  + str(vweb_pid))
	print('pdp_title_value::  '  + str(vpdp_title_value))
	print('brand_id::  '  + str(vbrand_id))
	print('brand_name::  '  + str(vbrand_name))
	print('price_rp::  '  + str(vprice_rp))
	print('price_sp::  '  + str(vprice_sp))
	print('pdp_rating_value::  '  + str(vpdp_rating_value))
	print('pdp_review_count::  '  + str(vpdp_review_count))
	print('pdp_rating_count::  '  + str(vpdp_rating_count))
	print('pdp_qa_count::  '  + str(vpdp_qa_count))
	print('pdp_desc_value::  '  + str(vpdp_desc_value))
	print('pdp_image_count::  '  + str(vpdp_image_count))
	print('pdp_image_url::  '  + str(vpdp_image_url))
	print('osa::  '  + str(vosa))
	print('osa_remark::  '  + str(vosa_remark))
	print('pdp_page_url::  '  + str(vpdp_page_url))
	print('url_code::  '  + str(vpdp_url_code))
	print('pdp_discount_value::  '  + str(vpdp_discount_value))
	print('location_id::  '  + str(vlocation_id))
	print('location_name::  '  + str(vlocation_name))
	print('group_id::  '  + str(vgroup_id))
	print('vreseller_id::  '  + str(vreseller_id))
	print('vreseller_type::  '  + str(vreseller_type))
	print('created_by::  '  + str(vcreated_by))
	print('pdp_bulletin_value::  '  + str(vpdp_bulletin_value))
	print('pdp_number_of_bulletin::  '  + str(vpdp_number_of_bulletin))
	print('reseller_name::  '  + str(vreseller_name))
	print('ec_keyvisuals::  '  + str(vec_keyvisuals))
	print('ec_comp_table::  '  + str(vec_comp_table))
	print('ec_faq::  '  + str(vec_faq))
	print('ec_howtouse::  '  + str(vec_howtouse))
	print('ec_vidio::  '  + str(vec_vidio))
	print('ec_rwd::  '  + str(vec_rwd))
	## START :: INSERT QUERY BLOCK  ##
	if action =='INSERT':
		sql1 = "INSERT INTO `24rakuten_crawl_pdp` (`pf_id`,`crawl_id`, `sku_id`,`web_pid`,`reseller_id`, `reseller_type`, `pdp_title_value`, `brand_id`,`brand_name`,`price_rp`,`price_sp`, `pdp_rating_value`, `pdp_review_count`,`pdp_rating_count`, `pdp_qa_count`,`pdp_desc_value`, `pdp_image_count`,`pdp_image_url`, `osa`,`osa_remark`,`pdp_page_url`, `url_code`,`pdp_discount_value`, `pdp_bulletin_value`, `pdp_number_of_bulletin`,`reseller_name_crawl`,`ec_keyvisuals`,`ec_comp_table`,`ec_faq`,`ec_howtouse`,`ec_vidio`,`ec_rwd`,`location_id`, `location_name`,`group_id`,`created_by`,`created_on`) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
		try:
			cursor.execute(sql1, ( 
			vpf_id,
			vcrawl_id,
			vsku_id,
			vweb_pid,
			vreseller_id,
			vreseller_type,
			vpdp_title_value.strip()[:65535],
			vbrand_id,
			vbrand_name,
			vprice_rp,
			vprice_sp,
			vpdp_rating_value,
			vpdp_review_count,
			vpdp_rating_count,
			vpdp_qa_count,
			vpdp_desc_value,
			vpdp_image_count,
			vpdp_image_url,
			vosa,
			vosa_remark,
			vpdp_page_url,
			vpdp_url_code,
			vpdp_discount_value,
			vpdp_bulletin_value,
			vpdp_number_of_bulletin,
			vreseller_name,
			vec_keyvisuals,
			vec_comp_table,
			vec_faq,
			vec_howtouse,
			vec_vidio,
			vec_rwd,
			vlocation_id,
			vlocation_name,
			vgroup_id,
			vcreated_by,
			timestamp
			))
			connection.commit()
		except cursor.Error as e:
			e=str(e)
			print(e)
			# creating error file. it will be replaced with send email function
			# sendmail(e)
			#errorLog.write(e)

def review_capture(vcrawl_id,vweb_pid):
	reviewTitle=''
	reviewWebId='0'	
	try:
		driver.execute_script("window.scrollTo(0, 100)")
		time.sleep(1)		
		driver.find_element_by_id("js-item-review-count-link").click()
		time.sleep(2)
	except Exception as e:
		time.sleep(2)

	try:
		html_doc1 = driver.find_element_by_id("js-review-widget").get_attribute('innerHTML')
		time.sleep(1) 
		pdp_soup1 = BeautifulSoup(html_doc1, 'html.parser')
		review_div = pdp_soup1.find("table", {"data-ratid" : "ratReviewParts"})

		if review_div is not None:
			review_all = review_div.find('td')		
			reviewDivs = review_div.findAll("div", recursive=True)
			reviewDivs = reviewDivs[1]		
			allData = reviewDivs.findAll('p')
			
			try:
				reviewed_by_name = allData[0].text.strip()				
			except Exception as e:
				reviewed_by_name='0'
				
			try:
				reviewed_date_span = allData[1].text.strip()
				date_data = str(''.join(filter(str.isdigit, reviewed_date_span)))
				reviewed_date= str(date_data[:4])+'-'+str(date_data[4:6])+'-'+str(date_data[6:8])			
			except Exception as e:
				reviewed_date = '0'
				
			rd = datetime.datetime.strptime(reviewed_date, '%Y-%m-%d').strftime('%Y-%m-%d')			
			pre_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
			
			if rd == pre_date:				
				try:
					reviewDetail = allData[3].text.strip()
				except Exception as e:
					reviewDetail= ''
				
				try:
					allImg = reviewDivs.findAll('img')
					rating_img= allImg[0]['src']
					rating = '0'
					if rating_img == '/images/rms/review/review_1.0.gif':
						rating = '1'
						
					if rating_img == '/images/rms/review/review_2.0.gif':
						rating = '2'
						
					if rating_img == '/images/rms/review/review_3.0.gif':
						rating = '3'
						
					if rating_img == '/images/rms/review/review_4.0.gif':
						rating = '4'
						
					if rating_img == '/images/rms/review/review_5.0.gif':
						rating = '5'
						
				except Exception as e:
					rating='0'			
					
				product_crawl_id = vcrawl_id
				print("product_crawl_id::"+str(product_crawl_id))
				print("web_pid::"+str(vweb_pid))
				print("rating::"+str(rating))
				print("reviewTitle::"+str(reviewTitle))
				print("reviewDetail::"+str(reviewDetail))
				print("reviewWebId::"+str(reviewWebId))
				print("reviewed_date::"+str(reviewed_date))
				print("reviewed_by_name::"+str(reviewed_by_name))
				
				sql1 = "INSERT INTO `24rakuten_crawl_review_info` (`crawl_id`, `web_pid`, `star_rating`, `content_1`, `content_2`, `web_review_ID`, `review_time`, `reviewed_by`,`created_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
				try:
					cursor.execute(sql1, (
					product_crawl_id, 
					vweb_pid, 
					rating, 
					reviewTitle, 
					reviewDetail, 
					reviewWebId, 
					reviewed_date, 
					reviewed_by_name,
					timestamp))
					connection.commit()
				except cursor.Error as e:
					e=str(e)
					print(e)
		
	except Exception as e:
		time.sleep(1)

try:
	with connection.cursor() as cursor:
		vpf_id = str(vpf_id)
		sql1 = "SELECT * FROM `rb_sku_platform` as sp, `rb_brands` as b WHERE sp.pf_id='"+vpf_id+"' and sp.brand_id=b.brand_id  AND sp.web_pid !='' and sp.status=1"

		cursor.execute(sql1)
		result1 = cursor.fetchall()
		for skus in result1:
			lazada_sku.append(skus)

		sql = "INSERT INTO `rb_crawl` (`pf_id`, `start_time`,`no_of_sku_parsed`, `crawl_type`) VALUES (%s, %s, %s, %s)"
		try:
			print('testing one')
			cursor.execute(sql, (vpf_id,timestamp,'0','1'))
			vcrawl_id = connection.insert_id()
			connection.commit()
		except cursor.Error as e:
			e=str(e)
			
		product_count = 0
		for sku in lazada_sku:
			crawl_datacapture('INSERT',sku)
			product_count = int(product_count)+1

		product_count = str(product_count)
		vcrawl_id = str(vcrawl_id)
		sa_time = datetime.now(japan_time)
		timestamp = sa_time.strftime('%Y-%m-%d %H:%M:%S')
		try:
			print('completed')
			cursor.execute("UPDATE rb_crawl SET status=1, end_time = '"+timestamp+"',no_of_sku_parsed='"+product_count+"' WHERE crawl_id='"+vcrawl_id+"'")
			connection.commit()
		except cursor.Error as e:
			print(e)
			# creating error file. it will be replaced with send email function
			# sendmail(e)
			#errorLog.write(e)

		try:
			print('completed')
			cursor.execute("UPDATE rb_platform SET  pdp_crawl_data_date = '"+timestamp+"', pdp_crawl_data_id='"+vcrawl_id+"' WHERE pf_id='"+vpf_id+"'")
			connection.commit()
		except cursor.Error as e:
			e=str(e)
		try:
		    kpi_id = '58'
		    kpi_name = 'JP_24rakuten_pdp'
		    run_status = 'success'
		    update_cron_status(kpi_id,kpi_name,run_status);
		except Exception as e:
		    e=str(e)
			# creating error file. it will be replaced with send email function
			# sendmail(e)
			#errorLog.write(e)
			
except cursor.Error as e:
	print(e)
	# creating error file. it will be replaced with send email function
	# sendmail(e)
	#errorLog.write(e)
finally:
	driver.quit()
	#connection.commit()
	connection.close()
