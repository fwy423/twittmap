import sys
import json
from flask import Flask, render_template, send_file
from moke_data import DataReader

sys.path.append("collect_tweet/")
from twitter_elasticsearch_util import clear, search

app = Flask(__name__)
elastic_host = "search-twittmap-wf-tos22nd6jgkyhdhvbptnb4pv7a.us-east-1.es.amazonaws.com"


@app.route("/")
def index():
    return render_template("index.html")


# pre-load fixed tweets
def pre_load_fixed_data():
    keywords = ["music", "food", "sport", "show", "movie", "car", "commercial", "party", "war", "hello"]
    data = DataReader()
    return data.read("static/data/data.txt", keywords)


# tweets_json = pre_load_fixed_data()

@app.route("/clear/<keyword>")
def clear(keyword=None):
    return clear(elastic_host, keyword)


@app.route("/searchf/<keyword>")
def searchf(keyword):
    result = json.loads(search(elastic_host, keyword))
    # for items in result["result"]:
    #     print(items)
    return result


@app.route('/images/<filename>')
def get_image(filename=None):
    return send_file('static/images/' + filename, mimetype='image/png')


if __name__ == "__main__":
    app.run()
