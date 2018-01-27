# Latte Art Classifier

Uses tensorflow to classify an image into latte art or not.

The web app can:
1. Label an image 
2. Label a yelp business
3. Give top k latte art coffeeshops given a location (zipcode, lat long, city, etc.)

## Usage Instructions:

1. create virtualenv (virtualenv charapp)
2. if it's already created, source charapp/bin/activate
3. Clone this repo
4. pip install -r requirements.txt (will install tensorflow locally)
5. Call various scripts locally or use the flask web app (gunicorn -c config.py --bind 0.0.0.0:5000 wsgi)

### To train or retrain:

python tensorflow/examples/image_retraining/retrain.py --bottleneck_dir=/latteart/bottlenecks --how_many_training_steps 4000 --model_dir=/latteart/inception --output_graph=/latteart/retrained_graph.pb --output_labels=/latteart/retrained_labels.txt --image_dir /latteart/data
