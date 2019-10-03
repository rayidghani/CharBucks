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


# top two functions not being used currenrly
def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()
    print(model_file)
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
    label_lines = [line.rstrip() for line 
                       in tf.gfile.GFile(model_dir + "retrained_labels.txt")]
    logger.info('Loaded labels %s from %s', label_lines, model_dir)

    # Unpersist graph from file
    with tf.gfile.FastGFile(model_dir + "retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    #load_labels_and_graph("retrained_labels.txt", "retrained_graph.pb")

    with tf.Session() as sess:
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
        Returns two numbers:  # of latte art images, total # of images

    todo:
        modify to work with non jpeg images
    """

    imgFiles = glob.glob(image_path+'/*.jpg')
    # load urls for each image
    url_file = image_path + '/log.txt'
    url_for_imgfile = dict(line.rstrip('\n').split(',') for line in open(url_file))
    
    #Load label file and strip off carriage return
    label_lines = load_labels(model_dir + "retrained_labels.txt")
    logger.info('Loaded labels %s from %s', label_lines, model_dir)
    graph = tf.Graph()
    graph = load_graph(model_dir + "retrained_graph.pb")

    #load_labels_and_graph("retrained_labels.txt", "retrained_graph.pb")

    with tf.Session(graph=graph) as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')    
        img_count = 0
        positive_count = 0
        score_for_url = {}
        output_list= []
        for imageFile in imgFiles:
            image_data = tf.gfile.FastGFile(imageFile, 'rb').read()
            predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            # Get prediction score for positive class
            positive_score = round(predictions[0][0],2)
            logger.info('Score for %s is %s', imageFile, positive_score)
            #positive_score = label_image(imageFile, model_dir)
            score_for_url[url_for_imgfile[os.path.basename(imageFile)]] = positive_score
            if (positive_score > threshold):
                positive_count+=1
            img_count += 1

        return score_for_url, positive_count, img_count




def label_directory_old(image_path, model_dir, threshold):
    """Function used to label all images in a directory

    Args:
        argv[1]: path to image directory
        argv[2]: model dir
        argv[3]: threshold above which to classify as art

    Returns:
        Returns two numbers:  # of latte art images, total # of images

    todo:
        modify to work with non jpeg images
    """

    imgFiles = glob.glob(image_path+'/*.jpg')
    # load urls for each image
    url_file = image_path + '/log.txt'
    url_for_imgfile = dict(line.rstrip('\n').split(',') for line in open(url_file))
    
    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line 
                       in tf.gfile.GFile(model_dir + "/retrained_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile(model_dir + "/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')    
        img_count = 0
        positive_count = 0
        score_for_url = {}
        output_list= []
        for imageFile in imgFiles:
            image_data = tf.gfile.FastGFile(imageFile, 'rb').read()
            predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            # Get prediction score for positive class
            positive_score = round(predictions[0][0],2)
            logger.info('Score for %s is %s', imageFile, positive_score)
            #positive_score = label_image(imageFile, model_dir)
            score_for_url[url_for_imgfile[os.path.basename(imageFile)]] = positive_score
            if (positive_score > threshold):
                positive_count+=1
            img_count += 1

        return score_for_url, positive_count, img_count
        
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def log_business():
    return 1

def rank_bizs_in_location(location, num_of_businesses_to_get, model_dir, tmpimgdir, threshold):
    """Function used to get scores for num_of_businesses_to_get businesses in a location

    Args:
        location: location (can be city, zip, lat long string)
        num_of_businesses_to_get: number of business to get and score

    Returns:
        Returns three arrays - positive_counts, total_counts, biz_names
    """

    if location is None:
        location = "chicago"

    logger.info("loading log file")
    datescored, numpositiveimages, numimages = load_logs("bizscores.log")
    logger.info('loaded %s lines from log file', len(datescored))

    logger.info('Starting to get %s businesses in %s from Yelp', num_of_businesses_to_get, location)
    all_bizids = yelp_helper.get_business_ids_from_api(location, num_of_businesses_to_get)
    
    # remove businesses with non ascii characters
    clean_bizids =  [b for b in all_bizids if is_ascii(b)]
    logger.info('Got %s businesses in %s', len(clean_bizids), location)
    biz_count = 0


    if len(clean_bizids) > 0:
        positive_counts = {}  #store number of positive images for the business
        total_counts = {} # store total number of imageas retrieved for the business
        biz_names = {} # store the business name
        for biz in clean_bizids:
            bizresponse = yelp_helper.get_business(API_KEY, biz)
            bizname = bizresponse['name']
            bizalias = bizresponse['alias']
            logger.info('Processing %s', bizname)
            bizurl = 'http://www.yelp.com/biz/' + biz

            if biz in datescored:
                # if this business has already been scored earlier, skip it
                # todo: put time limit 
                positive_count=int(numpositiveimages[biz])
                img_count=int(numimages[biz])
                logger.info('business %s already scored in %s %s', biz, datescored[biz], numpositiveimages[biz])
                positive_counts[bizurl]=positive_count
                total_counts[bizurl]= img_count
                biz_names[bizurl] = bizname
            else:
                bizresponse = yelp_helper.get_business(API_KEY, biz)
                bizname = bizresponse['name']
                logger.info('Processing %s', bizname)
                bizurl = 'http://www.yelp.com/biz/' + biz
                num_images = 0
                positive_count = 0
                logger.info('Getting images for id %s name %s and putting them in %s', biz, bizname, tmpimgdir)
                # check if we need to pass bizid or biz alias
                num_images = yelp_helper.get_business_images(bizalias, tmpimgdir)
                logger.info('Labeling %s images in directory %s with threshold %s', num_images, tmpimgdir, threshold)
                if num_images:
                    score_for_url, positive_count, img_count = label_directory(tmpimgdir, model_dir, threshold)
                else:
                    positive_count = 0
                
                positive_counts[bizurl]= int(positive_count)
                total_counts[bizurl]= num_images
                biz_names[bizurl] = bizname
                
                # permanent logging
                with open("imgscores.log", "a+") as f:
                    for imgurl, score in score_for_url.items():
                        f.write(str(datetime.datetime.today().strftime('%Y-%m-%d')) + ',' + biz + ',' + bizname + ',' + imgurl  + ','  + str(score) + '\n')      
                
                with open("bizscores.log", "a+", newline='') as f:
                    writer = csv.writer(f, delimiter=',')
                    line = [str(datetime.datetime.today().strftime('%Y-%m-%d')),biz ,bizname , str(positive_count), str(img_count)]    
                    writer.writerow(line)
                    #f.write(str(datetime.datetime.today().strftime('%Y-%m-%d')) + ',' + biz + ',' + bizname + ',' + str(positive_count)  + ','  + str(img_count) + '\n')      

            logger.info('%s has %s out of %s arts', bizname, positive_count, img_count)
            wait_time = random.randint(1, 5)
            biz_count += 1
            logger.info('Processed %s out of %s businesses', biz_count, len(clean_bizids))
            if biz not in datescored:
                logger.info('waiting %s seconds to process next business...',wait_time)
                time.sleep(wait_time)
        return positive_counts, total_counts, biz_names
    else:
        logger.error('No businesses returned by get_business_ids_from_api', exc_info=True)
        return 0;

def load_logs(bizlogfile):
    with open(bizlogfile, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        #{logger.info('%s %s %s %s', rows[0],rows[1],rows[2],rows[3], rows[4]) for rows in csv_reader}
        datescored=dict()
        numpositiveimages=dict()
        numimages=dict()

        for rows in csv_reader:
            datescored[rows[1]]=rows[0]
            numpositiveimages[rows[1]]=rows[3]
            numimages[rows[1]]=rows[4]
        logger.info('function loaded %s lines from log file', len(datescored))

    return datescored, numpositiveimages, numimages


