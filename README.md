# About

All of us coffeesnobs have been there. You go to a new city and need to find the nearest (or not so nearest) place to get your coffee. The Charbucks around the corner is definitely not an option. You turn to Yelp and find the local 4.5 star coffeeshop. It has friendly baristas, lot of seating, free wifi, but can you trust the baristas to know how to make a good espresso or cappuccino? Yes they have the La Marzocco machine up front, and Stumptown or Intelligentsia beans on display but then you hear the sound of milk being destroyed while being steamed and you know you're in the wrong place. You go back to Yelp, read some more reviews of other nearby places, look through the photos to see if any of them can do decent latteart, but are quickly running out of patience and time.  This is where the magic of machine learning comes in.

![goodart](https://wallpapercave.com/wp/wp5513240.png)


# Latte Art Classifier

After working on numerous projects in health, criminal justice, education, energy, workforce development, and social services, I realized that the area of social good I was missing from my portfolio was helping the world find good coffee. This of course ranked right below finding yet another way for restaurants to deliver food to hungry customers to make the world a better place.

### Problem Definition:

A 1% problem I face when I go to a new city is to find good coffee (I'm an espresso/cappucino person so I'll focus on that). Of course I ask friends for recommendations, read through numerous coffee forums, or browse countless Yelp reviews. All of these approaches take time and have their shortcomings. My friends may not share my taste in coffee. Coffee forums don't usually have good coverage across cities. Yelp reviews require careful reading and filtering to dig up the good recommendations from the mass recommendations. 

Over the years, I've usually found a good heuristic for finding decent coffeeshops - if their baristas can produce good latte art, that's a proxy for having well-trained baristas which in turn is a good proxy for decent espresso/cappucino.

### Existing Approaches:

How do I find coffeeshops that have baristas that can produce good latte art? I start with Yelp, and then browse through photos of coffee drinks to pick out ones that have espresso and milk based drinks and scroll to get a sense of which ones have decent latte art. I do this for a number of coffeeshops in a given city or neighborhood and use that to decide whewre to go. This process works pretty well but is extremely time consuming. 

### My Approach:

About a year and a half ago, I was in LA in my hotel room, the night before a meeting. Since my meeting wasn't until 11am, I thought I had time to get some good coffee. Of course I had recommendations from a couple of friends but those recommendations weren't near where I was staying (it's LA after all). I started my usual search process and realized that I may be able to use the magic of AI and deep learning to make the world a better place (hopefully by now you're getting the cynicism when I use that phrase).

### What I built:

In the next couple of hours, I ended up building a fairly simple app that automated what I was doing manually (don't worry, it's not going to make any jobs obsolete - for now). I did a google image search for "good latte art" and downloaded a couple of hundred images. I did another search for "bad latte art" and downloaded a couple of hundred images. I scanned through those images and deleted ones I didn't think matched my search. I then trained a neural network using tensorflow to differentiate between good and bad latte art photos. Now that I had a good classifier, here's how i built my app:

1. I wrote a script to find nearby coffeeshops from Yelp based on where I was.
2. For each coffeeshop, I downloaded a handful of photos that people had taken of their drinks.
3. I ran these images against my classifier and counted the number of images that were classified as "good".
4. I then ranked the coffeeshoips based on that score .

### Results:

Great so far (at least for me). I've been using this app for the last 18 months and have been very happy with my validation results over over 30 cities. I've done a "field trial" by sampling from the list and have found that when the app scores a coffeeshop as high, it does give me good coffee. Of course it may miss good coffeeshops but for now i'm ok with that. For the machine learners, I've validated it for both precision and recall (and most importantly my satisfaction) and found it to be fairly high, compared to both a random baseline and "going to popular coffeeshops" baseline. 


### Limitations:
I'm using latte art as a proxy for good coffee which works 	out ok for me but may not aklways generalize. Since I only care about getting good espresso/cappuccino/flat whites, this may not work with pourovers. Of course it's pretty easy to game by faking the photos.

### Future Work:

All the code is here so feel free to use, modify, improve it.

### How can you try it?
Unfortunately Yelp does not allow getting photos of business from it's API so i can't deploy it on a cloud server without getting blocked. To try it, you'll either have to install it locally or ...


# Uses tensorflow to classify an image into latte art or not.

The web app can:
1. Label an image from a URL 
2. Label a yelp business from their Yelp ID
3. Give top k latte art coffeeshops given a location (zipcode, lat long, city, etc.)

## Set up for deploying to heroku

Currently deployed (not very stable state) at https://charbucks.herokuapp.com/ 

## Usage Instructions:

Note: Use python 3.6 and not 3.7 (since tensorflow hasn't been updated to support 3.7 yet)

1. Create virtualenv (virtualenv -p python3.6 charapp)
2. If the virtualenv is already created, source charapp/bin/activate
3. Clone this repo
4. pip install -r requirements.txt (will install tensorflow locally)
5. Get a [yelp api key] (https://www.yelp.com/developers/documentation/v3/get_started) and set environment variable (export API_KEY=XXXXX)
5. Call various scripts locally or use the flask web app (python run.py) or run latteart.sh (sources into the virtualenv, runs the webapp, and opens the local browser)

### To train or retrain:

1. Update training images in model_trainer/latteart_model/data. There are two directories - art and notart. You can add/remove/modify images in those directories and then retrain the model
2. retrain using train.sh (it calls retrain.py)

### To test locally on your machine

Use "python label_image.py imagepath" to test locally

## Structure of the code

### Web App

* Classify an image on the web
Input: Image URL, Tensorflow Model
Output: Latte Art Score
	1. Download Image
	2. Classify with pre-trained neural network
	3. Get prediction score

* Score a Yelp business
Input: Yelp businees ID, Tensorflow Model
	1. Download first 30 images of the business from Yelp
	2. Classify each image with the pre-trained neural network
	3. Get prediction score for each image
	4. Return number (or percentage) of images with score > threshold (currently 0.6)

* Get top k coffeeshops in a location
Input: Location (zip, lat long, address, city), number of coffeeshops to return 
	1. Query Yelp api for k coffeeshops in the location
	2. For each business, download first 30 images of the business from Yelp
	3. Classify each image with pre-trained neural network
	4. Get prediction score for each image
	5. Score business with number (or percentage) of images with score > threshold (currently 0.6)
	6. Return ranked list of businesses


# To Do:
1. store persistent logs on s3
2. config file


