# import the python mysql client

import pymysql

from common_util import * 
connection = get_jp_connection()

try:
    with connection.cursor() as cursor:
      cursor.execute("call usp_fact_osa()")
      cursor.execute("call usp_fact_vendorcentral_dim()")
      cursor.execute("call usp_fact_keyword()")
      cursor.execute("call usp_fact_platform_dim()")
      cursor.execute("call usp_fact_product_dim()")
      cursor.execute("call usp_fact_kpi_dim()")
      cursor.execute("call usp_fact_seller_dim()")
      cursor.execute("call usp_fact_review()")
      cursor.execute("call usp_fact_brand_dim()")
      cursor.execute("call usp_fact_traffic_dim()")
      # cursor.execute("call usp_fact_traffic_dim_new()")
      
except Exception as e:
  print("Exeception occured:{}".format(e))


finally:
    connection.commit()
    connection.close()
