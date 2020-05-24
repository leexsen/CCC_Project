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

    result = couch['final_sport']

    file = open( 'sport_income.csv', 'a', newline='' )
    csv_write = csv.writer( file, dialect='excel' )

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

    # how many people like Some kind of sport
    for item in suburb_sport_persons:
        suburb = item.key[0].lower()
        sport_name = item.key[1]
        sport_num = item.value
        try:
            suburb_sport_percent[sport_name].update({suburb: sport_num / suburb_sport_total_dict[suburb]})
        except:
            suburb_sport_percent[sport_name] = {suburb: sport_num / suburb_sport_total_dict[suburb]}

    for sport_name in suburb_sport_percent:
        for suburb in suburb_income_dict:
            # print(suburb_sport_percent[sport_name])
            # print(suburb_sport_percent[sport_name][suburb])
            try:
                # suburb_country_population_percent[suburb].update(food_percent=suburb_food_percent[foodName][suburb])
                newDic = {"income": suburb_income_dict[suburb],
                          "sport_percent" : suburb_sport_percent[sport_name][suburb]}

                # newDic.update(suburb_income_dict[suburb])
                # print(newDic)
                try:
                    finalData[sport_name].update({suburb:newDic})
                except:
                    finalData[sport_name] = {suburb:newDic}

                if suburb_sport_percent[sport_name][suburb]:
                    csv_write.writerow([sport_name, suburb_income_dict[suburb],
                                        suburb_sport_percent[sport_name][suburb]])
                else:
                    csv_write.writerow( [sport_name, suburb_income_dict[suburb], 0])

            except:
                print('缺少数据', suburb)

    # for key in finalData:
    #     doc = {
    #         "sport": key,
    #         "stats": finalData[key]
    #     }
    #     result.save(doc)

    print("Mission Complete!")


if __name__ == "__main__":
    main()

    # for key in finalData:
    #     for suburb in finalData[key]:
    #         csv_write.writerow([key, finalData[suburb]["income"], finalData[suburb]['sport_percent']])
