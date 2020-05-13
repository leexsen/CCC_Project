import couchdb
import itertools
import time
import json

# count the number of hours appeared in each suburb
def countHour(dic, suburb, hour):
    if suburb not in dic:
        dic[suburb] = {}
    else:
        if hour not in dic[suburb]:
            dic[suburb][hour] = 1
        else:
            dic[suburb][hour] += 1


couch = couchdb.Server('http://admin:admin123@172.26.132.238:4000//') #connet to the database server
location_time_db = couch['location_time']
location_time_summary_db = couch['location_time_summary']


dic = {}
start_time = time.time()
# go through the location_time database and count the hours
for id in location_time_db:
    doc = location_time_db[id]
    suburb = doc['suburb'].lower()
    hour = doc['hour']
    countHour(dic, suburb, hour)

# open population_age.json for population and median age data
with open('population_age.json') as population_age_file:
    population_age = json.load(population_age_file)
    population_age_file.close()

# get population and median age data from the file
for feature in population_age['features']:
    properties = feature['properties']
    sa2_name = properties['sa2_name16'].lower()
    persons_num = properties['persons_num']
    median_persons_age = properties['median_persons_age']
    if sa2_name in dic:
        dic[sa2_name]['persons_num'] = persons_num
        dic[sa2_name]['median_persons_age'] = median_persons_age

# delete the previous record in location_time_summary database
for id in location_time_summary_db:
    location_time_summary_db.delete(location_time_summary_db[id])

# save documents to location_time_summary database
for area in dic:
    doc_summary = {'suburb': area}
    doc_summary['hour'] = {}
    for ele in dic[area]:
        if ele is 'persons_num' or ele is 'median_persons_age':
            doc_summary[ele] = dic[area][ele]
        else:
            doc_summary['hour'][ele] = dic[area][ele]
    # print(doc_summary)
    location_time_summary_db.save(doc_summary)

print(dic)
print(time.time() - start_time)