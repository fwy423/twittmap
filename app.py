from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


# pre-load fixed tweets
def pre_load_fixed_data():
    keywords = ["music", "food", "sport", "show", "movie", "car", "commercial", "party", "war", "hello"]
    data = DataReader()
    return data.read("static/data/tweets.txt", keywords)

tweets_json = pre_load_fixed_data()
@app.route("/searchf/<keyword>")
def searchf(keyword = None):
	if keyword is None:


if __name__ == "__main__":
    app.run()