import os
# import imp
# from geojson import Point, Feature, FeatureCollection, dumps
import json

# geojson = imp.load_source('geojson', '/home/ianh/venv/local/lib/python2.7/site-packages/geojson/__init__.py')
# foo.MyClass()

# from school_meals.py import FreeSchoolMeals
filepath = './schools_ext'
slash = '/'
filelist = []
# school_data= FreeSchoolMeals.get_school_data()

for root, dir, files in os.walk(filepath):
    for file in files:
        filelist.append(file)

print filelist

school_data= []
all_points = []

for file in filelist:
    properties = {}

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

                properties['json_fsmyear'] = json_fsmyear
                properties['json_fsmdata'] = json_fsmdata
                properties['json_fsmdata'] = json_fsmdata
                properties['json_schoolname'] = json_schoolname
                properties['json_type'] = json_type
                properties['json_medium'] = json_medium

#     all_points.append(
#         Feature(
#             geometry=Point((json_lng, json_lat)),
#             properties=properties
#         )
#     )
#
# print(all_points)
#
# fc = FeatureCollection(all_points)
# print(dumps(fc))
#
# with open('schools_geo.json', 'w') as geo1:
#     geo1.write(dumps(fc, indent=4))
