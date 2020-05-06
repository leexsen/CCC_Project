#Import the necessary methods from tweepy library
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from couchdb_util import couchDB

#Variables that contains the user credentials to access Twitter API
access_token = "1252819926017904641-aUMOOcBgP9gfybldsREQ0Rgn6jHiSJ"
access_token_secret = "2FMzKYXE7h5SW4UrGJ2nLtLjsTFSDRDAd2aCzuREv6fal"
consumer_key = "iznF9PGZDSeM7xHCEvJsZ2d0g"
consumer_secret = "vTE9AL3BaHTWjmerkBRnHZ66QvvQgz74WMwkOSBAX90UN3nfHX"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        db = couchDB('http://admin:admin123@172.26.132.59:5984/', db_name)
        tweet_json = json.loads(data)
        db.save_data_tweet(tweet_json)
        return True

    def on_error(self, status):
        print(status)

    def on_timeout(self):
        return True


def harvest_stream_tweets():
    # This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, StdOutListener())
    while True:
        try:
            stream.filter(locations=[144.8889, -37.8917, 145.0453, -37.7325], languages=['en'])
        except Exception as e:
            print(e)



if __name__ == '__main__':
    db_name = 'twitter_stream_data_melbourne'
    harvest_stream_tweets()