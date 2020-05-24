import json
import couchdb
from couchdb.mapping import Document, TextField, IntegerField


with open ('suburb_population.json') as a:
    suburb_population = json.load(a)



result = dict()

country_lst = ['australia', 'china', 'england', 'france', 'greece', 'india', 'italy', 'japan', 'korea', 'thailand']


class People(Document):
    suburb = TextField()
    # born_country = TextField()
    persons_num = IntegerField()


def count_population(file):
    for feature in file["features"]:
        feature["properties"]
        suburb = feature["properties"]['sa2_name16']
        try:
            result[suburb] += feature["properties"]['persons_num']
        except:
            result[suburb] = feature["properties"]['persons_num']

def main():
    couch = couchdb.Server( 'http://admin:admin@127.0.0.1:5984//' )  # connect to couchdb

    couch.create('suburb_population')
    db = couch['suburb_population']

    count_population(suburb_population)
    print(result)
    for key in result:
        people = People(suburb=key, persons_num=result[key])
        people.store(db)


if __name__ == '__main__':
    main()
