from bs4 import BeautifulSoup
from urllib import urlopen
import urllib
import os
import shutil
import sys

# change this as you see fit
biz_name = sys.argv[1] 
image_path = sys.argv[2]

shutil.rmtree(image_path)
os.makedirs(image_path)
url =   'http://www.yelp.com/biz_photos/' + biz_name
page = urlopen(url)
soup = BeautifulSoup(page.read(), 'html.parser')
photos = soup.findAll ('img', {'class' : 'photo-box-img'}, limit=None)

i=0
for photo in photos:
    urllib.urlretrieve(photo['src'], image_path + str(i) +".jpg")
    i+=1

