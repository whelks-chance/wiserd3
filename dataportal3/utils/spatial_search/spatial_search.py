import os
from django.contrib.gis.geos import GEOSGeometry
from django.db import connections
from dataportal3 import models
from wiserd3.settings import TOPOJSON_DIR

__author__ = 'ubuntu'

# TODO replace table_name with the model_instance._meta.db_table
geometry_columns = [
    {
        'table_name': 'spatialdata_aefa',
        'geometry_column': 'geom',
        'label': 'label',
        'table_model': models.SpatialdataAEFA,
        'name': 'AEFA'
    },
    {
        'table_name': 'spatialdata_police',
        'geometry_column': 'geom',
        'label': 'label',
        'table_model': models.SpatialdataPolice,
        'name': 'Police'
    },
    {
        'table_name': 'spatialdata_pcode',
        'geometry_column': 'geom',
        'label': 'label',
        'table_model': models.SpatialdataPostCode,
        'name': 'Postcode'
    },
    {
        'table_name': 'spatialdata_parl',
        'geometry_column': 'geom',
        'table_model': models.SpatialdataParl,
        'name': 'Parliamentary Constituencies 2011',
        'geog_short_code': 'parl2011',
        'region_id': '2092957700TYPE460',
        'topojson_file': os.path.join(TOPOJSON_DIR, '13Wales_parlconstit_2011/output-fixed-1-4326.json'),
        'topojson_file_high': os.path.join(TOPOJSON_DIR, '13Wales_parlconstit_2011/output-fixed-1-4326.json')
    },
    # {
    #     # FIXME REMOVE ME horribly broken
    #     'table_name': 'spatialdata_nawer',
    #     'geometry_column': 'geom',
    #     'table_model': models.SpatialdataParl,
    #     'name': 'Parliamentary',
    #     'geog_short_code': 'region',
    #     'region_id': '2092957700TYPE460',
    #     'topojson_file': os.path.join(TOPOJSON_DIR, 'AssemblyRegions/output-fixed-1-ms.json'),
    #     'topojson_file_high': os.path.join(TOPOJSON_DIR, 'AssemblyRegions/output-fixed-ms.json')
    # },
    {
        'table_name': 'spatialdata_msoa',
        'geometry_column': 'geom',
        'table_model': models.SpatialdataMSOA,
        'name': 'MSOA'
    },
    {
        'table_name': 'spatialdata_lsoa',
        'geometry_column': 'geom',
        'label': 'zonecode',
        'table_model': models.SpatialdataLSOA,
        'name': 'LSOA',
        'geog_short_code': 'lsoa',
        'region_id': '2092957700TYPE298',
        'topojson_file': os.path.join(TOPOJSON_DIR, '11Wales_lsoa_2011/output-fixed-1-k.json'),
        'topojson_file_high': os.path.join(TOPOJSON_DIR, '11Wales_lsoa_2011/output-fixed-1-k.json')
    },
    {
        'table_name': 'spatialdata_fire',
        'geometry_column': 'geom',
        'label': 'label',
        'table_model': models.SpatialdataFire,
        'name': 'Fire'
    },
    {
        'table_name': 'spatialdata_ua',
        'geometry_column': 'geom',
        'label': 'label',
        'table_model': models.SpatialdataUA,
        'name': 'Unitary Authority',
        'geog_short_code': 'ua',
        'region_id': '2092957700TYPE464',
        'topojson_file': os.path.join(TOPOJSON_DIR, '14Wales_lad_unitaryauthority_2011/output-fixed-1.json'),
        'topojson_file_high': os.path.join(TOPOJSON_DIR, '14Wales_lad_unitaryauthority_2011/output-fixed-1.json')
    },
    {
        'table_name': 'pcode_s',
        'geometry_column': 'geom',
        'label': 'label',
        'table_model': models.SpatialdataPostCodeS,
        'name': 'Postcode Sector',
        'geog_short_code': 'pcode',
        'region_id': '2092957700TYPE276',
        'topojson_file': os.path.join(TOPOJSON_DIR, '06Wales_pcs_2012/output-fixed-1.json'),
        'topojson_file_high': os.path.join(TOPOJSON_DIR, '06Wales_pcs_2012/output-fixed.json')
    },
    {
        'table_name': 'ua_2',
        'geometry_column': 'geom',
        'label': 'code',
        'table_model': models.SpatialdataUA_2,
        'name': 'Unitary Authority 2'
    },
    # {
    #     'table_name': 'nawer',
    #     'geometry_column': 'geom',
    #     'label': 'code',
    #     'geog_short_code': 'region',
    #     # FIXME wrong region_id
    #     'region_id': '2092957700TYPE460',
    #     'table_model': models.SpatialdataNawer,
    #     'name': 'National Assembly Region',
    #     'topojson_file': os.path.join(TOPOJSON_DIR, 'AssemblyRegions/output-fixed-1-ms.json'),
    #     'topojson_file_high': os.path.join(TOPOJSON_DIR, 'AssemblyRegions/output-fixed-ms.json')
    # },
    {
        'table_name': models.SpatialdataNAWregions._meta.db_table,
        'geometry_column': 'geom',
        'label': 'code',
        'geog_short_code': 'region',
        # FIXME wrong region_id
        'region_id': '2092957700TYPE273',
        'table_model': models.SpatialdataNAWregions,
        'name': 'National Assembly Region',
        'topojson_file': os.path.join(TOPOJSON_DIR, 'AssemblyRegions2/output-fixed-1.json'),
        'topojson_file_high': os.path.join(TOPOJSON_DIR, 'AssemblyRegions2/output-fixed-1.json')
    },
    # {
    #     'table_name': models.SpatialdataConstituency._meta.db_table,
    #     'geometry_column': 'geom',
    #     'label': 'code',
    #     'geog_short_code': 'constituency',
    #     # FIXME wrong region_id
    #     'region_id': '2092957700TYPE460',
    #     'table_model': models.SpatialdataConstituency,
    #     'name': 'National Assembly Constituency',
    #     'topojson_file': os.path.join(TOPOJSON_DIR, 'ConstituencyProfile/output-fixed-1-const-prof.json'),
    #     'topojson_file_high': os.path.join(TOPOJSON_DIR, 'ConstituencyProfile/output-fixed-1-const-prof.json')
    # },
    {
        'table_name': models.SpatialdataNAWConstituency._meta.db_table,
        'geometry_column': 'geom',
        'label': 'code',
        'geog_short_code': 'constituency',
        # FIXME wrong region_id
        'region_id': '2092957700TYPE460',
        'table_model': models.SpatialdataNAWConstituency,
        'name': 'National Assembly Constituency',
        'topojson_file': os.path.join(TOPOJSON_DIR, 'AssemblyConstituencys2/output-fixed-1.json'),
        'topojson_file_high': os.path.join(TOPOJSON_DIR, 'AssemblyConstituencys2/output-fixed-1.json')
    },
    {
        'table_name': models.SpatialdataPostCodePoint._meta.db_table,
        'geometry_column': 'geom',
        'label': 'postcode',
        'geog_short_code': 'pcode_point',
        # FIXME wrong region_id
        'region_id': '1234567890',
        'table_model': models.SpatialdataPostCodePoint,
        'name': 'Postcode Points',
        'topojson_file': '/home/ianh/Downloads/shp_files/OSCodePointOpenFeb2016Wales/pprint.json',
        'topojson_file_high': '/home/ianh/Downloads/shp_files/OSCodePointOpenFeb2016Wales/pprint.json',
    },

    # {
    #     'table_name': None,
    #     'geometry_column': None,
    #     'label': None,
    #     'geog_short_code': 'lsoa_pembrokshire_point',
    #     # FIXME wrong region_id
    #     'region_id': '1234567890',
    #     'table_model': None,
    #     'name': 'LSOA Pembrokshire Points',
    #     'topojson_file': '/home/ianh/Downloads/shp_files/LOSAPopCentroids/pprint.json',
    #     'topojson_file_high': '/home/ianh/Downloads/shp_files/LOSAPopCentroids/pprint.json',
    # },

    # {
    #     'table_name': 'spatialdatanawer',
    #     'geometry_column': 'geom',
    #     'label': 'code',
    #     'geog_short_code': 'region',
    #     # FIXME wrong region_id
    #     'region_id': '2092957700TYPE460',
    #     'table_model': models.SpatialdataNawer,
    #     # FIXME wrong name, just remove this thing
    #     'name': 'Parliamentary',
    #     'topojson_file': os.path.join(TOPOJSON_DIR, 'AssemblyRegions/output-fixed-1-ms.json'),
    #     'topojson_file_high': os.path.join(TOPOJSON_DIR, 'AssemblyRegions/output-fixed-ms.json')
    # }
]


def save_map_geom_image(geom_object, name='1'):
    from staticmap.staticmap import StaticMap, Line

    m = StaticMap(1024, 768, 30, 30)

    print type(geom_object)
    print geom_object.num_coords
    print geom_object.boundary
    print geom_object.area

    for coord in geom_object.coords:
        print type(coord)
        print coord
        for point in coord:
            print point

        for i in range(len(coord) - 1):
            print coord[i], coord[i + 1]

            m.add_line(
                Line(((coord[i][0], coord[i][1]),
                      (coord[i + 1][0], coord[i + 1][1])),
                     'blue', 3)
            )

        print coord[len(coord) - 1], coord[0]
        m.add_line(
            Line(((coord[len(coord) - 1][0], coord[len(coord) - 1][1]),
                  (coord[0][0], coord[0][1])),
                 'blue', 3)
        )
    image = m.render()
    image.save('map_{}.png'.format(name))


def find_intersects(geography_wkt):

    return_data = {}
    found_intersects = {}
    survey_boundaries = {}
    intersect_data = []

    # We need a geom object from the WKT
    print geography_wkt
    geom_object = GEOSGeometry(geography_wkt, srid=27700)
    print geom_object

    # It's almost always in the wrong SRID, so transform it
    geom_object = geom_object.transform(4326, clone=True)
    print geom_object

    # geometry_columns is a full list of dicts
    # which define a model, its name and table names
    for geoms in geometry_columns:
        try:

            f_table_name = str(geoms['table_name'])
            f_geometry_column = geoms['geometry_column']
            f_label = 'name'
            if 'label' in geoms:
                f_label = geoms['label']

            print '\n', f_table_name, f_geometry_column, f_label

            survey_data = {}
            survey_data['areas'] = []

            spatial_layer_table = geoms['table_model']

            # area_names_query = spatial_layer_table.objects.using('new').extra(
            #     select={
            #         'geometry': 'ST_Intersects(ST_Transform(ST_GeometryFromText("' + geography_wkt + '", 27700), 4326), ' + f_geometry_column +')'
            #     }
            # )

            variable_column = f_geometry_column
            search_type = 'intersects'
            filter_var = variable_column + '__' + search_type
            area_names_queryset = spatial_layer_table.objects.using('new').all().filter(**{filter_var: geom_object})

            # print 'area_names_query', area_names_queryset.query
            area_names = area_names_queryset.values_list(f_label, flat=True)
            # print list(area_names)
            print len(list(area_names))

            if connections['new'].queries:
                print connections['new'].queries[-1]

            if len(list(area_names)) > 0:
                link_table = models.SpatialSurveyLink.objects.filter(geom_table_name=f_table_name).prefetch_related('survey')

                # link_table_surveys = link_table.distinct('survey')
                # print link_table_surveys

                intersect_data.append({
                    'table_name': f_table_name,
                    'intersecting_regions': list(area_names),
                })

                available_options = {}
                for found in link_table:

                    # Create empty list of boundaries if we dont have one for this survey yet
                    if found.survey.identifier not in survey_boundaries:
                        survey_boundaries[found.survey.identifier] = []

                    # Append to list of boundary names "Police', 'AEFA' if not already there
                    if found.boundary_name not in survey_boundaries[found.survey.identifier]:
                        survey_boundaries[found.survey.identifier].append(found.boundary_name)

                    # TODO this makes crazy assumptions
                    if found.survey.identifier not in available_options:
                        available_options[found.survey.identifier] = []

                    # Data available for this geography, for this survey
                    available_options[found.survey.identifier].append(found.data_name)

                found_intersects[f_table_name] = {
                    'table_options': available_options,
                    'intersects': list(area_names)
                }
        except Exception as e69342758432:
            print '**starterror**\nSpatial search error: ', str(e69342758432), type(e69342758432) , '\n**enderror**\n'
            pass
    # print connections['new'].queries

    print 'intersect_data', intersect_data
    return_data['survey_boundaries'] = survey_boundaries
    return_data['boundary_surveys'] = found_intersects
    return_data['intersects'] = intersect_data
    return return_data


def get_data_for_regions(survey, data_name, regions):

    data = {}

    print 'survey', survey
    print 'data_name', data_name
    print 'regions', len(regions)

    found_model = models.SpatialSurveyLink.objects.filter(survey__identifier=survey,
                                                          data_name=data_name)
    # for m in found_model:
    #     print m.boundary_name

    found_model = found_model[0]
    print found_model

    all_spatial_data = found_model.regional_data

    found_direct_count = 0
    found_trimed_count = 0
    not_found = 0
    for region in regions:
        try:
            found_region_data = all_spatial_data[region]
            # print region, found_region_data
            found_direct_count += 1
            data[region] = found_region_data
        except:
            try:
                found_region_data = all_spatial_data[region.replace(' ', '')]
                # print region, found_region_data, '*'
                found_trimed_count += 1
                data[region.replace(' ', '')] = found_region_data
            except:
                print 'missing', region
                not_found += 1
    print 'found/trimmed/missing/total', found_direct_count, found_trimed_count, not_found, len(regions)
    return data

