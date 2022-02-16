from __future__ import absolute_import
import sys
import os
import argparse
import logging
import subprocess
import time
import random
import  datetime
from . import latteart_helpers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

YELP_API_KEY = os.environ.get('YELP_API_KEY')
if YELP_API_KEY:
    logger.debug('Loaded Yelp API Key %s', YELP_API_KEY)
else:
    logger.error('No environment variable set for Yelp API key - export YELP_API_KEY=XXX')

#todo: read from config file

model_dir = 'latteart_model_files/'
data_dir = 'data/'
imgdir ='latteart-images/'
threshold = 0.6
bizlogfile=data_dir+'bizscores.log'
imglogfile=data_dir+'imgscores.log'
locationfile=data_dir+'locations.txt'

def load_locations(locationfile):
    with open(locationfile, mode='r') as f:
        locations = f.read().splitlines()
        logger.info('Loaded %s locations', len(locations))
    return locations

def batch_process_locations(locationfile, start, offset):
    logger.info('Loading log file for historically scored businesses')
    date_scored, num_positive_images, num_total_images, name, latitude, longitude, alias, city, state, rating, numreviews = latteart_helpers.load_bizlog(bizlogfile)

    locations = load_locations(locationfile)
    # start = 0 for default
    end = len(locations)
    for l in locations[int(start):end]:
        latteart_helpers.rank_bizs_in_location(l, 50, offset, model_dir, imgdir, threshold)
        wait_time = 1
        logger.info('waiting %s seconds to process next location...', wait_time)
        time.sleep(wait_time)






