import tweepy
import time

ckey = "ZlPgE73ivGdJAl3ROeNHc1RKJ"
csecret = "s9FyEOMOmjckzmtfuwm9Iw6NGiFk8tMxmEYllxYzC1rMd4XDVe"
atoken = "784480113459093504-izVnLvSy8MAE5e84tYD04WY1CCaKD4L"
asecret = "nhQiQaRxFrUyNLtCOjeLO7wBVx9XcvSG8OqCAtg5RhqmJ"

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)
public_tweets = api.home_timeline()


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, limit_mode=True, time_limit=60, log_file=None):
        if (limit_mode):
            self.start_time = time.time()
            self.limit = time_limit

        if (log_file is None):
            # creat a new log file
            self.log_file = open('streaming.log', 'a', encoding='utf8')
        else:
            self.log_file = log_file

        super(MyStreamListener, self).__init__()

    def on_error(self, status_code):
        if status_code == 420:
            self.log_file.close()
            # returning False in on_data disconnects the stream
            return False

    def on_data(self, data):
        # parse the twitter and extract the geolocation information
        # Reference: https://dev.twitter.com/overview/api/tweets

        print(data.text)