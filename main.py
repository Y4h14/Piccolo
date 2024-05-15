#!/usr/bin/python3
"""Define a flask application"""
import random
import string
import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, redirect, request, send_file
from pymongo import mongo_client
import qrcode

# creating the flask app
app = Flask(__name__)

# finding and loading .env
env_path = find_dotenv()
load_dotenv(env_path)

# conncectiong to a mongo database Atlas
client = mongo_client.MongoClient(os.getenv("DB_CONNECT"))
db = client.pico


def generate_url(length=6):
    """
    generates a string that acts as the short url with a specified length
    Args:
        - length: the lenth of the random string genrated
    """
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for i in range(length))
    return short_url


def check_exists(field, value):
    """"
    checks if a specific value exists in the database
    Args:
        - field: the field in the database
        - value: the value to look for
    Returns: Ture if the value exists in the field
    """
    try:
        result = db.pico.find_one({field: value})
    except Exception:
        return False

    return result is not None


@app.route('/', methods=['GET', 'POST'])
def index():
    """Defines the main route for the flask application"""
    if request.method == 'POST':
        long_url = request.form['long_url']
        if long_url == '':
            return render_template('index.html')

        # check if the long url alredy in database
        if check_exists("long_url", long_url):
            query = db.pico.find_one({"long_url": long_url})
            long_url = query["long_url"]
            short_url = query["_id"]
        else:
            short_url = generate_url()
            # generate a new short_url if it's already exitst
            if check_exists("_id", short_url):
                short_url = generate_url()
            try:
                db.pico.insert_one({'_id': short_url, 'long_url': long_url})
            except Exception as e:
                print(e)

        # create the resutling url
        result_url = f"{request.url_root}{short_url}"

        # create the qercode image
        img = qrcode.make(long_url)
        img_file = "static/images/qrcode.png"
        img.save(img_file)

        return render_template("result.html",
                               short_url=result_url,
                               long_url=long_url, img=img_file)
    return render_template("index.html")


@app.route('/<short_url>')
def redirect_url(short_url):
    """route fucntion for forwarding short url to long url"""
    query = db.pico.find_one({'_id': short_url})
    if query:
        long_url = query['long_url']
    else:
        return "URL not found", 402
    # put the long URL in the correct format
    if long_url:
        if long_url.find("http://") != 0 and long_url.find("https://") != 0:
            long_url = "http://" + long_url

        return redirect(long_url)
    else:
        return "URL not found", 402


if __name__ == '__main__':
    app.run(debug=True)
