# import the python mysql client

import pymysql

from common_util import * 
connection = get_jp_connection()

try:
    with connection.cursor() as cursor:
      # business logic for pdp
      try:
        cursor.execute("call usp_bl_pdp_24Rakuten()")
        connection.commit()
      except Exception as e:
        print(e)

      try:
        cursor.execute("call usp_bl_pdp_amazon()")
        connection.commit()
      except Exception as e:
        print(e)

      try:
        cursor.execute("call usp_bl_pdp_kenkocom_rakuten()")
        connection.commit()
      except Exception as e:
        print(e)

      try:
        cursor.execute("call usp_bl_pdp_lohaco()")
        connection.commit()
      except Exception as e:
        print(e)

      try:
        cursor.execute("call usp_bl_pdp_soukai_rakuten()")
        connection.commit()
      except Exception as e:
        print(e)
      # business logic for kw

      try:
        cursor.execute("call usp_bl_kw_24Rakuten()")
        connection.commit()
      except Exception as e:
        print(e)

      try:
        cursor.execute("call usp_bl_kw_amazon()")
        connection.commit()
      except Exception as e:
        print(e)

      try:
        cursor.execute("call usp_bl_kw_kenkocom_rakuten()")
        connection.commit()
      except Exception as e:
        print(e)

      try:
        cursor.execute("call usp_bl_kw_lohaco()")
        connection.commit()
      except Exception as e:
        print(e)

      try:
        cursor.execute("call usp_bl_kw_soukai_rakuten()")
        connection.commit()
      except Exception as e:
        print(e)
except Exception as e:
  print("Exeception occured:{}".format(e))


finally:
    connection.commit()
    connection.close()
