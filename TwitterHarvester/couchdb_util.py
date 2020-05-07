import couchdb

class couchDB():

    def __init__(self, server_url, db_name=None):
        self.server_url = server_url
        self.couchserver = couchdb.Server(self.server_url)
        self.db_name = db_name
        if db_name is not None:
            self.db=self.couchserver[db_name]
        else:
            self.db = None

    def create_db(self, db_name):
        if db_name in self.couchserver:
            print("Database {} already exists.".format(db_name))
        else:
            self.couchserver.create(db_name)
            print("Database {} has been created.".format(db_name))

    def deleteDB(self, dbname):
        try:
            del self.couchserver[dbname]
            print("Database {} has been deleted".format(dbname))
        except NameError:
            print("Database {} does not exist".format(dbname))

    def show_all_dbs(self):
        print([db for db in self.couchserver])

    def save_data_tweet(self, data):
        if "id_str" not in data:
            print("Requirement not satisfied: Data about to save should contain field 'id_str'.")
        else:
            _id = data["id_str"]
            data["_id"] = _id
            try:
                self.db.save(data)
                print('Tweet {} has been saved to {}'.format(_id, self.db_name))
            except couchdb.http.ResourceConflict:
                print('Tweet {} already exits in database'.format(_id))
                pass

    def get_data_by_key(self, key):
        try:
            return self.db[key]
        except Exception as e:
            raise e

    def get_all_data(self):
        all_data = []
        for item in self.db.view('_all_docs', include_docs=True):
            all_data.append(item['doc'])
        return all_data



if __name__ == '__main__':
    # Below can be used for CouchDB test
    SERVER_URL = 'http://admin:admin123@172.26.132.59:5984/'
    db = couchDB(SERVER_URL, 'test')
    db.show_all_dbs()
    tweet = {
              "created_at": "Sun Apr 19 10:10:29 +0000 2020",
              "id": 1251815425601605632,
              "id_str": "1251815425601605632",
              "text": "The fish and the pond are the best friends fish #throwback #melbourne #melbourneiloveyou #checkmelbourne"
            }
    db.save_data_tweet(tweet)
    print(db.get_data_by_key('1251815425601605632'))
    print(db.get_all_data()) 