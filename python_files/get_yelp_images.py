from bs4 import BeautifulSoup
from urllib import urlopen
import urllib
import os
import shutil
import sys

def main(argv):
    """Function used to download yelp images for a business

    Args:
        argv[1]: yelp business id
        argv[2]: directory to store images in.

    Returns:
        Returns the number of images downloaded.
    """
    biz_name = sys.argv[1] 
    image_download_path = sys.argv[2]
    # delete if the directory already exists from last run
    shutil.rmtree(image_download_path)
    # make the directory again
    os.makedirs(image_download_path)
    url = 'http://www.yelp.com/biz_photos/' + biz_name

    # todo: switch to this later on and test only grabbing images of drinks
    urlfordrinks =   'http://www.yelp.com/biz_photos/' + biz_name + '?tab=drink'

    page = urlopen(url)
    soup = BeautifulSoup(page.read(), 'html.parser')
    photos = soup.findAll ('img', {'class' : 'photo-box-img'}, limit=None)
    i=0
    for photo in photos:
        urllib.urlretrieve(photo['src'], image_download_path + str(i) +".jpg")
        i+=1
    return i

if __name__ == "__main__":
   main(sys.argv[1:])