from bs4 import BeautifulSoup
from urllib import urlopen
import urllib
import os
import shutil
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info('Grabbing images for %s and putting them in %s', biz_name, image_download_path)

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
    logger.info('Found %s images', len(photos))
    if len(photos) > 0:
        for photo in photos:
            urllib.urlretrieve(photo['src'], image_download_path + str(i) +".jpg")
            i+=1
        logger.info('Finished getting %s images for %s', i, biz_name)
        return i
    else:
        logger.error('No photos found', exc_info=True)

if __name__ == "__main__":
   main(sys.argv[1:])