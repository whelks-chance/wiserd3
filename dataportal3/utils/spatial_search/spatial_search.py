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
    intersect_data = []

    for geoms in geometry_columns:
        try:

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
            print 'Cant find spatial table', str(e69342758432), type(e69342758432)
            pass

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

