import couchdb

class couchDB():

    def __init__(self, server_url, db_name=None):
        self.server_url = server_url
        self.couchserver = couchdb.Server(self.server_url)
        self.db_name = db_name

        if db_name is not None:
            self.create_db(db_name)
            self.db = self.couchserver[db_name]
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
        try:
            _id = data['_id']
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