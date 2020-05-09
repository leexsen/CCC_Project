#Import the necessary methods from tweepy library
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from couchdb_util import couchDB

#Variables that contains the user credentials to access Twitter API
access_token = "1250405129175437312-8OczLcJHF6SJjkLLBKHnpL7HPDIX4J"
access_token_secret = "q999mxwFxgqmiE2cJRX12nrFQvFDrB7sJJPxob1wfajdT"
consumer_key = "o8JwBJas09Yu6zyedfW98JyZU"
consumer_secret = "H3G9HwO9tnejwfhZVhh3kwIFFUROk9KFHUgFc24N5B3sZ3HwHQ"

server_url = 'http://admin:admin123@worker1:4000/'
db_name = 'imported_twitter_melbourne'

masternode_hostname = 'worker1'

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self):
        super().__init__()
        self.db = couchDB(server_url, db_name)

    def on_data(self, data):
        tweet_json = json.loads(data)
        self.db.save_data_tweet(tweet_json)
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
    harvest_stream_tweets() 