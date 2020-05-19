import couchdb
import json

# my_couch = couchdb.Server("http://127.0.0.1:5984/")
# map_food_db = my_couch['map_food']
couch = couchdb.Server('http://admin:admin123@172.26.132.238:4000//')
db_food = couch['final_food']  # access to database 'final_food'

def get_food_data(suburb):
    dict = {}
    for id in db_food:
        doc = db_food[id]
        food_country = doc['country'].lower()
        suburbs = doc['stats']
        if suburb in suburbs:
            food_percentage = suburbs[suburb]['food_percent']
            dict[food_country] = food_percentage
    return dict


with open('suburb.json') as suburbs:
    suburbs_json = json.load(suburbs)

features = suburbs_json['features']
food_countries = ['china',  "japan", "korea", "india",  "australia",  "greece", "italy", "thai"]
for feature in features:
    properties = feature['properties']
    suburb = properties['name'].lower()

    # add food_final db data to suburbs json
    country_percents = get_food_data(suburb)
    for food_country in food_countries:
        if food_country not in country_percents:
            properties['food_' + food_country] = 0
        else:
            properties['food_' + food_country] = country_percents[food_country]

# map_food_db.save(suburbs_json)  # save to mydatabase

print(suburbs_json) # the json contains all data