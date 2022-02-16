from __future__ import absolute_import
import tensorflow as tf
import sys
import os
import shutil
from os import listdir
from os import mkdir
from shutil import copyfile
from os.path import isfile, join
import glob
import argparse
import logging
import subprocess
import time
import random
import urllib3
import  datetime
import csv
from . import yelp_helper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

YELP_API_KEY = os.environ.get('YELP_API_KEY')
if YELP_API_KEY:
    logger.debug('Loaded Yelp API Key %s', YELP_API_KEY)
else:
    logger.error('No environment variable set for Yelp API key - export YELP_API_KEY=XXX')


model_dir = 'latteart_model_files/'
data_dir = 'data/'
imgdir ='latteart-images/'
threshold = 0.6
bizlogfile=data_dir+'bizscores.log'
imglogfile=data_dir+'imgscores.log'
locationfile=data_dir+'locations.txt'



def load_graph(model_file):
    graph = tf.Graph()
    # graph_def = tf.GraphDef()
    graph_def = tf.compat.v1.GraphDef()
    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def, name='')
    return graph


def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.io.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label

def label_image(image_path, model_dir):
    """Function used to label an image

    Args:
        argv[1]: path to image
        argv[2]: difrectory where trained model is stored

    Returns:
        Returns a score for the image

    Todo:
        test with non jpeg images
    """

    # Read in the image_data
    image_data = tf.io.gfile.GFile(image_path, 'rb').read()

    #Load label file and strip off carriage return
    label_lines = load_labels(model_dir + "retrained_labels.txt")
    logger.info('Loaded labels %s from %s', label_lines, model_dir)
    graph = tf.Graph()
    graph = load_graph(model_dir + "retrained_graph.pb")
    logger.info('Loaded tensorflow graph from %s', model_dir)

    # with tf.Session(graph=graph) as sess:
    with tf.compat.v1.Session(graph=graph) as sess:

        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')        
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
        logger.info('predictions are %s', predictions)
      
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        # Get prediction score for positive class - round to 2 decimals
        positive_score = round(predictions[0][0],2)
        logger.info('Score is %s', positive_score)
        return positive_score

        # code for printing out probability for both classes
        #for node_id in top_k:
        #    human_string = label_lines[node_id]
        #    score = predictions[0][node_id]
        #    print('%s (score = %.5f)' % (human_string, score))

def label_directory(image_path, model_dir, threshold):
    """Function used to label all images in a directory

    Args:
        argv[1]: path to image directory
        argv[2]: model dir
        argv[3]: threshold above which to classify as art

    Returns:
        Returns dictionary of url,score for each image,
         # of latte art images, total # of images

    todo:
        modify to work with non jpeg images
    """
    # todo: add support for  non jpg images
    image_files = glob.glob(image_path+'/*.jpg')
    # load urls for each image
    tmplogfile = image_path + '/tmplog.txt'
    url_for_image_hash = dict(line.rstrip('\n').split(',') for line in open(tmplogfile))
    
    #Load label file and strip off carriage return
    label_lines = load_labels(model_dir + "retrained_labels.txt")
    logger.info('Loaded labels %s from %s', label_lines, model_dir)
    graph = tf.Graph()
    graph = load_graph(model_dir + "retrained_graph.pb")
    logger.info('Loaded tensorflow graph from %s', model_dir)

    with tf.compat.v1.Session(graph=graph) as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')    
        total_image_count = 0
        positive_image_count = 0
        score_for_url_hash = {}
        for image_file in image_files:
            image_data = tf.io.gfile.GFile(image_file, 'rb').read()
            predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            # Get prediction score for positive class
            positive_score = round(predictions[0][0],2)
            logger.info('Score for %s is %s', image_file, positive_score)
            #positive_score = label_image(imageFile, model_dir)
            score_for_url_hash[url_for_image_hash[os.path.basename(image_file)]] = positive_score
            if (positive_score > threshold):
                positive_image_count+=1
            total_image_count += 1

        return score_for_url_hash, positive_image_count, total_image_count
        
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def rank_bizs_in_location(location, num_of_businesses_to_get, offset, model_dir, tmpimgdir, threshold):
    """Function used to get scores for num_of_businesses_to_get businesses in a location

    Args:
        location: location (can be city, zip, lat long string)
        num_of_businesses_to_get: number of business to get and score

    Returns:
        Returns three dicts - positive_counts, total_counts, biz_names
    """

    if location is None:
        location = "chicago"

    logger.info('Loading log file for historically scored businesses')
    date_scored, num_positive_images, num_total_images, name, latitude, longitude, alias, city, state, rating, numreviews = load_bizlog(bizlogfile)
    logger.info('Starting to get %s businesses in %s from Yelp', num_of_businesses_to_get, location)
    business_ids_list = yelp_helper.get_business_ids_from_api(location, num_of_businesses_to_get, offset)
    
    # remove businesses with non ascii characters
    if business_ids_list:
        clean_business_ids =  [b for b in business_ids_list if is_ascii(b)]
        logger.info('Got %s businesses in %s', len(clean_business_ids), location)
        business_count = 0

        if len(clean_business_ids) > 0:
            biz_to_positive_image_count = {}  #store number of positive images for the business
            biz_to_total_image_count = {} # store total number of images retrieved for the business
            biz_to_name = {} # store the business name
            biz_to_alias = {}
            biz_to_city = {}
            biz_to_state = {}
            biz_to_latitude = {} 
            biz_to_longitude = {} 
            biz_to_rating = {}
            biz_to_numreviews = {}

            for bizid in clean_business_ids:
                bizurl = 'http://www.yelp.com/biz/' + bizid
                # loop over each business
                if bizid in date_scored:
                # if (bizid in date_scored() and (date_scored[bizid] > datetime.now() - timedelta(months=6))
                    # if this business has already been scored earlier, skip it
                    # todo: put time limit 
                    logger.info('business %s already scored on %s', name[bizid], date_scored[bizid])

                    # fill dictionaries for this location
                    biz_to_positive_image_count[bizurl] = int(num_positive_images[bizid])
                    biz_to_total_image_count[bizurl] = int(num_total_images[bizid])
                    biz_to_name[bizurl] = name[bizid]
                    biz_to_latitude[bizurl] = latitude[bizid]
                    biz_to_longitude[bizurl] = longitude[bizid]
                    biz_to_alias[bizurl] = alias[bizid]
                    biz_to_city[bizurl] = city[bizid]
                    biz_to_state[bizurl] = state[bizid]
                    biz_to_rating[bizurl] = rating[bizid]
                    biz_to_numreviews[bizurl] = numreviews[bizid]

                else:
                    # this business has not been scored before
                    bizresponse = yelp_helper.get_business(YELP_API_KEY, bizid)
                    logger.info("Processing url %s", bizurl)
                    try:
                        biz_to_name[bizurl] = bizresponse['name']
                        biz_to_alias[bizurl]  = bizresponse['alias']
                        biz_to_latitude[bizurl] = bizresponse['coordinates']['latitude']
                        biz_to_longitude[bizurl] = bizresponse['coordinates']['longitude']
                        biz_to_city[bizurl] = bizresponse['location']['city']
                        biz_to_state[bizurl]  = bizresponse['location']['state']
                        biz_to_rating[bizurl]  = bizresponse['rating']
                        biz_to_numreviews[bizurl] = bizresponse['review_count']
                        logger.info('got data for %s', biz_to_name[bizurl])

                        num_images = 0
                        positive_count = 0
                        logger.info('Getting images for id %s with name %s and putting them in %s', bizid, bizresponse['name'], tmpimgdir)
                        # todo: check if we need to pass bizid or biz alias
                        num_images = yelp_helper.get_business_images(bizresponse['alias'], tmpimgdir)
                        logger.info('Labeling %s images in directory %s with threshold %s', num_images, tmpimgdir, threshold)
                        if num_images:
                            # if we found photos we can now score them
                            score_for_url, positive_count, img_count = label_directory(tmpimgdir, model_dir, threshold)
                        else:
                            # no images found in yelp
                            score_for_url = {} 
                            img_count = 0 
                        biz_to_positive_image_count[bizurl]= positive_count
                        biz_to_total_image_count[bizurl]= num_images

                        # permanent logging for both images/urls and businesses
                        with open(imglogfile, "a+") as f:
                            imglogwriter = csv.writer(f, delimiter=',')
                            for imgurl, score in score_for_url.items():
                                #todo: make it a csv writer
                                line = [str(datetime.datetime.today().strftime('%Y-%m-%d')),bizid ,bizresponse['name'] , imgurl, str(score)]
                                imglogwriter.writerow(line)
                                #f.write(str(datetime.datetime.today().strftime('%Y-%m-%d')) + ',' + bizid + ',' + bizresponse['name'] + ',' + imgurl  + ','  + str(score) + '\n')      
                        
                        with open(bizlogfile, "a+", newline='') as f:
                            bizlogwriter = csv.writer(f, delimiter=',')
                            #todo: fix
                            line = [str(datetime.datetime.today().strftime('%Y-%m-%d')),bizid ,bizresponse['name'] , str(positive_count), str(img_count), bizresponse['location']['city'], bizresponse['location']['state'], bizresponse['coordinates']['latitude'], bizresponse['coordinates']['longitude'],bizresponse['alias'],bizresponse['rating'],bizresponse['review_count']]    
                            bizlogwriter.writerow(line)
                            #todo: write alias, city, state
                            #f.write(str(datetime.datetime.today().strftime('%Y-%m-%d')) + ',' + biz + ',' + bizname + ',' + str(positive_count)  + ','  + str(img_count) + '\n')      
                        logger.info('%s has %s out of %s arts', bizresponse['name'], positive_count, img_count)
                    except KeyError:
                        logger.info('key error processing %s', bizresponse)

                business_count += 1
                logger.info('Processed %s out of %s businesses in %s', business_count, len(clean_business_ids), location)
                        
                        # if this was a new business and crawled, wait and go to the next one
                if bizid not in date_scored:
                    wait_time = random.randint(1, 5)
                    logger.info('waiting %s seconds to process next business...',wait_time)
                    time.sleep(wait_time)
                
            return biz_to_positive_image_count, biz_to_total_image_count, biz_to_name, biz_to_latitude, biz_to_longitude
    else:
        logger.error('No businesses returned by get_business_ids_from_api', exc_info=True)
        return 0;

def load_bizlog(bizlogfile):
    # 2019-10-16,RorY8SkHmDztoyazx_TgPg,LDU Coffee,32,54,Dallas,TX,32.81444,-96.78511,ldu-coffee-dallas,5.0,203
    # date, id, name, pos, total, city, state, lat, long, alias, rating, numreviews
    with open(bizlogfile, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        date_scored=dict()
        num_positive_images=dict()
        num_images=dict()
        name=dict()
        alias=dict()
        latitude=dict()
        longitude=dict()
        city=dict()
        state=dict()
        rating=dict()
        numreviews=dict()

        for biz in csv_reader:
            date_scored[biz[1]]=biz[0]
            name[biz[1]]=biz[2]
            num_positive_images[biz[1]]=int(biz[3])
            num_images[biz[1]]=int(biz[4])
            city[biz[1]]=biz[5]
            state[biz[1]]=biz[6]
            latitude[biz[1]]=biz[7]
            longitude[biz[1]]=biz[8]
            alias[biz[1]]=biz[9]
            rating[biz[1]]=biz[10]
            numreviews[biz[1]]=int(biz[11])

        logger.info('Loaded %s lines from log file %s', len(date_scored),bizlogfile)

    return date_scored, num_positive_images, num_images, name, latitude, longitude, alias, city, state, rating, numreviews


