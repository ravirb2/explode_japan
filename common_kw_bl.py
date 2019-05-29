import pymysql
import pandas as pd
import sys
from common_util import * 
connection = get_jp_connection()

try:
    with connection.cursor() as cursor:

        if sys.argv[1]:
            pf_id = str(sys.argv[1])
        else:
            quit()

        cursor.execute("select * from rb_platform where pf_id="+pf_id)
        pf_result = cursor.fetchone()
        # print pf_result
        # quit()

        cursor.execute("delete from rb_kw where date(created_on) = date(now()) and pf_id="+pf_id)

        vCrawlId = ''
        cursor.execute("SELECT kw_crawl_data_id as vCrawlId FROM  rb_platform  WHERE DATE(kw_crawl_data_date) = DATE(NOW() - INTERVAL 1 DAY)  AND pf_id = "+pf_id+" AND STATUS = 1 ;")
        result0 = cursor.fetchone()
        vCrawlId= result0['vCrawlId']
        print vCrawlId
        
        vCrawlId_PDP = ''
        cursor.execute("SELECT  pdp_crawl_data_id as vCrawlId_PDP FROM  rb_platform WHERE  DATE(pdp_crawl_data_date) = DATE(NOW())  AND pf_id = "+pf_id+" AND STATUS = 1 ;")
        result0 = cursor.fetchone()
        vCrawlId_PDP= result0['vCrawlId_PDP']
        print vCrawlId_PDP

        TEMP_PDP_SOURCE = pd.read_sql("SELECT * FROM "+pf_result['pdp_table_name']+" WHERE crawl_id = "+str(vCrawlId_PDP)+" AND STATUS = 1 ;", connection)      
        TEMP_KW_SOURCE= pd.read_sql("SELECT * FROM "+pf_result['kw_table_name']+" WHERE crawl_id = "+str(vCrawlId)+" AND STATUS = 1 ;", connection)

        url_code = pd.read_sql("SELECT kws.kw_crawl_data_id,IFNULL(pds.url_code,CONCAT('ID-',kws.kw_crawl_data_id)) AS url_code_crawl FROM "+pf_result['kw_table_name']+" AS kws LEFT  JOIN "+pf_result['pdp_table_name']+" pds ON pds.pdp_title_value = kws.pdp_title_value AND pds.pf_id = "+pf_id+" AND kws.pf_id = "+pf_id+" AND pds.pdp_title_value != '0' WHERE pds.`crawl_id` = "+str(vCrawlId_PDP)+" AND kws.`crawl_id`= "+str(vCrawlId)+" GROUP BY kws.kw_crawl_data_id, url_code_crawl",connection)
        final_df = TEMP_KW_SOURCE.merge(url_code, on="kw_crawl_data_id", how="left")

        final_df['kw_crawl_data_id']= final_df.kw_crawl_data_id.astype(str)
    
        final_df['kw_crawl_data_id'] = 'ID-'+final_df['kw_crawl_data_id']    
        final_df.url_code_crawl_y = final_df.url_code_crawl_y.combine_first(final_df.kw_crawl_data_id)    
        
        final_df1 = final_df[['crawl_id','pf_id', 'location_id', 'location_name', 'pincode','brand_id', 'brand_name', 'brand_name_th','keyword_id','keyword','position','url_code_crawl_y','pdp_title_value','is_rb','pdp_page_url','created_on','created_by','modified_on','modified_by','status','brand_crawl','pdp_discount_value','pdp_sponsored']] 
        final_df1.columns = ['crawl_id','pf_id', 'location_id', 'location_name', 'pincode','brand_id', 'brand_name', 'brand_name_th','keyword_id','keyword','keyword_search_rank','keyword_search_product_id','keyword_search_product','keyword_is_rb_product','keyword_page_url','created_on','created_by','modified_on','modified_by','status','brand_crawl','pdp_discount_value','pdp_sponsored']
        
        #writer = pd.ExcelWriter('output11.xlsx', options={'strings_to_urls': False})
        #final_df1.to_excel(writer,'Sheet1')
        #writer.save()
        final_df1.to_dense().to_csv(pf_result['kw_table_name']+'.csv', index = False, sep=',', encoding='utf-8')        
        cursor.execute("LOAD DATA LOCAL INFILE '"+pf_result['kw_table_name']+".csv' INTO TABLE rb_kw FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS (`crawl_id`,`pf_id`,`location_id`,`location_name`,`pincode`,`brand_id`,`brand_name`,`brand_name_th`,`keyword_id`,`keyword`,`keyword_search_rank`,`keyword_search_product_id`,`keyword_search_product`,`keyword_is_rb_product`,`keyword_page_url`,`created_on`,`created_by`,`modified_on`,`modified_by`,`status`,`brand_crawl`,`pdp_discount_value`,`pdp_sponsored`) SET `keyword_type`=1, `platform_name`='"+pf_result['pf_name']+"', `kw_crawl_date`=CURRENT_TIMESTAMP, `created_on`=CURRENT_TIMESTAMP,`week`=concat(year(now()), week(now())), `month`=month(now()), `quarter`= QUARTER(NOW()), `year`=year(now())")
      
except Exception as e:
  print("Exeception occured:{}".format(e))


finally:
    connection.commit()
    connection.close()