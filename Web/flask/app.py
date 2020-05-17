from flask import Flask,render_template
import couchdb

app = Flask(__name__)
couch = couchdb.Server('http://admin:admin123@172.26.132.238:4000//')  # connect to couchdb

@app.route('/')
def homepage():
    return render_template('Food_UI.html')

# return the data about final_food database
@app.route('/food')
def get_food_db():
    db_food = couch['final_food']  # access to database 'final_food'
    dict = {}
    for id in db_food:
        doc = db_food[id]
        food_country = doc['country']
        if food_country is not 'england' or food_country is not 'france':
            dict[food_country] = doc['stats']
    return dict

# return the data about final_sport database
@app.route('/sport')
def get_sport_db():
    db_sport = couch['final_sport'] # access the database 'final_sport'
    dict = {}
    for id in db_sport:
        doc = db_sport[id]
        sport = doc['sport']
        stats = doc['stats']
        dict[sport] = stats
    return dict

# return the data about location_time_summary database
@app.route('/sleep')
def get_sleep_db():
    location_time_summary_db = couch['location_time_summary']
    average_person_tweet_view = location_time_summary_db.view('myViews/avarage_person_tweet')
    suburb_median_age = location_time_summary_db.view('myViews/suburb_median_age')

    dict = {}
    for item in average_person_tweet_view:
        if item.value is not None and item.key.lower() != 'west melbourne':
            suburb = item.key.lower()
            average_person_tweet = item.value
            dict[suburb] = {}
            dict[suburb]['average_person_tweet'] = average_person_tweet

    for item in suburb_median_age:
        suburb = item.key.lower()
        median_age = item.value
        if suburb in dict:
            dict[suburb]['median_age'] = median_age
    return dict

if __name__ == '__main__':
    app.run()
