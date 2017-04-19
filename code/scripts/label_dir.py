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



def main(argv):
    """Function used to label all images in a directory

    Args:
        argv[1]: path to image directory
        argv[2]: model dir
        argv[3]:  threshold above which to classify as art
        argv[4]:  verbose

    Returns:
        Returns two numbers:  # of latte art images, total # of images

    todo:
        make latteart directory a paramaeter
        add argparse to pass arguments
    """

    varPath = sys.argv[1]
    model_dir = sys.argv[2]
    threshold = float(sys.argv[3])
    verbose = int(sys.argv[4])

    # testing new code
    #imgFiles = [f for f in listdir(varPath) if isfile(join(varPath, f))]
    imgFiles = glob.glob(varPath+'/*.jpg')

    # load urls for each image
    url_file = varPath + '/log.txt'
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
            # testing new code
            #image_data =  tf.gfile.FastGFile(varPath+"/"+imageFile, 'rb').read()   
            image_data =  tf.gfile.FastGFile(imageFile, 'rb').read()   

            #print (imageFile)
            predictions = sess.run(softmax_tensor, \
                     {'DecodeJpeg/contents:0': image_data})
            
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            positive_score = round(predictions[0][1],2)
            if (positive_score > threshold):
                positive_count+=1
                score_for_url[url_for_imgfile[os.path.basename(imageFile)]] = positive_score
                if verbose:
                    output_list.append ('%s*%s' % (url_for_imgfile[os.path.basename(imageFile)],positive_score))



            img_count += 1

        if verbose:
            #return_string = '[\'fsfsdfdsd\',\'dfgdgdfg\']' 
            return_string = "^".join(output_list)
            #return_string = "[" + return_string + "]"
            #return_string = "[[" + return_string + "]," + "[" + str(positive_count) + "," + str(img_count) + "]]"
            print return_string
            return score_for_url, positive_count, img_count
        else:
            print('%s %s' % (positive_count,img_count))
            return positive_count, img_count
            

if __name__ == "__main__":
   main(sys.argv[1:])
