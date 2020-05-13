data4634792039184191815.json
- polygon coordinates of suburbs in Inner Melbourne

imported_to_clean_data.py
- obtain data from imported_twitter_melbourne View
- filter the coordinates which included in Inner Melbourne and identify the suburb it belongs to
- save in clean_data with the format {'_id', 'suburb_name', 'text'} 

stream.py
- obtain data form CouchDB View
- identify the which suburb each belongs to
- write the name of suburb and the corresponding text to suburb_file.csv

imported_to_location_time.py
- obtain data from imported_twitter_melbourne View
- filter the coordinates which included in Inner Melbourne and identify the suburb it belongs to
- save in location_time database with the format {'_id', 'suburb', 'hour', 'time'} 

location_time_summary.py
- get data form location_time database and population_age.json
- count tweets' created time
- save data to loaction_time_summay database with format{'_id', 'suburb', 'hour', 'persons_num', 'median_persons_age'}

population_age.json
- record the population number and median age of each suburb in Melbourne

suburb_file.csv
- {suburb_name}{text}
