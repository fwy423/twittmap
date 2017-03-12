import tweepy
import time
import json

from static_variables import ckey, csecret, atoken, asecret


def center_location(location):
    assert len(location) == 4
    x = location[0][0] + location[1][0] + location[2][0] + location[3][0]
    y = location[0][1] + location[1][1] + location[2][1] + location[3][1]
    return [x / 4, y / 4]


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, limit_mode=True, time_limit=60, log_file=None):
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
        print("+++++++++++++")
        if (time.time() - self.start_time) < self.limit:
            try:
                json_msg = json.loads(data)

                if json_msg.get("place") is not None:
                    location = json_msg["place"]["bounding_box"]["coordinates"]
                    #                 location = json_msg["coordinates"]["coordinates"]
                    text = json_msg["text"]
                    timestamp = json_msg["timestamp_ms"]
                    user_name = json_msg["user"]["screen_name"]
                    print('location:', location[0][0])
                    print('timestamp:', timestamp)
                    print('user_name:', user_name)
                    print('text:', text)

            except Exception as e:
                print("Error: " + str(e))
                self.log_file.write("Error: " + str(e))

            return True
        else:
            self.log_file.close()
            return False


if __name__ == '__main__':

    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    api = tweepy.API(auth)
    with open("streaming.log", 'a', encoding="utf-8") as log:
        print("start streaming...")
        myStreamListener = MyStreamListener(limit_mode=True, time_limit=10, log_file=log)
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=['hello'])
