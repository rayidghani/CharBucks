
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
import csv

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

    logger.info('Querying %s with headers %s and url params %s ...', url, headers, url_params)

    response = requests.request('GET', url, headers=headers, params=url_params, verify=False)
    logger.debug('querying returned json %s',response.json())
    return response.json()


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)


def load_logs(bizlogfile):
    with open(bizlogfile, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        bizids = []
        for biz in csv_reader:
            bizids.append(biz[1])
    return bizids

def load_ratings(ratingfile):
    with open(ratingfile, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        ratings = {}
        for row in csv_reader:
            ratings[row[0]]=1
    return ratings


def main():
    bizids = load_logs('../bizscores.log')
    ratings = load_ratings('../bizratings.log')
    with open("../bizratings.log", "a+") as f:
        for bizid in bizids:
            if not(bizid in ratings):
                bizresponse = get_business(YELP_API_KEY, bizid)
                try:
                    bizrating = bizresponse['rating']
                    bizreviewcount = bizresponse['review_count']
                    f.write(bizid + ',' + str(bizrating) + ',' + str(bizreviewcount) + '\n')      
                    logger.info('for %s %s %s', bizid, bizrating, bizreviewcount)
                except KeyError:
                    logger.info('key error processing %s', bizresponse)

  
if __name__== "__main__":
  main()

