import subprocess
import urllib
import yelp_helper
import latteart_helpers
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


container_id = 'latte'
curpath = 'scripts/'
model_dir = 'latteart_model_files/'
imgdir ='images/'
threshold = 0.6
docker = 0

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def score_imageurl(image_url):
    # download image
    image_name = imgdir + "image.jpg"
    logger.info('Starting to get %s', image_url)
    yelp_helper.get_image_from_url(image_url, image_name)
    # score image
    positive_score = latteart_helpers.label_image(image_name, model_dir)
    return positive_score

def score_yelpbiz(bizid, verbose):
    if is_ascii(bizid):
        num_images = yelp_helper.get_business_images(bizid, imgdir)
        if num_images:
            score_for_url, positive_count, img_count = latteart_helpers.label_directory(imgdir, model_dir, threshold)
        else:
            positive_count = 0
        return positive_count, img_count, score_for_url
    else:
        logger.error('bizid %s has non ascii characters', bizid)
        return 0

def get_biz_scores_from_location(location, limit, verbose):
    return latteart_helpers.rank_bizs_in_location(location, limit, model_dir, imgdir, threshold)


