import tensorflow as tf
import sys

# change this as you see fit
#image_path = sys.argv[1]

# Read in the image_data
#image_data = tf.gfile.FastGFile(image_path, 'rb').read()
import os
import shutil
from os import listdir
from os import mkdir
from shutil import copyfile
from os.path import isfile, join
varPath = sys.argv[1]
imgFiles = [f for f in listdir(varPath) if isfile(join(varPath, f))]


# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("latteart/retrained_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("latteart/retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    #try:
    #    shutil.rmtree(destDir)
    #except:
    #    None
    #mkdir ('scanned')
    
    img_count = 0
    latte_count = 0
    for imageFile in imgFiles:
        image_data =  tf.gfile.FastGFile(varPath+"/"+imageFile, 'rb').read()       

        print (imageFile)
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
        
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        positive_score = round(predictions[0][1],2)
        if (positive_score > 0.6):
            latte_count+=1
        #firstElt = top_k[0];
        #human_string = label_lines[firstElt]
        #score = predictions[0][firstElt]
        #print('%s %s (score = %.5f)' % (firstElt, human_string, score))
        #if (firstElt == 1 and score > 0.5) or (firstElt == 0 and score < 0.65):
        #    latte_count +=1
            #print imageFile
 	img_count += 1

    #print('total images = %s' % (img_count))
    #print('latte images = %s' % (latte_count))
    print latte_count img_count
