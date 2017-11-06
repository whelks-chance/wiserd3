import os
import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")
import django
django.setup()

from cancommute import models
from django.contrib.gis.geos import GEOSGeometry, LineString

# <generic:Series>
# 	<generic:SeriesKey>
# 		<generic:Value concept="GEO" value="1001113"/>
# 		<generic:Value concept="POWGEO" value="1001113"/>
# 		<generic:Value concept="Sex" value="1"/>
# 	</generic:SeriesKey>
#
# 	<generic:Obs>
# 		<generic:Time>2011</generic:Time>
# 		<generic:ObsValue value="80"/>
# 	</generic:Obs>
# </generic:Series>


def do_the_import():
    from xml.etree import ElementTree as ET

    parser = ET.iterparse('./data/Generic_99-012-X2011032.xml')

    all_data = []
    for event, element in parser:
        if element.tag == '{http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic}Series':

            data = dict()

            for el2 in element.getchildren():
                # print 'el2', el2
                # print 'tag', el2.tag
                # print 'attrib', el2.attrib
                print '\n**'

                if el2.tag == '{http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic}SeriesKey':

                    for el3 in el2.getchildren():
                        print 'el3 tag', el3.tag
                        print 'el3 attrib', el3.attrib

                        if el3.attrib.get('value'):
                            if el3.attrib.get('concept'):
                                data[el3.attrib['concept']] = el3.attrib['value']

                if el2.tag == '{http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic}Obs':

                    for el3 in el2.getchildren():
                        print 'el3 tag', el3.tag
                        print 'el3 attrib', el3.attrib

                        if el3.attrib.get('value'):
                            if el3.attrib.get('concept'):
                                data[el3.attrib['concept']] = el3.attrib['value']
                            else:
                                data.update(el3.attrib)

                    # if el3.tag == '{http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic}Value':
                    #     data[el3.attrib['concept']] = el3.attrib['value']
                    #
                    # if el3.tag == '{http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic}Obs':
                    #     data[el3.attrib['concept']] = el3.attrib['value']

            all_data.append(data)

            # do something with this element
            # then clean up
            element.clear()
            print '\n\n'

    print pprint.pformat(all_data)

    for d in all_data:
        print '\n'

        origin_model = models.CanadaShape.objects.get(csduid=d['GEO'])
        destination_model = models.CanadaShape.objects.get(csduid=d['POWGEO'])

        m, created = models.Route.objects.get_or_create(
            origin=origin_model,
            destination=destination_model
        )

        print 'route', m, created

        origin_geom = origin_model.geom
        destination_geom = destination_model.geom

        if created or m.geom is None:
            # print GEOSGeometry(origin_geom).point_on_surface
            # print type(GEOSGeometry(destination_geom).point_on_surface)

            line = LineString([
                GEOSGeometry(origin_geom).point_on_surface.coords,
                GEOSGeometry(destination_geom).point_on_surface.coords
            ])
            m.geom = line

            print line

        if d.get('Sex'):
            if d['Sex'] == '1':
                m.total = d['value']
            if d['Sex'] == '2':
                m.males = d['value']
            if d['Sex'] == '3':
                m.females = d['value']
        m.save()


def find_destinations():
    all_routes = models.Route.objects.all()

    dest_ids = []
    for r in all_routes:
        assert isinstance(r, models.Route)
        dest_ids.append(r.destination.csduid)

    destinations = models.CanadaShape.objects.filter(csduid__in=dest_ids)

    print destinations.count()
    print pprint.pformat(list(destinations))

# do_the_import()
find_destinations()