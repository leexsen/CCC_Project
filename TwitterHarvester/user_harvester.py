import tweepy
from couchdb_util import couchDB
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, timedelta

access_token = "1252819926017904641-aUMOOcBgP9gfybldsREQ0Rgn6jHiSJ"
access_token_secret = "2FMzKYXE7h5SW4UrGJ2nLtLjsTFSDRDAd2aCzuREv6fal"
consumer_key = "iznF9PGZDSeM7xHCEvJsZ2d0g"
consumer_secret = "vTE9AL3BaHTWjmerkBRnHZ66QvvQgz74WMwkOSBAX90UN3nfHX"


class UserTweetsHavester:

    def __init__(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        self.server_url = 'http://admin:admin123@worker1:4000/'
        self.db_name = 'imported_twitter_melbourne'
        masternode_hostname = 'worker1'
        self.db = couchDB(self.server_url, self.db_name)

    def save_used_ids_to_file(self):
        user_ids = set()
        data = self.db.get_all_data()
        for json_obj in data:
            user_id = json_obj['user']['id']
            user_ids.add(str(user_id))
        with open('user_ids.txt', 'w') as f:
            for user_id in user_ids:
                f.write(user_id)
                f.write('\n')

    def get_followers_and_save_ids(self, user_id):
        follower_ids = self.api.followers_ids(user_id)
        with open('follower_ids.txt', 'a') as f:
            for follower_id in follower_ids:
                # print(follower_id)
                f.write(str(follower_id))
                f.write('\n')

    def get_tweets_by_user(self, user_id):
        end_date = datetime.utcnow() - timedelta(days=120)
        melbourne_place_id = '01864a8a64df9dc4'
        for status in Cursor(self.api.user_timeline, id=user_id, q="place:{}".format(melbourne_place_id), lang="en").items():
            self.db.save_data_tweet(status._json)
            if status.created_at < end_date:
                break


if __name__ == '__main__':
    harvester = UserTweetsHavester()
    harvester.save_used_ids_to_file()

    user_ids = []
    with open('user_ids.txt') as f:
        for line in f:
            user_id = line[:-1]
            user_ids.append(user_id)

    for user_id in user_ids:
        harvester.get_tweets_by_user(user_id)

    # 2 The below is for saving follower ids

    # for user_id in user_ids:
    #     harvester.get_followers_and_save_ids(user_id)
    #follower_ids = []
    #with open('follower_ids.txt') as f:
        #for line in f:
            #follower_id = line[:-1]
            #follower_ids.append(follower_id)

    #for follower_id in follower_ids:
       # harvester.get_tweets_by_user(follower_id)

