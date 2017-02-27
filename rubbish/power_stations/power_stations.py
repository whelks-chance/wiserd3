# coding=utf-8
import json
import os
import pprint

from django.contrib.gis.geos import GEOSGeometry

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiserd3.settings')
import django
django.setup()

from dataportal3 import models
from wiserd3 import settings


a = {
    'Power Stations': [
        {
            'type': 'Nuclear',
            'items': [
                {
                    'name': 'Trawsfynydd',
                    'location': '-3.94843888888889,52.9248638888889,0',
                    'output': '470 MW',
                    'notes': '(Decommissioned in 1991)'
                },
                {
                    'name': 'Wylfa',
                    'location': '-4.48333333333333,53.4166666666667,0',
                    'output': '980 MW',
                    'notes': '(Decommissioned in 2015)'
                },
            ]
        },

        {
            'type': 'Coal - fired',
            'items': [
                {
                    'name': 'Aberthaw',
                    'location': '-3.405,51.3872222222222,0',
                    'output': '1500 MW',
                    'notes': ''
                },
                {
                    'name': 'Uskmouth B',
                    'location': '-2.97055555555556,51.5491666666667,0',
                    'output': '393 MW',
                    'notes': ''
                },
                {
                    'name': 'Carmarthen Bay',
                    'location': '',
                    'output': '360 MW',
                    'notes': '(Decommissioned in 1984)'
                },
            ]
        },

        {
            'type': 'Gas - fired( or combined gas / coal)',
            'items': [
                {
                    'name': 'Baglan Bay',
                    'location': '-3.82972222222222,51.6197222222222,0',
                    'output': '870 MW',
                    'notes': ''
                },
                {
                    'name': 'Barry',
                    'location': '-3.22861111111111,51.4080555555556,0',
                    'output': '245 MW',
                    'notes': ''
                },
                {
                    'name': 'Connah\'s Quay',
                    'location': '',
                    'output': '1380 MW',
                    'notes': 'Originally coal-fired PF, 6x Parsons 30 MW turbines. Commissioned 1955.[citation needed]'
                },
                {
                    'name': 'Deeside',
                    'location': '-3.03388888888889,53.2338888888889,0',
                    'output': '500 MW',
                    'notes': ''
                },
                {
                    'name': 'Pembroke',
                    'location': '-4.98833333333333,51.6830555555556,0',
                    'output': '2000 MW',
                    'notes': '(planning approved 2009) operational 2012'
                },
                {
                    'name': 'Severn',
                    'location': '-2.97638888888889,51.5477777777778,0',
                    'output': '824 MW',
                    'notes': ''
                },
                {
                    'name': 'Shotton',
                    'location': '-3.03277777777778,53.2338888888889,0',
                    'output': '210 MW',
                    'notes': 'CHP(currently decommissioned)'
                },
                {
                    'name': 'BioGen Gwyriad',
                    'location': '-2.993057,53.047741,0',
                    'output': '3.5 MW',
                    'notes': 'biogas'
                },
            ]
        },

        {
            'type': 'Hydro - electric',
            'items': [
                {
                    'name': 'Dinorwig',
                    'location': '-4.11388888888889,53.1186111111111,0',
                    'output': '1728 MW',
                    'notes': '(pumped storage)'
                },
                {
                    'name': 'Ffestiniog',
                    'location': '-3.96888888888889,52.9808333333333,0',
                    'output': '360 MW',
                    'notes': '(pumped storage)'
                },
                {
                    'name': 'Rheidol',
                    'location': '-3.9,52.3961111111111,0',
                    'output': '49 MW',
                    'notes': ''
                },
                {
                    'name': 'River Tawe Swansea Bay barrage',
                    'location': '-3.92888888888889,51.6161111111111,0',
                    'output': '',
                    'notes': ''
                },
            ]
        },

        {
            'type': 'Wind power',
            'items': [
                {
                    'name': 'Alltwalis Wind Farm',
                    'location': '-4.25083333333333,51.9733333333333,0',
                    'output': '23 MW',
                    'notes': ''
                },
                {
                    'name': 'Carno wind farm',
                    'location': '-3.60027777777778,52.5502777777778,0',
                    'output': '49 MW',
                    'notes': ''
                },
                {
                    'name': 'Cefn Croes',
                    'location': '-3.75083333333333,52.405,0',
                    'output': '58.5 MW',
                    'notes': ''
                },
                {
                    'name': 'Moel Maelogen',
                    'location': '-3.72361111111111,53.1352777777778,0',
                    'output': '14.3 MW',
                    'notes': ''
                },
                {
                    'name': 'North Hoyle Offshore Wind Farm',
                    'location': '-3.4,53.4333333333333,0',
                    'output': '60 MW',
                    'notes': ''
                },
                {
                    'name': 'Rhyl Flats',
                    'location': '-3.65,53.3666666666667,0',
                    'output': '90 MW',
                    'notes': ''
                },
                {
                    'name': 'Gwynt y Môr',
                    'location': '-3.58333333333333,53.45,0',
                    'output': '576 MW',
                    'notes': '(consent granted 2008, construction began 2011)'
                },
            ]
        },
    ]
}


class PowerStations:
    def __init__(self):
        pass

    def record(self):
        for s in a['Power Stations']:
            station_type = s['type']

            for i in s['items']:
                new_ps = models.PowerStation()
                new_ps.name = i['name']
                new_ps.type = station_type
                new_ps.output = i['output']
                new_ps.notes = i['notes']
                new_ps.location = i['location']

                new_ps.save()

    def do_geoms(self):
        for ps in models.PowerStation.objects.all():
            assert isinstance(ps, models.PowerStation)

            coords = ps.location.split(',')

            if len(coords) > 1:
                ps.geom = GEOSGeometry('POINT({} {})'.format(coords[0], coords[1]))

                ps.save()


if __name__ == "__main__":

    # list_to_be_sorted = settings.M4W_SEARCH_LAYER_UUIDS[0]['item_list']
    # newlist = sorted(list_to_be_sorted, key=lambda k: k['description'])
    #
    # print pprint.pformat(newlist, indent=4)
    # print json.dumps(newlist, indent=4)


    ps = PowerStations()
    ps.record()
    ps.do_geoms()
