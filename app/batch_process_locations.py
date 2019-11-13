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
imgdir ='images/'
threshold = 0.6


def load_locations(locationfile):
    with open(locationfile, mode='r') as f:
        locations = f.read().splitlines()
        logger.info('Loaded %s locations', len(locations))
    return locations

def batch_process_locations(locationfile, offset):

    logger.info('Loading log file for historically scored businesses')
    date_scored, num_positive_images, num_total_images = latteart_helpers.load_logs("bizscores.log")
    locations = load_locations(locationfile)
    for l in locations:
        latteart_helpers.rank_bizs_in_location(l, 50, offset, model_dir, imgdir, threshold)
        wait_time = 1
        logger.info('waiting %s seconds to process next location...', wait_time)
        time.sleep(wait_time)






