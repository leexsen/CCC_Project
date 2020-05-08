#Import the necessary methods from tweepy library
import json, requests
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from couchdb_util import couchDB
from python_hosts.hosts import Hosts

#Variables that contains the user credentials to access Twitter API
access_token = "1252819926017904641-aUMOOcBgP9gfybldsREQ0Rgn6jHiSJ"
access_token_secret = "2FMzKYXE7h5SW4UrGJ2nLtLjsTFSDRDAd2aCzuREv6fal"
consumer_key = "iznF9PGZDSeM7xHCEvJsZ2d0g"
consumer_secret = "vTE9AL3BaHTWjmerkBRnHZ66QvvQgz74WMwkOSBAX90UN3nfHX"

couchdb_url = 'http://admin:admin123@worker1:4000/'
db_name = 'twitter_stream_data_melbourne'

masternode_hostname = 'worker1'

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self, hosts):
        super().__init__()

        # this is to ensure the load balancer will direct us to the same node
        # as before. In other word, this is to let the load balancer to us to a
        # consistent worker node all the time.

        masternode_ip = hosts[masternode_hostname]
        server_url = couchdb_url.replace(masternode_hostname, masternode_ip)

        session = requests.Session()
        response = session.get(server_url)
        cookies = response.cookies.get_dict()
        cookie = '{}={}'.format('mycookies', cookies['mycookies'])

        print('Connected to ' + cookies['mycookies'])

        self.db = couchDB(server_url, db_name, cookie)

    def on_data(self, data):
        tweet_json = json.loads(data)
        self.db.save_data_tweet(tweet_json)
        return True

    def on_error(self, status):
        print(status)

    def on_timeout(self):
        return True

# This will read /etc/hosts for resolving hostnames
def init_hosts():
    hosts = {}
    host_entries = Hosts(Hosts.determine_hosts_path()).entries

    for entry in host_entries:
        if entry.names is None:
            continue

        name = entry.names[0]
        hosts[name] = entry.address

    return hosts

def harvest_stream_tweets():
    # This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    hosts = init_hosts()

    stream = Stream(auth, StdOutListener(hosts))
    
    while True:
        try:
            stream.filter(locations=[144.8889, -37.8917, 145.0453, -37.7325], languages=['en'])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    harvest_stream_tweets() 