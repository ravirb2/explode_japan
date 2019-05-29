import pymysql.cursors
def get_connection():
	connection = pymysql.connect(host='3.18.127.118',
	user='rbuser',
	password='ohr6ePEVJASbrbhealth',
	#port=2499,
	db='rbexplode_jp1',
	charset='utf8',
	local_infile=True,
	cursorclass=pymysql.cursors.DictCursor)
	return connection