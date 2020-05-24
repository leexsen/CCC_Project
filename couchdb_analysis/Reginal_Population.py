import json
import couchdb
from couchdb.mapping import Document, TextField, IntegerField
import csv

with open ('Regional_Pop_Sum.json') as data:
    regional_population = json.load( data )
    data.close()


class Populaiton( Document ):
    suburb = TextField()
    population = IntegerField()


result = dict()


def allocate_mean_income(file):
    for feature in file["features"]:
        suburb = feature["properties"]["sa2_name16"]
        population = feature["properties"]["persons_num"]
        result[suburb] = population


def main():
    couch = couchdb.Server( 'http://admin:admin123@172.26.132.238:4000//' )  # connect to couchdb

    db = couch['regional_population']

    allocate_mean_income( regional_population )

    for key in result:
        income = Populaiton( suburb=key, population=result[key])
        income.store(db)


if __name__ == '__main__':
    main()
    print(result)
    # file = open( 'Aurin_income.csv', 'a', newline='' )
    # csv_write = csv.writer( file, dialect='excel' )
    # allocate_mean_income( Personal_Income )
    # for key in result:
    #     csv_write.writerow([key, result[key][0]])