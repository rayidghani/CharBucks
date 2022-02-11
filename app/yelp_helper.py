# -*- coding: utf-8 -*-
"""
Adapted from Yelp Fusion API code sample.

Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.
"""

from __future__ import print_function
from __future__ import absolute_import

import argparse
import json
import pprint
import requests
import sys
import os
import shutil
import sys
import logging
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# todo: read from config file
model_dir = 'latteart_model_files/'
data_dir = 'data/'
imgdir ='images/'
threshold = 0.6
bizlogfile=data_dir+'bizscores.log'
imglogfile=data_dir+'imgscores.log'
locationfile=data_dir+'locations.txt'



# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app

YELP_API_KEY = os.environ.get('YELP_API_KEY')
if YELP_API_KEY:
    logger.debug('Loaded Yelp API Key %s', YELP_API_KEY)
else:
    logger.error('No environment variable set for Yelp API key - export YELP_API_KEY=XXX')

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


def get_business_ids_from_api(location, num_of_businesses_to_get, offset):
    """Queries the API based on the input location from the user.

    Args:
        location (str): The location of the business to query.
    """
    logger.info('Calling search api for location %s and getting %d businesses', location, num_of_businesses_to_get)
    response = search(YELP_API_KEY, location, num_of_businesses_to_get, offset)
    businesses = response.get('businesses')
    if not businesses:
        logger.error('No relevant businesses found in %s', location)
        return 0
    else:
        num_of_businesses = len(businesses)
        business_ids_list = []
        for business in businesses:
            business_ids_list.append(business['id'])
        return business_ids_list


def search(api_key, location, num_of_businesses_to_get, offset):
    """Query the Search API by a search term and location.

    Args:
        location (str): The search location passed to the API.
        num_of_businesses_to_get (int): # of businesses you want to get 
        offset (int): start from offset

    Returns:
        dict: The JSON response from the request.
    """
    # change here to get different categories or search terms
    # todo: load from config file
    #term = "espresso"
    term = "latte"
    category = "coffee"
    # coffeeroasteries
    url_params = {
        'term': term.replace(' ', '+'),
        'categories': category.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': num_of_businesses_to_get,
        'offset': offset
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)

def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(YELP_API_KEY, term, location)
    businesses = response.get('businesses')
    business_id = businesses[0]['id']
    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(YELP_API_KEY, business_id)
    print(u'Result for business "{0}" found:'.format(business_id))
    pprint.pprint(response, indent=2)


def get_image_from_url(image_url, image_name):
    # download image from image_url
    try:
        r = requests.get(image_url, verify=False)
        image_file = open(image_name, 'wb')
        for chunk in r.iter_content(100000):
            image_file.write(chunk)
        image_file.close()
        return image_name
    except:
        logger.error('image could not be retrieved - waiting 60 seconds')
        time.sleep(60)
        return 0


    logger.info('Querying %s with headers %s and url params %s ...', url, headers, url_params)

    response = requests.request('GET', url, headers=headers, params=url_params, verify=False)
    logger.debug('querying returned json %s',response.json())
    return response.json()


def get_business_images(biz_name,image_download_path):
    """download yelp images for a business

    Args:
        biz_name: yelp business id
        image_download_path: directory to store images in.

    Returns:
        Downloads and returns the number of images downloaded.
    """
    logger.info('Downloading images for %s and putting them in %s', biz_name, image_download_path)

    # delete if the directory already exists from last run
    shutil.rmtree(image_download_path)
    # make the directory again
    os.makedirs(image_download_path)
    temp_log_file = open(image_download_path + 'tmplog.txt', "w")
    
    url = 'http://www.yelp.com/biz_photos/' + biz_name
    urlfordrinks = 'http://www.yelp.com/biz_photos/' + biz_name + '?tab=drink'

    page = requests.get(urlfordrinks, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')
    photos = soup.findAll ('img', {'class' : 'photo-box-img'}, limit=None)
    if len(photos) > 30:
        # if we found more than 30 photos, go to the next page of photos
        nexturldrinks = 'http://www.yelp.com/biz_photos/' + biz_name + '?start=30&tab=drink'
        page = requests.get(nexturldrinks, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')
        new_photos = soup.findAll ('img', {'class' : 'photo-box-img'}, limit=None)
        photos.extend(new_photos)

    logger.info('Found %s images for drinks', len(photos))
    image_counter=0
    if not(len(photos)):
    # if there were no drink photos, try getting regular photos
            page = requests.get(url, verify=False)
            soup = BeautifulSoup(page.text, 'html.parser')
            photos = soup.findAll ('img', {'class' : 'photo-box-img'}, limit=None)
            # go to next page if it exists and get more photos
            if len(photos) > 30:
                nexturl = 'http://www.yelp.com/biz_photos/' + biz_name + '?start=30&tab=drink'
                page = requests.get(nexturl, verify=False)
                soup = BeautifulSoup(page.text, 'html.parser')
                new_photos = soup.findAll ('img', {'class' : 'photo-box-img'}, limit=None)
                photos.extend(new_photos)
            logger.info('No drink images found. Getting %s images for the business overall', len(photos))
    
    if len(photos):
    # if any photos were found
        for photo in photos:
            # todo: deal with error in getting image
            if get_image_from_url(photo['src'], image_download_path + str(image_counter) + ".jpg"):

                # urllib.urlretrieve(photo['src'], image_download_path + str(i) + ".jpg")
                logger.info('Finished getting image %s', image_counter)
                temp_log_file.write(str(image_counter) + ".jpg," + photo['src'] + "\n")
                image_counter+=1
        logger.info('Finished getting %s images for %s', image_counter, biz_name)
        temp_log_file.close()
        return image_counter
    else:
        logger.error('No images found', exc_info=True)
        return 0

