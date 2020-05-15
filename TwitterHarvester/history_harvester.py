import tweepy
from tweepy import API
from tweepy import OAuthHandler
from couchdb_util import couchDB

def get_historical_twitters(start_time, end_time):
    access_token = "1250405129175437312-8OczLcJHF6SJjkLLBKHnpL7HPDIX4J"
    access_token_secret = "q999mxwFxgqmiE2cJRX12nrFQvFDrB7sJJPxob1wfajdT"
    consumer_key = "o8JwBJas09Yu6zyedfW98JyZU"
    consumer_secret = "H3G9HwO9tnejwfhZVhh3kwIFFUROk9KFHUgFc24N5B3sZ3HwHQ"
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    server_url = 'http://admin:admin123@worker1:4000/'
    db_name = 'imported_twitter_melbourne'

    masternode_hostname = 'worker1'

    db = couchDB(server_url, db_name)
    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    melbourne = api.geo_id('01864a8a64df9dc4')
    tweets = tweepy.Cursor(api.search, q="place:%s" % melbourne, lang = "en", since=start_time, until=end_time).items()

    while True:
        try:
            tweet = tweets.next()
            db.save_data_tweet(tweet._json)
        except tweepy.TweepError:
            continue


if __name__ == '__main__':
    start_time = '2020-05-08'
    end_time = '2020-05-15'
    get_historical_twitters(start_time, end_time)