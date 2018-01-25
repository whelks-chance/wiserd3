import os
import json
import geojson
# from school_meals.py import FreeSchoolMeals
filepath= '/home/kdickson/PycharmProjects/wiserd3/rubbish/schools/schools_ext'
slash= '/'
filelist= []
# school_data= FreeSchoolMeals.get_school_data()

for root, dir, files in os.walk(filepath):
    for file in files:
        filelist.append(file)

print filelist

school_data= []

for file in filelist:
    fullfilepath= filepath+slash+file
    # with open(filepath+slash+file) as jsonfile:
    print fullfilepath
    with open(fullfilepath) as data:
        json_data = json.loads(data.read())
    print json_data['lat']
    # print json.load(filepath+slash+file)
    json_lat = json_data['lat']
    json_lng = json_data['lon']
    json_schoolname = json_data['schName']
    json_schoolcode = json_data ['schoolCode']
    json_type = json_data ['schTypeEnglish']
    json_medium = json_data ['schLanguageEnglish']
    indicatorlist= json_data ['lstSubjectsIndicators']
    for i in indicatorlist:
        lstseries= i['lstSeries']
        for j in lstseries:
            if j['subjectCode'] == 'FSM3' and j['nameEnglish'] == 'School':
                json_fsmyear = j['years']
                json_fsmdata = j['data']
                print json_fsmdata
                json_fsmdata = json_fsmdata[-1]
                print json_fsmdata
