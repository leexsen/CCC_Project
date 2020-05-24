import json
import couchdb
import csv
from couchdb.mapping import Document, TextField, IntegerField

finalData = {}


def main():
    couch = couchdb.Server('http://admin:admin123@172.26.132.238:4000//')

    suburb_income = couch['income_class'].view('_design/classification/_view/suburb_income', reduce=False)

    suburb_sport_persons = couch['clean_data'].view('_design/clean/_view/suburb_sport_reduce', reduce=True, group=True)

    suburb_sport_total = couch['clean_data'].view('_design/clean/_view/suburb_sport_reduce', reduce=True, group_level=1)

    result = couch["suburb_sport"]

    suburb_income_dict = {}

    suburb_sport_total_dict = {}
    suburb_sport_percent = {}

    for item in suburb_income:
        suburb = item.key.lower()
        mean_income = item.value
        suburb_income_dict[suburb] = mean_income

    # how many people in somewhere
    for item in suburb_sport_total:
        suburb = item.key[0].lower()
        suburb_sport_total = item.value
        suburb_sport_total_dict[suburb] = suburb_sport_total

    for key in suburb_sport_total_dict:
        doc = {
            "suburb: ": key,
            "total_tweets: ": suburb_sport_total_dict[key]
        }
        result.save(doc)
        print(key)

    print("Mission Complete!")


if __name__ == "__main__":
    main()

    # for key in finalData:
    #     for suburb in finalData[key]:
    #         csv_write.writerow([key, finalData[suburb]["income"], finalData[suburb]['sport_percent']])
