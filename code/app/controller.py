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
            result = model.get_score(posttext)
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
            result = model.get_biz_score(posttext,verbose)
            print(result)
            return render_template("bizid.html", results=result)
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
            result = model.get_biz_scores_from_location(posttext, limit, verbose)
            print(result)
            return render_template("location.html", results=result)
    return render_template("location.html")
