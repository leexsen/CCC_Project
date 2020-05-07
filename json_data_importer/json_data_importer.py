from mpi4py import MPI
from couchdb_util import couchDB
import os, sys, json, array, requests

server_url = 'http://admin:admin123@172.26.132.238:4000/'
db_name = 'imported_twitter_melbourne'

class TwitterFile:
    def __init__(self, filename):
        # opening it in binary mode instead of text mode for avoiding 
        # unnecessary decoding 
        self.file = open(filename, 'r')

        # skip the first row
        self.file.readline()
        
        # load the index file
        index_filename = filename + '.index'
        self.load_index(index_filename)
        
        # the total_rows is stored at the tail of the index, which is index[-1],
        # and the first row of the twitter file doesn't count.
        self.total_rows = self.index[-1] - 1

    # the index consistis of the absolute offset of a line from the start of the
    # twitter file.
    def load_index(self, filename):
        with open(filename, 'rb') as f:
            filesize = os.path.getsize(filename)

            # each element in the index is a type of unsigned long
            self.index = array.array('L') 
            self.index.fromfile(f, filesize // self.index.itemsize)

    # get the absolute starting position of a line from the index so 
    # it can jump to that line immediately
    def skip_lines(self, num_lines):
        offset = self.index[num_lines]
        self.file.seek(offset)

    def get_total_rows(self):
        return self.total_rows

    def close(self):
        self.file.close()

    
    def readline_json(self):
        line = self.file.readline()

        # remove the comma and '\n' at the end of the line
        if line[-2] == ',':
            line = line[:-2]
        else:
            line = line[:-1]

        try:
            return json.loads(line)
        except json.decoder.JSONDecodeError:
            return None

class ComputeNode:
    def __init__(self, filename):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()

        self.file = TwitterFile(filename)

        session = requests.Session()
        response = session.get(server_url)
        cookies = response.cookies.get_dict()
        cookie = '{}={}'.format('mycookies', cookies['mycookies'])

        print('Connected to ' + cookies['mycookies'])

        if self.rank == 0:
            self.db = couchDB(server_url, db_name, cookie)

            for i in range(1, self.size):
                self.comm.send(0, dest=i)

        else:
            self.comm.recv(source=0)
            self.db = couchDB(server_url, db_name, cookie)

    def compute_start_end(self):
        total_rows = self.file.get_total_rows()
        chunk_size = total_rows // self.size + 1
        self.start = self.rank * chunk_size
        self.end = min(self.start + chunk_size, total_rows)

    def compute_upload_data(self):
        if self.start > 0:
            self.file.skip_lines(self.start)
        
        for _ in range(self.start, self.end):
            row = self.file.readline_json()

            if row is None:
                continue

            data = row['doc']
            data['key'] = row['key']
            del data['_rev']

            self.db.save_data_tweet(data)


    def close(self):
        self.file.close()
    
        
twitter_filename = sys.argv[1]

computeNode = ComputeNode(twitter_filename)
computeNode.compute_start_end()
computeNode.compute_upload_data()

computeNode.close()
