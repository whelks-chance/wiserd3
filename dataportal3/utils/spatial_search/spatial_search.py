from dataportal3 import models

__author__ = 'ubuntu'


def find_intersects(geography_wkt):

    geometry_columns = [
        {
            'table_name': 'pcode',
            'geometry_column': 'geom',
            'table_model': models.Pcode
        }
    ]

    found_intersects = {}

    for geoms in geometry_columns:
        f_table_name = str(geoms['table_name'])
        f_geometry_column = geoms['geometry_column']

        survey_data = {}
        survey_data['areas'] = []

        spatial_layer_table = geoms['table_model']

        area_names = spatial_layer_table.objects.using('new').extra(
            select={
                'geometry': 'ST_Intersects(ST_Transform(ST_GeometryFromText("' + geography_wkt + '", 27700), 4326), ' + f_geometry_column +')'
            }
        ).values_list('label', flat=True)

        link_table = models.SpatialSurveyLink.objects.filter(geom_table_name=f_table_name)

        link_table_surveys = link_table.distinct('survey')
        print link_table_surveys

        available_options = {}
        for found in link_table:
            if found.survey.identifier not in available_options:
                available_options[found.survey.identifier] = []
            available_options[found.survey.identifier].append(found.data_name)

        found_intersects[f_table_name] = {
            'table_options': available_options,
            'intersects': area_names
        }

    return found_intersects


def get_data_for_regions(survey, data_name, regions):

    print 'survey', survey
    print 'data_name', data_name
    print 'regions', len(regions)

    found_model = models.SpatialSurveyLink.objects.get(survey__identifier=survey, data_name=data_name)

    print found_model

    all_spatial_data = found_model.regional_data

    for region in regions:
        try:
            found_region_data = all_spatial_data[region.replace()]
            print region, found_region_data
        except:
            try:
                found_region_data = all_spatial_data[region.replace(' ', '')]
                print region, found_region_data, '*'
            except:
                print 'missing', region

    data = {}


    return data

