from flask import render_template, request, url_for, jsonify
from app import app, model
from flask import Flask, request

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")

@app.route('/url', methods=['POST', 'GET'])
def classify_image_url():
    if request.method == 'POST':
        url = request.form['url']
        if url is not "":
            result = model.score_imageurl(url)
            return render_template("url.html", results=result)
    return render_template("url.html")

@app.route('/bizid', methods=['POST', 'GET'])
def classify_bizid():
    if request.method == 'POST':
        yelpalias = request.form['yelpalias']
        if request.form.get("verbose"):
            verbose = 1
        else:
            verbose = 0
        if yelpalias is not "":
            positive_image_count, total_image_count, url_to_score_hash = model.score_yelpbiz(yelpalias, verbose)
            return render_template("bizid.html", positive_image_count=positive_image_count, total_image_count=total_image_count, url_to_score_hash=url_to_score_hash)
    return render_template("bizid.html")

@app.route('/location', methods=['POST', 'GET'])
def classify_location():
    if request.method == 'POST':
        location = request.form['location']
        if request.form.get("verbose"):
            verbose = 1
        else:
            verbose = 0
        limit = request.form['limit']
        if location is not "":
            positive_image_counts, total_image_counts, names, latitudes, longitudes = model.score_location(location, limit, verbose)
            return render_template("location.html", location=location, scores=positive_image_counts, counts=total_image_counts, names=names, latitudes = latitudes, longitudes = longitudes)
    return render_template("location.html")

@app.route('/offlinelocation', methods=['POST', 'GET'])
def retrieve_location_offline():
    if request.method == 'POST':
        location = request.form['location']
        if request.form.get("verbose"):
            verbose = 1
        else:
            verbose = 0
        limit = request.form['limit']
        if location is not "":
            positive_image_counts, total_image_counts, names, latitudes, longitudes = model.offline_location(location, limit, verbose)
            return render_template("offlinelocation_nomap.html", location=location, scores=positive_image_counts, counts=total_image_counts, names=names, latitudes = latitudes, longitudes = longitudes)
    return render_template("offlinelocation_nomap.html")


@app.route('/location2', methods=['POST', 'GET'])
def classify_location2():
    if request.method == 'POST':
        location = request.form['location']
        if request.form.get("verbose"):
            verbose = 1
        else:
            verbose = 0
        limit = request.form['limit']
        if location is not "":
            positive_image_counts, total_image_counts, names, latitudes, longitudes = model.score_location(location, limit, verbose)
            return render_template("location-exp.html", location=location, scores=positive_image_counts, counts=total_image_counts, names=names, latitudes = latitudes, longitudes = longitudes)
    return render_template("location-exp.html")


@app.route('/browse', methods=['POST', 'GET'])
def browse():
#    a, positive_image_counts, total_image_counts, names, latitudes, longitudes = model.browse()
    dates, positive_image_counts, total_image_counts, names, latitudes, longitudes, aliases, cities, states, ratings, numreviewslist = model.browse()
    if request.method == 'POST':
        location = request.form['location']
        zoom = 10

    else:
        location = '41.881832, -87.623177'
        zoom = 1
    return render_template("browse.html", location=location, zoom=zoom, scores=positive_image_counts, counts=total_image_counts, names=names, latitudes = latitudes, longitudes = longitudes)


@app.route('/batch', methods=['POST', 'GET'])
def batch():
    if request.method == 'POST':
       offset = request.form['offset']
       start = request.form['start']
       positive_image_counts, total_image_counts, names = model.batch(start,offset)
       return render_template("batch.html")
    return render_template("batch.html")

