# coding=utf-8
import json
import os
import csv
import pprint
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiserd3.settings')
import django
django.setup()
# from django.contrib.gis.geos import Point
from dataportal3 import models
from dataportal3.utils.userAdmin import get_anon_user, get_request_user


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
    categories = []
    for idx, d in enumerate(ds):
        d['geom'] = "POINT ({} {})".format(d['x'], d['y'])
        categories.append(d['category'].strip())
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

    ns, created = models.NomisSearch.objects.get_or_create(
        uuid = 'WMHpoints',
        user=get_request_user()
    )
    ns.name = 'WMHpoints'
    ns.uuid = 'WMHpoints'
    ns.dataset_id = 'WMHpoints'
    ns.geography_id = ''
    ns.search_attributes = {}
    ns.display_attributes = {
        "bin_num": "5",
        "bin_type": "q",
        "colorpicker": "YlGnBu",
        "point_icon": "fa-bolt",
        "remote_value_key": "category",
    }
    ns.display_fields = {}
    ns.search_type = models.SearchType.objects.get(name='LocalResearch')
    ns.save()

    for category in set(categories):
        ns, created = models.NomisSearch.objects.get_or_create(
            uuid = 'WMHpoints_{}'.format(category.replace(' ', '_')),
            user=get_request_user()
        )
        ns.name = 'WMHpoints_{}'.format(category)
        ns.dataset_id = 'WMHpoints'
        ns.geography_id = ''
        ns.search_attributes = {}
        ns.display_attributes = {
            "bin_num": "5",
            "bin_type": "q",
            "colorpicker": "YlGnBu",
            "point_icon": "fa-bolt",
            "remote_value_key": "category",
            "filter": category
        }
        ns.display_fields = {}
        ns.search_type = models.SearchType.objects.get(name='LocalResearch')
        ns.save()


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
