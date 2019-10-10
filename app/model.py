import subprocess
import urllib
from . import yelp_helper
from . import latteart_helpers
import logging
import requests
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_dir = 'latteart_model_files/'
imgdir ='images/'
threshold = 0.6


def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def score_imageurl(image_url):
    """Given a url for an image, downloads the image and returns latte art score.
        Args:
        image_url (str): URl for image;
    """

    # download image
    image_name = imgdir + "image.jpg"
    logger.info('Calling yelp_helper to to download %s', image_url)
    if yelp_helper.get_image_from_url(image_url, image_name):
        # score image
        score = latteart_helpers.label_image(image_name, model_dir)
        # todo: log time, image_url, positive_score
        return score
    else:
        return 0;

def score_yelpbiz(bizalias, verbose):
    """Given a yelp alias for a business, downloads images from yelp for the business
     and returns both the individual scores for each image and aggregate score 
     for the business
        Args:
        bizalias (str): yelp alias for business
        verbose (bool): just get the score if false or get score for each image;
    """
    # ignore businesses with non-ascii yelp aliases
    if is_ascii(bizalias):
        # download image from yelp and return count of images downloaded
        num_images = yelp_helper.get_business_images(bizalias, imgdir)
        if num_images:
            url_to_score_hash, positive_image_count, total_image_count = latteart_helpers.label_directory(imgdir, model_dir, threshold)
        else:
            positive_count = 0
            total_image_count = 0
        return positive_image_count, total_image_count, url_to_score_hash
    else:
        logger.error('bizid %s has non ascii characters', bizid)
        return 0

def score_location(location, limit, verbose):
    return latteart_helpers.rank_bizs_in_location(location, limit, model_dir, imgdir, threshold)


