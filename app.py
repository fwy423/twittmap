from flask import Flask, render_template, jsonify, send_file
from moke_data import DataReader

sys.path.append("../co")
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# pre-load fixed tweets
def pre_load_fixed_data():
    keywords = ["music", "food", "sport", "show", "movie", "car", "commercial", "party", "war", "hello"]
    data = DataReader()
    return data.read("static/data/data.txt", keywords)


tweets_json = pre_load_fixed_data()


@app.route("/searchf/<keyword>")
def searchf(keyword=None):
    if keyword is None:
        to_return = jsonify(tweets_json)
    else:
        tweets_of_keyword = {keyword: []}
        if keyword in tweets_json:
            tweets_of_keyword = {keyword: tweets_json[keyword]}
        to_return = jsonify(tweets_of_keyword)
    return to_return


@app.route('/images/<filename>')
def get_image(filename=None):
    return send_file('static/images/' + filename, mimetype='image/png')


if __name__ == "__main__":
    app.run()
