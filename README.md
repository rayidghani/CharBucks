# Latte Art Classifier

Uses tensorflow to classify an image into latte art or not.

The web app can:
1. Label an image 
2. Label a yelp business
3. Give top k latte art coffeeshops given a location (zipcode, lat long, city, etc.)

## Set up for deploying to heroku

Currently deployed at https://charbucks.herokuapp.com/

## Usage Instructions:

Note: Use python 3.6 and not 3.7 (since tensorflow hasn't been updated to support 3.7 yet)

1. Create virtualenv (virtualenv -p python3.6 charapp)
2. If the virtualenv is already created, source charapp/bin/activate
3. Clone this repo
4. pip install -r requirements.txt (will install tensorflow locally)
5. Get a [yelp api key] (https://www.yelp.com/developers/documentation/v3/get_started) and set environment variable (export API_KEY=XXXXX)
5. Call various scripts locally or use the flask web app (python run.py) or run latteart.sh (sources into the virtualenv, runs the webapp, and opens the local browser)

### To train or retrain:

1. update training images in model_trainer/latteart_model/data. There are two directories - art and notart. You can modify images in those directories and then retrain the model
2. retrain using train.sh (it calls retrain.py)

### To test locally

Use "python label_image.py imagepath" to test locally

## Structure

### Web App

* Classify an image on the web
Input: Image URL, Tensorflow Model
Output: Score
	1. Download Image
	2. Classify with pre-trained neural network
	3. Get prediction score

* Classify a Yelp business
Input: Yelp businees id, Tensorflow Model
	1. Download first 30 images of the business from Yelp
	2. Classify each image with pre-trained neural network
	3. Get prediction score for each image
	4. Return number (or percentage) of images with score > threshold (curreny 0.6)

* Get top k coffeeshops in a location
Input: Location (zip, lat long, address, city), number of coffeeshops to return 
	1. Query yelp api for k coffeeshops in the location
	2. For each business, download first 30 images of the business from Yelp
	3. Classify each image with pre-trained neural network
	4. Get prediction score for each image
	5. Score business with number (or percentage) of images with score > threshold (curreny 0.6)
	6. Return ranked list of businesses






