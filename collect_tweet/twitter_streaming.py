import tweepy
import time
import json

from twitter_elasticsearch_util import upload, search, creat_mapping


def load_keys(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)
        ckey = data["ckey"]
        csecret = data["csecret"]
        atoken = data["atoken"]
        asecret = data["asecret"]
        elastic_host = data["elastic_host"]
        return ckey, csecret, atoken, asecret, elastic_host


def center_location(location):
    assert len(location) == 1 and len(location[0]) == 4
    x = location[0][0][0] + location[0][1][0] + location[0][2][0] + location[0][3][0]
    y = location[0][0][1] + location[0][1][1] + location[0][2][1] + location[0][3][1]
    return x / 4, y / 4


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, elastic_host, limit_mode=True, time_limit=60, log_file=None):
        print("Initialization...")
        if limit_mode:
            print("Time Limit Mode: ", time_limit, "sec")
            self.start_time = time.time()
            self.limit = time_limit

        if log_file is None:
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

        if (time.time() - self.start_time) < self.limit:
            try:
                json_msg = json.loads(data)
                if json_msg.get("place") is not None:
                    print("+++++++++++++")
                    location = json_msg["place"]["bounding_box"]["coordinates"]
                    location_long, location_lat = center_location(location)
                    text = json_msg["text"]
                    timestamp = int(json_msg["timestamp_ms"])
                    timestamp = time.strftime("%a %b %d %H:%M:%S", time.localtime(timestamp))
                    user_name = json_msg["user"]["screen_name"]
                    print('location_long:', location_long)
                    print('location_lat:', location_lat)
                    print('timestamp:', timestamp)
                    print('user_name:', user_name)
                    print('text:', text)

                    upload_data = {
                        "location_long": location_long,
                        "location_lat": location_lat,
                        "timestamp": timestamp,
                        "user_name": user_name,
                        "text": text
                    }
                    print(upload_data)
                    upload(elastic_host, upload_data)

            except Exception as e:
                print("Error: " + str(e))
                self.log_file.write("Error: " + str(e))

            return True
        else:
            self.log_file.close()
            return False


def running(key_words, key_path, limit_mode=True, time_limit=100):
    ckey, csecret, atoken, asecret, elastic_host = load_keys(key_path)
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    api = tweepy.API(auth)
    with open("streaming.log", 'a', encoding="utf-8") as log:
        print("start streaming...")
        myStreamListener = MyStreamListener(elastic_host=elastic_host, limit_mode=limit_mode, time_limit=time_limit,
                                            log_file=log)
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=key_words)


if __name__ == '__main__':
    keywords = ["lunch", "food", "dinner", "eat", "desert", "delicious", "drinks", "bar", "restaurant", "breakfast"]
    running(keywords, key_path="keys.json", limit_mode=True, time_limit=100)

    # ckey, csecret, atoken, asecret, elastic_host = load_keys("../../keys.json")
    # auth = tweepy.OAuthHandler(ckey, csecret)
    # auth.set_access_token(atoken, asecret)
    #
    # api = tweepy.API(auth)
    # with open("streaming.log", 'a', encoding="utf-8") as log:
    #     print("start streaming...")
    #     myStreamListener = MyStreamListener(elastic_host=elastic_host, limit_mode=False, time_limit=10, log_file=log)
    #     myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    #     myStream.filter(track=['hello'])
