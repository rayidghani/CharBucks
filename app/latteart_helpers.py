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

API_KEY = os.environ.get('API_KEY')
if API_KEY:
    logger.debug('Loaded Yelp API Key %s', API_KEY)
else:
    logger.error('No environment variable set for Yelp API key - set API_KEY=XXX')

def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()
    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def, name='')
    return graph


def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
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
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    #Load label file and strip off carriage return
    label_lines = load_labels(model_dir + "retrained_labels.txt")
    logger.info('Loaded labels %s from %s', label_lines, model_dir)
    graph = tf.Graph()
    graph = load_graph(model_dir + "retrained_graph.pb")
    logger.info('Loaded tensorflow graph from %s', model_dir)

    with tf.Session(graph=graph) as sess:
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

    with tf.Session(graph=graph) as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')    
        total_image_count = 0
        positive_image_count = 0
        score_for_url_hash = {}
        for image_file in image_files:
            image_data = tf.gfile.FastGFile(image_file, 'rb').read()
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

def rank_bizs_in_location(location, num_of_businesses_to_get, model_dir, tmpimgdir, threshold):
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
    date_scored, num_positive_images, num_total_images = load_logs("bizscores.log")
    logger.info('Starting to get %s businesses in %s from Yelp', num_of_businesses_to_get, location)
    business_ids_list = yelp_helper.get_business_ids_from_api(location, num_of_businesses_to_get)
    
    # remove businesses with non ascii characters
    clean_business_ids =  [b for b in business_ids_list if is_ascii(b)]
    logger.info('Got %s businesses in %s', len(clean_business_ids), location)
    business_count = 0

    if len(clean_business_ids) > 0:
        biz_to_positive_image_count = {}  #store number of positive images for the business
        biz_to_total_image_count = {} # store total number of imageas retrieved for the business
        biz_to_name = {} # store the business name
        for bizid in clean_business_ids:
            bizresponse = yelp_helper.get_business(API_KEY, bizid)
            bizurl = 'http://www.yelp.com/biz/' + bizid
            bizname = bizresponse['name']
            bizalias = bizresponse['alias']
            #bizcoordinates = bizresponse['coordinates']
            logger.info('Processing %s', bizname)

            if bizid in date_scored:
                # if this business has already been scored earlier, skip it
                # todo: put time limit 
                positive_count = int(num_positive_images[bizid])
                img_count = int(num_total_images[bizid])
                logger.info('business %s already scored on %s with %s positive images', bizname, date_scored[bizid], positive_count)
                biz_to_positive_image_count[bizurl] = positive_count
                biz_to_total_image_count[bizurl] = img_count
                biz_to_name[bizurl] = bizname
            else:
                num_images = 0
                positive_count = 0
                logger.info('Getting images for id %s with name %s and putting them in %s', bizid, bizname, tmpimgdir)
                # check if we need to pass bizid or biz alias
                num_images = yelp_helper.get_business_images(bizalias, tmpimgdir)
                logger.info('Labeling %s images in directory %s with threshold %s', num_images, tmpimgdir, threshold)
                if num_images:
                    score_for_url, positive_count, img_count = label_directory(tmpimgdir, model_dir, threshold)
                else:
                    score_for_url, positive_count, img_count = 0
                
                biz_to_positive_image_count[bizurl]= positive_count
                biz_to_total_image_count[bizurl]= num_images
                biz_to_name[bizurl] = bizname
                
                # permanent logging
                with open("imgscores.log", "a+") as f:
                    for imgurl, score in score_for_url.items():
                        f.write(str(datetime.datetime.today().strftime('%Y-%m-%d')) + ',' + bizid + ',' + bizname + ',' + imgurl  + ','  + str(score) + '\n')      
                
                with open("bizscores.log", "a+", newline='') as f:
                    writer = csv.writer(f, delimiter=',')
                    line = [str(datetime.datetime.today().strftime('%Y-%m-%d')),bizid ,bizname , str(positive_count), str(img_count)]    
                    writer.writerow(line)
                    #f.write(str(datetime.datetime.today().strftime('%Y-%m-%d')) + ',' + biz + ',' + bizname + ',' + str(positive_count)  + ','  + str(img_count) + '\n')      
            business_count += 1
            logger.info('%s has %s out of %s arts', bizname, positive_count, img_count)
            logger.info('Processed %s out of %s businesses', business_count, len(clean_business_ids))
            
            if bizid not in date_scored:
                wait_time = random.randint(1, 5)
                logger.info('waiting %s seconds to process next business...',wait_time)
                time.sleep(wait_time)
        
        return biz_to_positive_image_count, biz_to_total_image_count, biz_to_name
    else:
        logger.error('No businesses returned by get_business_ids_from_api', exc_info=True)
        return 0;

def load_logs(bizlogfile):
    with open(bizlogfile, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        date_scored=dict()
        num_positive_images=dict()
        num_images=dict()

        for rows in csv_reader:
            date_scored[rows[1]]=rows[0]
            num_positive_images[rows[1]]=rows[3]
            num_images[rows[1]]=rows[4]
        logger.info('Loaded %s lines from log file', len(date_scored))

    return date_scored, num_positive_images, num_images


