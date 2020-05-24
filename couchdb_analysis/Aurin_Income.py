import json
import couchdb
from couchdb.mapping import Document, TextField, IntegerField
import csv

with open ('SA2_Estimates_of_Personal-Income.json') as data:
    Personal_Income = json.load(data)
    data.close()


class Income(Document):
    suburb = TextField()
    mean_income = IntegerField()
    income_class= IntegerField()


result = dict()

rich = range(85000, 150000)
middle = range(62000, 85000)
poor = range(0, 60000)


def allocate_mean_income(file):
    for feature in file["features"]:
        suburb = feature["properties"]["sa2_name16"]
        mean = feature["properties"]["mean_aud"]
        if mean in rich:
            result[suburb] = [mean, 1]
        elif mean in middle:
            result[suburb] = [mean, 0]
        elif mean in poor:
            result[suburb] = [mean, -1]


def main():
    couch = couchdb.Server( 'http://admin:admin123@172.26.132.238:4000//' )  # connect to couchdb

    db = couch['income_class']

    allocate_mean_income( Personal_Income )

    for key in result:
        income = Income(suburb=key , mean_income=result[key][0], income_class=result[key][1])
        income.store(db)


if __name__ == '__main__':
    main()
    print(result)
    # file = open( 'Aurin_income.csv', 'a', newline='' )
    # csv_write = csv.writer( file, dialect='excel' )
    # allocate_mean_income( Personal_Income )
    # for key in result:
    #     csv_write.writerow([key, result[key][0]])