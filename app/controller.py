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
            positive_image_counts, total_image_counts, names = model.score_location(location, limit, verbose)
            return render_template("location.html", location=location, scores=positive_image_counts, counts=total_image_counts, names=names)
    return render_template("location.html")
