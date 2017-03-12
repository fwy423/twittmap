import sys
from flask import Flask, render_template, send_file,jsonify

sys.path.append("collect_tweet/")
from twitter_elasticsearch_util import clear, search, location_search

application = Flask(__name__)
elastic_host = "search-twittmap-wf-tos22nd6jgkyhdhvbptnb4pv7a.us-east-1.es.amazonaws.com"
keywords = ["lunch", "food", "dinner", "eat", "desert", "delicious", "drinks", "bar", "restaurant", "breakfast"]


@application.route("/")
def index():
    return render_template("index.html")

@application.route("/clear/<keyword>")
def clear(keyword=None):
    return clear(elastic_host, keyword)


@application.route("/searchf/<keyword>")
def searchf(keyword):
    if keyword in keywords:
        result = search(elastic_host, keyword)
    else:
        location = keyword.split()
        location = map(float, location)
        print (location)
        result = location_search(elastic_host, location)
    return jsonify(result)


@application.route('/images/<filename>')
def get_image(filename=None):
    return send_file('static/images/' + filename, mimetype='image/png')


if __name__ == "__main__":
    application.run(host = '0.0.0.0')
