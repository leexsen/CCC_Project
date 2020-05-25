from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
import couchdb
import json

# my_couch = couchdb.Server("http://127.0.0.1:5984/")
# map_food_db = my_couch['map_food']
couch = couchdb.Server("http://admin:admin123@172.26.132.238:4000//")
db_food = couch["final_food"]  # access to database "final_food"
db_sport = couch["final_sport"]  # access the database "final_sport"
location_time_summary_db = couch["location_time_summary"]  # access the database location_time_summary
db_suburb_food = couch["suburb_food"]
db_suburb_sport = couch["suburb_sport"]
print("load couchDB")
print("food", db_food)
print("sport", db_sport)


def get_food_data(suburb):
    dict = {}
    for id in db_food:
        doc = db_food[id]
        food_country = doc["country"].lower()
        suburbs = doc["stats"]
        if suburb in suburbs:
            food_percentage = suburbs[suburb]["food_percent"]
            dict[food_country] = food_percentage
    # print("food data", dict)
    return dict


def get_sport_data(suburb):
    dict = {}
    for id in db_sport:
        doc = db_sport[id]
        sport = doc["sport"]
        suburbs = doc["stats"]
        if suburb in suburbs:
            exercise_percentage = suburbs[suburb]["sport_percent"]
            dict[sport] = exercise_percentage
    return dict


def get_sleep_data():
    average_person_tweet_view = location_time_summary_db.view("myViews/avarage_person_tweet")

    dict = {}
    for item in average_person_tweet_view:
        if item.value is not None and item.key.lower() != "west melbourne":
            suburb = item.key.lower()
            average_person_tweet = item.value
            dict[suburb] = {}
            dict[suburb]["average_person_tweet"] = average_person_tweet

    return dict


def get_median_age():
    suburb_median_age = location_time_summary_db.view("myViews/suburb_median_age")

    dict = {}
    for item in suburb_median_age:
        if item.value is not None and item.key.lower() != "west melbourne":
            suburb = item.key.lower()
            median_age = item.value
            dict[suburb] = {}
            dict[suburb]["median_age"] = median_age
    # print("age data", dict)
    return dict

def get_suburb_food():
    dic = {}
    for id in db_suburb_food:
        # print("id",id)
        # print("111",db_suburb_food[id])
        # print(db_suburb_food[id]['suburb: '])
        suburb = db_suburb_food[id]['suburb: ']
        # print(suburb)
        total_tweets = db_suburb_food[id]['total tweets: ']

        dic[suburb] = total_tweets
    return dic

def get_suburb_sport():
    dic = {}
    for id in db_suburb_sport:
        suburb = db_suburb_sport[id]['suburb: ']
        print(id)
        total_tweets = db_suburb_sport[id]['total_tweets: ']
        dic[suburb] = total_tweets
    return dic

def write2json():
    with open("suburb_info-1589933179300.json") as suburbs:
        suburbs_json = json.load(suburbs)

    features = suburbs_json["features"]
    food_countries = ["china", "japan", "korea", "india", "australia", "greece", "italy", "thai"]
    sports = ["cycling", "rugby", "basketball", "horsing", "tennis", "golf", "swimming", "dancing", "soccer", "karate"]
    for feature in features:
        properties = feature["properties"]
        suburb = properties["name"].lower()

        # add food_final db data to suburbs json
        country_percents = get_food_data(suburb)
        for food_country in food_countries:
            if food_country not in country_percents:
                properties["food_" + food_country] = "null"
            else:
                properties["food_" + food_country] = country_percents[food_country]

        # add sport_final db data to suburbs json
        sport_percents = get_sport_data(suburb)
        for sport in sports:
            if sport not in sport_percents:
                properties["sport_" + sport] = "null"
            else:
                properties["sport_" + sport] = sport_percents[sport]

        # add location_time_summary db data to suburbs json
        average_person_tweets = get_sleep_data()
        if suburb in average_person_tweets:
            properties["average_person_tweets"] = average_person_tweets[suburb]["average_person_tweet"]
        else:
            properties["average_person_tweets"] = "null"

        # add median_age data to suburbs json
        median_ages = get_median_age()
        if suburb in median_ages:
            properties["median_age"] = median_ages[suburb]["median_age"]
        else:
            properties["median_age"] = "null"

        # add suburb_food data to suburbs json
        suburb_food = get_suburb_food()
        if suburb in suburb_food:
            properties["food_total"] = suburb_food[suburb]
        else:
            properties["food_total"] = "null"

        # add suburb_sport data to suburbs json
        suburb_sports = get_suburb_sport()
        if suburb in suburb_sports:
            properties["sports_total"] = suburb_sports[suburb]
        else:
            properties["sports_total"] = "null"
    

    suburb_str = json.dumps(suburbs_json)
    suburb_str.replace('\'', '\"').replace("None", "null")
    # map_food_db.save(suburbs_json)  # save to mydatabase

    output = open("suburb_info_test.json", 'w')
    output.write(suburb_str)

    # print(suburbs_json1) # the json contains all data

def updateMap():
    gis = GIS(username="xuazhou", password="zx122333098")

    search_result = gis.content.search(query="info", item_type="Feature Layer")
    suburb = search_result[0]
    print(search_result[0])

    suburb_collection = FeatureLayerCollection.fromitem(suburb)
    print(suburb_collection.properties)
    suburb_collection.manager.overwrite('suburb_info-1589933179300.json')


# write2json()
# print("JSON written")
updateMap()
print("updated")
