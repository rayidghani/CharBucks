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
5. Call various scripts locally or use the flask web app (python run.py)

### To train or retrain:

1. update training images in model_trainer/latteart_model/data. There are two directories - art and notart. You can modify images in those directories and then retrain the model
2. retrain using train.sh (it calls retrain.py)

### To test locally

Use "python label_image.py imagepath" to test locally
