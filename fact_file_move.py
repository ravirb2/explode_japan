import shutil
import os
import datetime
import glob
import time

source = 'C:\\Users\\Public\\factfile\\japan\\'
dest1 = 'C:\\Users\\rb\\RB\\eXplode Japan - Documents\\'
files = os.listdir(source)

if len(files) == 0:
    quit()


current_month = datetime.date.today().strftime("%Y-%m")
countrylist = ''

path =dest1 + current_month
delete_file= path +"\\*" 
file_test = glob.glob(delete_file)
for f in file_test:
    os.remove(f)
try:
    os.rmdir(path)
except OSError:
    print "no directory found"
    
try:  
    os.mkdir(path)
except OSError:  
    print ("Creation of the directory %s failed" % path)
else:  
    print ("Successfully created the directory %s" % path)
try:
    for f in files:
            src =source+f
            dest1 =path+"\\"+f
            os.rename(src, dest1)
except OSError:
    print "file alredy exist"
        
