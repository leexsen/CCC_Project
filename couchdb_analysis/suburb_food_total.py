import json
import couchdb
import csv
from couchdb.mapping import Document, TextField, IntegerField


def main():
    couch = couchdb.Server('http://admin:admin123@172.26.132.238:4000//')

    suburb_population = couch['regional_population'].view('_design/food/_view/suburb_population')

    country_population = couch['country_population'].view('_design/food/_view/country_population', reduce=False)

    suburb_food_persons = couch['clean_data'].view('_design/clean/_view/suburb_food_reduce', reduce=True, group=True)

    suburb_food_total = couch['clean_data'].view('_design/clean/_view/suburb_food_reduce', reduce=True, group_level=1)

    result = couch["suburb_food"]

    with open("Aurin_income.csv") as f2:
        suburb_file = f2.read().splitlines()
        f2.close()

    suburb_population_dict = {}
    suburb_country_population_percent = {}

    suburb_food_total_dict = {}
    suburb_food_percent = {}

    finalData = {}

    suburb_name = []

    for line in suburb_file:
        suburb_name.append(line.split(',')[0])

    for item in suburb_population:
        suburb_population_dict[item.key.lower()] = item.value
    for item in country_population:
        suburb = item.key[0].lower()
        country = item.key[1]
        persons_num = item.value
        try:
            suburb_country_population_percent[suburb].update({country: persons_num / suburb_population_dict[suburb]})
        except:
            suburb_country_population_percent[suburb] = {country: persons_num / suburb_population_dict[suburb]}

    # how many people in somewhere
    for item in suburb_food_total:
        suburb = item.key[0].lower()
        suburb_food_total = item.value
        suburb_food_total_dict[suburb] = suburb_food_total
    #
    # # how many people like Some kind of food
    # for item in suburb_food_persons:
    #     suburb = item.key[0].lower()
    #     foodName = item.key[1]
    #     foodNum = item.value
    #     try:
    #         suburb_food_percent[foodName].update({suburb:foodNum / suburb_food_total_dict[suburb]})
    #     except:
    #         suburb_food_percent[foodName] = {suburb: foodNum / suburb_food_total_dict[suburb]}
    #
    # for key in suburb_country_population_percent:
    #     suburb = key[0]
    #     country = key[1]
    #     country_percent = suburb_country_population_percent[key]
    #
    # for suburb in suburb_country_population_percent:
    #
    #     for foodName in suburb_food_percent:
    #         try:
    #             # suburb_country_population_percent[suburb].update(food_percent=suburb_food_percent[foodName][suburb])
    #             newDic = {"food_percent" : suburb_food_percent[foodName][suburb]}
    #             newDic.update(suburb_country_population_percent[suburb])
    #             try:
    #                 finalData[foodName].update({suburb:newDic})
    #             except:
    #                 finalData[foodName] = {suburb:newDic}
                #
                # csv_write.writerow( [foodName, suburb_country_population_percent[suburb]['australia'],
                #                      suburb_food_percent[foodName][suburb]] )

                # temp_suburb = suburb_name
                #
                # for name in suburb_food_percent[foodName]:
                #     if name in temp_suburb:
                #         csv_write.writerow( [foodName, suburb_country_population_percent[suburb],
                #                              suburb_food_percent[foodName][suburb]])
                #         temp_suburb.remove(name)
                #
                # if len(temp_suburb) > 0:
                #     for name in temp_suburb:
                #         csv_write.writerow([foodName, suburb_country_population_percent[name], 0])


                # if suburb_food_percent[foodName][suburb]:
                #     csv_write.writerow([foodName, suburb_country_population_percent[suburb],
                #                         suburb_food_percent[foodName][suburb]])
                # else:
                #     csv_write.writerow( [foodName, suburb_country_population_percent[suburb], 0])

            # except:
            #     # csv_write.writerow( [foodName, suburb_country_population_percent[suburb]['australia'], 0])
            #     print('缺少数据', suburb)

    # for key in finalData:
    #     doc = {
    #         "country": key,
    #         "stats": finalData[key]
    #     }
    #     result.save(doc)
    #
    # for key in finalData:
    #     print(key)
    #     print(finalData[key])
    count = 0
    for key in suburb_food_total_dict:
        count+=1
        # doc = {
        #     "suburb: ": key,
        #     "total tweets: ": suburb_food_total_dict[key]
        # }
        # result.save(doc)
        print(count)
        print(key)
        print(suburb_food_total_dict[key])

    print("Mission Complete!")


if __name__ == "__main__":
    main()


