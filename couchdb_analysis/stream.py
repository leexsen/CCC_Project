import couchdb
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import csv


couch = couchdb.Server('http://admin:admin123@172.26.132.59:5984//')  # connect to couchdb

db = couch['twitter_stream_data_melbourne']  # access to database 'twitter_stream_data_melbourne', 可更改其他数据库名字

with open('polygon_file.json') as polygon_file:  # open the file of suburb coordinates，Inner Melbourne所有区域地图坐标
    suburb_info_json = json.load(polygon_file)


def check_suburb(coordinate):
    # return the name of suburb that contains the coordinate

    name = ''
    for feature in suburb_info_json['features']:
        lat_lon_list = feature['geometry']['coordinates'][0][0]  # the coordinates of a suburb
        suburb_name = feature['properties']['name']  # the name of the suburb
        polygon = Polygon(lat_lon_list)
        point = Point(coordinate[0], coordinate[1])
        if polygon.contains(point):
            name = suburb_name

    return name


def write_suburb(coordinates, content):
    # write the suburb_name and the tweet text into suburb_file

    if len(check_suburb(coordinates)) > 0:
        csv_write.writerow([check_suburb(coordinate), content])


if __name__ == '__main__':

    database = '_design/Melbourne/_view/coordinates'  # couchdb 相关view地址，可改其他

    suburb_file = open('suburb_file.csv', 'a', newline='')  # open suburb_file，可改新文件名
    csv_write = csv.writer(suburb_file, dialect='excel')

    for item in db.view(database):
        coordinate = item.key
        text = item.value
        write_suburb(coordinate, text)  # write information to file

    suburb_file.close()
    print("Completed!")
