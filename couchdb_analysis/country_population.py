import json
import couchdb
from couchdb.mapping import Document, TextField, IntegerField


with open ('G09a.json') as a:
    countries_a = json.load(a)

with open ('G09b.json') as b:
    countries_b = json.load(b)

with open ('G09c.json') as c:
    countries_c = json.load(c)

with open ('G09d.json') as d:
    countries_d = json.load(d)

with open ('G09e.json') as e:
    countries_e = json.load(e)

with open ('G09f.json') as f:
    countries_f = json.load(f)

with open ('G09g.json') as g:
    countries_g = json.load(g)

with open ('G09h.json') as h:
    countries_h = json.load(h)


result = dict()

country_lst = ['australia', 'china', 'england', 'france', 'greece', 'india', 'italy', 'japan', 'korea', 'thailand']


class People(Document):
    suburb = TextField()
    born_country = TextField()
    num = IntegerField()


def count_population(file):
    for feature in file["features"]:
        suburb = feature["sa2_name16"]
        for country in feature["properties"]:
            if country in country_lst:
                try:
                    result[suburb, country] = max(result[suburb, country], feature["properties"][country])
                except:
                    result[suburb, country] = feature["properties"][country]


def main():
    couch = couchdb.Server( 'http://admin:admin123@172.26.132.238:4000//' )  # connect to couchdb

    db = couch['country_population']

    count_population(countries_a)
    count_population(countries_b)
    count_population(countries_c)
    count_population(countries_d)
    count_population(countries_e)
    count_population(countries_f)
    count_population(countries_g)
    count_population(countries_h)

    for key in result:
        people = People(suburb=key[0], born_country=key[1], num=result[key])
        people.store(db)


if __name__ == '__main__':
    main()
