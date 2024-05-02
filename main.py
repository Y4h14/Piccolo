#!/usr/bin/python3
import random
import string
from flask import Flask, render_template, redirect, request
from pymongo import mongo_client

app = Flask(__name__)
client = mongo_client.MongoClient()
db = client.pico


def generate_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for i in range(length))
    return short_url


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = generate_url()
        # add check to see if the generated short_url is
        # not already in the database
        try:
            db.pico.insert_one({'_id': short_url, 'long_url': long_url})
        except Exception as e:
            print(e)
        # return f"Pico URL: {request.url_root}{short_url}"
        result_url = f"{request.url_root}{short_url}"
        return render_template("result.html",
                               short_url=result_url, long_url=long_url)
    return render_template("index.html")


@app.route('/<short_url>')
def redirect_url(short_url):
    # long_url = shortend_urls.get(short_url)
    query = db.pico.find_one({'_id': short_url})
    if query:
        print(query)
        long_url = query['long_url']
    else:
        return "URL not found", 402
    if long_url:
        if long_url.find("http://") != 0 and long_url.find("https://") != 0:
            long_url = "http://" + long_url
        print(long_url)
        return redirect(long_url)
    else:
        return "URL not found", 402


if __name__ == '__main__':
    app.run(debug=True)
