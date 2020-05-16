import tweepy
import time
from tweepy import API
from tweepy import OAuthHandler
from couchdb_util import couchDB


access_token = "1252819926017904641-aUMOOcBgP9gfybldsREQ0Rgn6jHiSJ"
access_token_secret = "2FMzKYXE7h5SW4UrGJ2nLtLjsTFSDRDAd2aCzuREv6fal"
consumer_key = "iznF9PGZDSeM7xHCEvJsZ2d0g"
consumer_secret = "vTE9AL3BaHTWjmerkBRnHZ66QvvQgz74WMwkOSBAX90UN3nfHX"

server_url = 'http://admin:admin123@worker1:4000/'
db_name = 'imported_twitter_melbourne'
masternode_hostname = 'worker1'

def get_historical_twitters(start_time, end_time):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    db = couchDB(server_url, db_name)
    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # place = api.geo_search(query="AU", granularity="country")[0].id
    melbourne_place_id = '01864a8a64df9dc4'
    tweets = tweepy.Cursor(api.search, q="place:{}".format(melbourne_place_id), lang="en", since=start_time, until=end_time).items()

    def save_data():
        tweet = tweets.next()
        db.save_data_tweet(tweet._json)

    while True:
        try:
            save_data()
        except tweepy.TweepError:
            time.sleep(1000)
            continue
        except Exception as e:
            # Not sure what to do with StopIteration error
            save_data()


if __name__ == '__main__':
    # Note: It can harvest tweets from only the past few days.
    start_time = '2020-05-10'
    end_time = '2020-05-30'
    get_historical_twitters(start_time, end_time)

