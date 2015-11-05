from dataportal3 import models

__author__ = 'ubuntu'


def find_intersects(geography_wkt):

    geometry_columns = [
        {
            'table_name': 'spatialdata_aefa',
            'geometry_column': 'geom',
            'table_model': models.SpatialdataAEFA
        },
        {
            'table_name': 'spatialdata_police',
            'geometry_column': 'geom',
            'table_model': models.SpatialdataPolice
        },
        {
            'table_name': 'spatialdata_pcode',
            'geometry_column': 'geom',
            'table_model': models.SpatialdataPostCode
        },
        {
            'table_name': 'spatialdata_parl',
            'geometry_column': 'geom',
            'table_model': models.SpatialdataParl
        },
        {
            'table_name': 'spatialdata_msoa',
            'geometry_column': 'geom',
            'table_model': models.SpatialdataMSOA
        },
        {
            'table_name': 'spatialdata_lsoa',
            'geometry_column': 'geom',
            'table_model': models.SpatialdataLSOA
        },
        {
            'table_name': 'spatialdata_fire',
            'geometry_column': 'geom',
            'table_model': models.SpatialdataFire
        },
        {
            'table_name': 'spatialdata_ua',
            'geometry_column': 'geom',
            'table_model': models.SpatialdataUA
        },
    ]

    return_data = {}
    found_intersects = {}
    survey_boundaries = {}

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

        # link_table_surveys = link_table.distinct('survey')
        # print link_table_surveys

        available_options = {}
        for found in link_table:

            if found.survey.identifier not in survey_boundaries:
                survey_boundaries[found.survey.identifier] = []

            if found.boundary_name not in survey_boundaries[found.survey.identifier]:
                survey_boundaries[found.survey.identifier].append(found.boundary_name)

            if found.survey.identifier not in available_options:
                available_options[found.survey.identifier] = []
            available_options[found.survey.identifier].append(found.data_name)

        found_intersects[f_table_name] = {
            'table_options': available_options,
            'intersects': area_names
        }

    return_data['survey_boundaries'] = survey_boundaries
    return_data['boundary_surveys'] = found_intersects
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

