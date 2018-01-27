from flask import render_template, request, url_for, jsonify
from app import app, model
from flask import Flask, request

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")

@app.route('/url', methods=['POST', 'GET'])
def classify_image_url():
    if request.method == 'POST':
        posttext = request.form['posttext']
        if posttext is not "":
            result = model.score_imageurl(posttext)
            print(result)
            return render_template("url.html", results=result)
    return render_template("url.html")

@app.route('/bizid', methods=['POST', 'GET'])
def classify_bizid():
    if request.method == 'POST':
        posttext = request.form['posttext']
        if request.form.get("verbose"):
            verbose = 1
        else:
            verbose = 0
        if posttext is not "":
            positive_count, img_count, score_for_url = model.score_yelpbiz(posttext,verbose)
            return render_template("bizid.html", positive_count=positive_count, img_count=img_count, score_for_url=score_for_url)
    return render_template("bizid.html")

@app.route('/location', methods=['POST', 'GET'])
def classify_location():
    if request.method == 'POST':
        posttext = request.form['posttext']
        if request.form.get("verbose"):
            verbose = 1
        else:
            verbose = 0
        limit = request.form['limit']
        if posttext is not "":
            scores, counts = model.get_biz_scores_from_location(posttext, limit, verbose)
            return render_template("location.html", scores=scores, counts=counts)
    return render_template("location.html")
