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
from urllib.request import urlopen
from bs4 import BeautifulSoup
# from . import creds

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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app

# client_id and client_secret are now deprecated
#CLIENT_ID = creds.login['client_id']
#CLIENT_SECRET = creds.login['app_secret']
#API_KEY = creds.login['api_key']
API_KEY = os.environ.get('API_KEY')

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

def get_image_from_url(image_url, image_name):

    # download image from image_url
    r = requests.get(image_url, verify=False)
    #image_name = "image_to_classify__" + str(random.randint(1,10000)) + ".jpg"
    image_file = open(image_name, 'wb')
    for chunk in r.iter_content(100000):
        image_file.write(chunk)
    image_file.close()
    return image_name


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

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params, verify=False)

    return response.json()


def search(api_key, location, num_of_businesses_to_get):
    """Query the Search API by a search term and location.

    Args:
        location (str): The search location passed to the API.
        num_of_businesses_to_get (int): # of businesses you want to get 

    Returns:
        dict: The JSON response from the request.
    """
    term = "espresso"
    category = "coffee"
    url_params = {
        'term': term.replace(' ', '+'),
        'categories': category.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': num_of_businesses_to_get
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)
    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']
    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    pprint.pprint(response, indent=2)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)

def get_business_ids_from_api(location, num_of_businesses_to_get):
    """Queries the API by the input values from the user.

    Args:
        location (str): The location of the business to query.
    """
    #bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

    logger.info('Getting search results from api')
    response = search(API_KEY, location, num_of_businesses_to_get)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses in {0} found.'.format(location))
        return

    num_of_businesses = len(businesses)
    list_to_return = []
    for business in businesses:
        list_to_return.append(business['id'])
 
    return list_to_return

def get_business_images(biz_name,image_download_path):
    """Function used to download yelp images for a business

    Args:
        argv[1]: yelp business id
        argv[2]: directory to store images in.

    Returns:
        Returns the number of images downloaded.
    """
    logger.info('Grabbing images for %s and putting them in %s', biz_name, image_download_path)

    # delete if the directory already exists from last run
    shutil.rmtree(image_download_path)
    # make the directory again
    os.makedirs(image_download_path)
    log_file = open(image_download_path + 'log.txt', "w")
    
    url = 'http://www.yelp.com/biz_photos/' + biz_name

    # todo: switch to this later on and test only grabbing images of drinks
    urlfordrinks =   'http://www.yelp.com/biz_photos/' + biz_name + '?tab=drink'

    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')
    photos = soup.findAll ('img', {'class' : 'photo-box-img'}, limit=None)
    i=0
    logger.info('Found %s images', len(photos))
    if len(photos) > 0:
        for photo in photos:
            get_image_from_url(photo['src'], image_download_path + str(i) + ".jpg")
            # urllib.urlretrieve(photo['src'], image_download_path + str(i) + ".jpg")
            log_file.write(str(i) + ".jpg," + photo['src'] + "\n")
            i+=1
        logger.info('Finished getting %s images for %s', i, biz_name)
        log_file.close()
        return i
    else:
        logger.error('No photos found', exc_info=True)
        return 0

