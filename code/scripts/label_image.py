import tensorflow as tf
import sys

def main(argv):
    """Function used to label an image

    Args:
        argv[1]: path to image

    Returns:
        Returns a score 

    Todo:
        make latteart directory a paramaeter
        test with non jpeg images
    """
  
    image_path = sys.argv[1]

    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Load label file and strip off carriage return
    label_lines = [line.rstrip() for line 
                       in tf.gfile.GFile("latteart_model/retrained_labels.txt")]

    # Unpersist graph from file
    with tf.gfile.FastGFile("latteart_model/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
        
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        # Get prediction score for positive class
        positive_score = round(predictions[0][1],2)
        print positive_score
        return positive_score


        # code for printing out probability for both classes
        #for node_id in top_k:
        #    human_string = label_lines[node_id]
        #    score = predictions[0][node_id]
        #    print('%s (score = %.5f)' % (human_string, score))

if __name__ == "__main__":
   main(sys.argv[1:])
