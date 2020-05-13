import couchdb
import json
import time
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


couch = couchdb.Server('http://admin:admin123@172.26.132.238:4000//')  # connect to couchdb
# couch.create('location_time')   #create database

db = couch['imported_twitter_melbourne']  # access "imported_twitter_melbourne" database
location_time_dataset = couch['location_time']  # access "clean_data" database

# access design document view of "imported_twitter_melbourne" database
imported_view = db.view('_design/imported/_view/coordinate')


def check_suburb(coordinates):
    # return the name of suburb that contains the coordinate

    name = ''
    for feature in suburb_info_json['features']:
        lat_lon_list = feature['geometry']['coordinates'][0][0]  # the coordinates of a suburb
        suburb_name = feature['properties']['name']  # the name of the suburb
        polygon = Polygon(lat_lon_list)
        point = Point( coordinates[0], coordinates[1] )
        if polygon.contains(point):  # if the point is in the polygon
            name = suburb_name  # assign suburb name to name, otherwise name = ''

    return name

# return the hour of the time
def find_hour(date_time):
    time_origin = time.strptime(date_time, '%a %b %d %H:%M:%S +0000 %Y')
    time_new = time.strftime('%Y/%m/%d %H', time_origin)

    date_hour = time_new.split(' ')
    # date = date_hour[0]
    hour = date_hour[1]
    return hour

if __name__ == '__main__':

    with open( 'data4634792039184191815.json' ) as polygon_file:  # open the file of suburb coordinates
        suburb_info_json = json.load( polygon_file )
        polygon_file.close()

    print('start')
    for item in imported_view:
        date_time = db[item.id]['created_at']
        if len(check_suburb(item.key)) > 0:  # if name = suburb name
            doc = {
                '_id': item.id,
                'suburb': check_suburb(item.key),
                'text': item.value,
                'time': date_time,
                'hour': find_hour(date_time)
            }
            try:
                location_time_dataset.save(doc)  # insert formatted information into clean_data database
            except:
                print( "Data exist!" )

    print( "Mission Complete!" )