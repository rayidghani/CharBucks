# Latte Art Classifier

After working on numerous projects in health, criminal justice, education, energy, workforce development, and social services, I realized that the most social good i can do is to help the world find good coffeeshops. This of course ranked right below finding yet another way for restaurants to deliver food to hungry customers to make the world a better place.

Problem Definition:
A 1% problem I face when I go to a new city is to find a good coffeeshop. Of course you can ask friends, read through coffee forums, or browse yelp reviews. All of them have their shortcomings and take time. I've usually found a good heuristic for finding decent coffeeshops - if their baristias can produce good latte art, that's a high precision proxy for having well-trained baristas which in turn is a good proxy for decent espressos/cappucinos.


Existing Approaches:
How do I find coffeeshops that has baristas that can produce good latte art? I start with Yelp, and then browse through photos of coffee cups to pick out ones that have espresso and milk based drinks and scan them to get a sense of which ones have decent latte art. I do this for a number of coffeeshops in a given city or neighborhood and use that to decide whewre to go. This process works pretty well but is time consuming. 

New Approach:
About a year and a hlaf ago, I was in LA in my hotel room, the night before a meeting. Since my meeting wasn't until 11am, I thought I had time to get come good coffee. Of course i had recommendations from a friend but those recommendations weren't near where i was staying (it's LA after all). I started my usual search process and realized that I may be able to use the magic of AI and deep learning to make the world a better place (hopefully by now you're getting the cynicism when I use that phrase).

What I built:
In the next couple of hours, I ended up building a fairly simple app that automated what i was doing manually. I did an image search for "good latte art" and downloaded a couple of hundred images. i did another search for "bad latte art" and downloaded a couple of hundred images. I scanned throufgh those images and filtered ones i didn't think matched my search. I then trained footnote a neural network to differentiate between good and bad latte art photos which worked pretty well. Now that i had a good classifier, here's what i did:

1. I wrote a script to find nearby coffeeshops from yelp
2. For each coffeeshops, i downloaded a handful of photos that people had taken of their drinks
3. I ran these images againszt my classifier and counted the # of images that were claxsified as "good"
4. I then ranked the coffeeshoips based on that score 

Results:
I've been using this app for the last 18 months and have been enormously happy with my validaiton results. I've done a field trial by sampling from the list and have found both the precision and recall to be fairly high, compared to both a random baseline and "popularity" baseline. Of course, this is based on my personal tests

Limitations:


Future Work:
All the code is here so feel free to use, modify, improve it.





Uses tensorflow to classify an image into latte art or not.

The web app can:
1. Label an image from a URL 
2. Label a yelp business from their Yelp ID
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
	4. Return number (or percentage) of images with score > threshold (currently 0.6)

* Get top k coffeeshops in a location
Input: Location (zip, lat long, address, city), number of coffeeshops to return 
	1. Query yelp api for k coffeeshops in the location
	2. For each business, download first 30 images of the business from Yelp
	3. Classify each image with pre-trained neural network
	4. Get prediction score for each image
	5. Score business with number (or percentage) of images with score > threshold (currently 0.6)
	6. Return ranked list of businesses






