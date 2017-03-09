# Latte Art Classifier

## Usage Instructions:

1. Install tensorflow (in a docker container)
2. Clone this repo
3. label_web_image.sh URL_OF_IMAGE


## To train or retrain:

python tensorflow/examples/image_retraining/retrain.py --bottleneck_dir=/latteart/bottlenecks --how_many_training_steps 4000 --model_dir=/latteart/inception --output_graph=/latteart/retrained_graph.pb --output_labels=/latteart/retrained_labels.txt --image_dir /latteart/data

## To label a single image locally

python label_image.py /latteart/images_to_label/Z.jpg

## To label a single image by url

./label_web_image.sh https://s3-media4.fl.yelpcdn.com/bphoto/opxgfR90CMeao7XY8_-2uQ/o.jpg

## To label a directory of images

python label_dir.py latteart/images_to_label/

## to label a yelp business by id

./get_rating.sh blue-bottle-coffee-los-angeles-17 latteart/images_to_label/

