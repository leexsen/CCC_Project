# Import the necessary methods from tweepy library
# import sys
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from couchdb_util import couchDB


# Variables that contains the user credentials to access Twitter API
access_token = "1252819926017904641-aUMOOcBgP9gfybldsREQ0Rgn6jHiSJ"
access_token_secret = "2FMzKYXE7h5SW4UrGJ2nLtLjsTFSDRDAd2aCzuREv6fal"
consumer_key = "iznF9PGZDSeM7xHCEvJsZ2d0g"
consumer_secret = "vTE9AL3BaHTWjmerkBRnHZ66QvvQgz74WMwkOSBAX90UN3nfHX"

server_url = 'http://admin:admin123@worker1:4000/'
db_name = 'imported_twitter_melbourne'
masternode_hostname = 'worker1'

# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self):
        super().__init__()
        self.db = couchDB(server_url, db_name)

    def on_data(self, data):
        tweet_json = json.loads(data)
        print(tweet_json)
        self.db.save_data_tweet(tweet_json)
        return True

    def on_error(self, status):
        # print(sys.stderr, 'Encountered error with status code:', status)
        if status == 420:
            return False
        return True  # Don't kill the stream

    def on_timeout(self):
        # print(sys.stderr, 'Timeout...')
        return True


def harvest_stream_tweets():
    # This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, StdOutListener(),wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    while True:
        try:
            # [144.8889, -37.8917, 145.0453, -37.7325]
            stream.filter(locations=[144.3336, -38.5030, 145.8784, -37.1751], languages=['en'])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    harvest_stream_tweets()