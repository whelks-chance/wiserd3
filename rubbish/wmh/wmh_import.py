# coding=utf-8
import json
import os
import csv
import pprint

# from django.contrib.gis.geos import Point
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiserd3.settings')
import django
django.setup()


def convert_csv_to_json(csv_file):
    reader = csv.reader(open(csv_file, 'r'))
    header = None
    ds = []

    for r in reader:
        if header:
            d = dict()
            for idx, h in enumerate(header):
                if h:
                    d[h] = r[idx]
            ds.append(d)
        else:
            header = r

    print header
    print pprint.pformat(ds)
    fixtures = []
    for idx, d in enumerate(ds):
        d['geom'] = "POINT ({} {})".format(d['x'], d['y'])
        fixtures.append(
            {
                "pk": str(idx),
                "model": "dataportal3.WMHpoints",
                "fields": d
            }
        )

    with open('mining_features.json', 'w') as mhw_fixtures:
        mhw_fixtures.write(json.dumps(fixtures, indent=4))

    from django.core.management import call_command

    call_command('loaddata', 'mining_features.json', app_label='dataportal3', database='new')

if __name__ == "__main__":
    print sys.argv
    print '', 'This program should probably take a CSV file, with headers :'
    print ['community_town', 'coords', 'y', 'x', 'name', 'postcode', 'council_borough', 'memory_of', 'date', 'colliery', 'category', 'description', 'built', 'artist_architect', 'people', 'img_1', 'img_2', 'img_3', 'img_4']
    print ''

    if len(sys.argv) > 1:
        convert_csv_to_json(sys.argv[1])
    else:
        csv_file = 'mining_heritage_formatted.csv'
        convert_csv_to_json(csv_file)
