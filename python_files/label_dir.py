import tensorflow as tf
import sys
import os
import shutil
from os import listdir
from os import mkdir
from shutil import copyfile
from os.path import isfile, join

def main(argv):
    """Function used to label all images in a directory

    Args:
        argv[1]: path to inmage directory
        argv[2]:  threshold above which to classify as art

    Returns:
        Returns two numbers:  # of latte art images, total # of images

    todo:
        make latteart directory a paramaeter
    """
  
    varPath = sys.argv[1]
    threshold = float(sys.argv[2])


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
        img_count = 0
        latte_count = 0
        for imageFile in imgFiles:
            image_data =  tf.gfile.FastGFile(varPath+"/"+imageFile, 'rb').read()       

            #print (imageFile)
            predictions = sess.run(softmax_tensor, \
                     {'DecodeJpeg/contents:0': image_data})
            
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            positive_score = round(predictions[0][1],2)
            if (positive_score > threshold):
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
        print('%s %s' % (latte_count,img_count))
        return latte_count, img_count


if __name__ == "__main__":
   main(sys.argv[1:])
