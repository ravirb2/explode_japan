# import the python mysql client

import pymysql

from common_util import * 
connection = get_jp_connection()

try:
    with connection.cursor() as cursor:
      # business logic for Review
      try:
        cursor.execute("call usp_fact_review_kenkocom_rakuten()")
        connection.commit()
      except Exception as e:
        print(e)
      try:
        cursor.execute("call usp_fact_review_lohaco()")
        connection.commit()
      except Exception as e:
        print(e)
      try:
        cursor.execute("call usp_fact_review_amazon()")
        connection.commit()
      except Exception as e:
        print(e)
      try:
        cursor.execute("call usp_fact_review_24rakuten()")
        connection.commit()
      except Exception as e:
        print(e)
      cursor.execute("CALL usp_fact_review_soukai_rakuten()")


      
except Exception as e:
  print("Exeception occured:{}".format(e))


finally:

    connection.commit()
    connection.close()

