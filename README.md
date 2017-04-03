# Latte Art Classifier

## Usage Instructions:

1. Install tensorflow (in a docker container) - 
2. Clone this repo
3. Start the docker container and mount the cloned repo directory
docker run -it -d -v ~/Projects/CharBucks/python_files/:/latteart/ -w /latteart --name="latte" rayid/tensorflow:image-class
4. Call various scripts locally or use the flask web app

## Local Scripts to use

* To label a single image by it's URL: label_web_image.sh URL_OF_IMAGE
* To get a score for a business: get_rating.sh YELP_BUSINESS_ID VERBOSE_OR_NOT (optional - 0 or 1)
* To get a score for the nearest k coffeeshops to a location: python get_business_ranking LOCATION NUMBER_OF_BUSINESSES_TO_GET

### To train or retrain:

python tensorflow/examples/image_retraining/retrain.py --bottleneck_dir=/latteart/bottlenecks --how_many_training_steps 4000 --model_dir=/latteart/inception --output_graph=/latteart/retrained_graph.pb --output_labels=/latteart/retrained_labels.txt --image_dir /latteart/data

### To label a single image locally

python label_image.py /latteart/images_to_label/Z.jpg

### To label a single image by url

./label_web_image.sh https://s3-media4.fl.yelpcdn.com/bphoto/opxgfR90CMeao7XY8_-2uQ/o.jpg

### To label a directory of images

python label_dir.py latteart/images_to_label/

### to label a yelp business by id

./get_rating.sh blue-bottle-coffee-los-angeles-17 latteart/images_to_label/

## Web App
