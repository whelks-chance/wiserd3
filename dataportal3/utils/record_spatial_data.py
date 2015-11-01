import json
import os
import pprint
from django.apps import apps
# from django.core.exceptions import ObjectDoesNotExist
# from django.db import connections, ConnectionRouter, DEFAULT_DB_ALIAS
from django.db import connections

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")
import django
django.setup()

# from old import survey_models as old_models
from dataportal3 import models as new_models

tablenames = [
    "x_sid_liw2007_lsoa_", "x_sid_liw2007_police_", "x_sid_liwhh2004_fire_", "x_sid_liw2007_pcode_",
    "x_wisid_ad_plasc_ethnic_2004_ua_", "x_sid_liwhh2004_aefa_", "x_sid_liwhh2004_lsoa_",
    "x_sid_liwhh2005_parl_", "x_sid_liwhh2005_lsoa_", "x_sid_liwhh2005_police_", "x_sid_liwhh2005_pcode_",
    "x_sid_liwhh2005_ua_", "x_sid_liwhh2006_aefa_", "x_sid_liwhh2006_pcode_", "x_sid_liwps2004_lsoa_",
    "x_sid_liwps2004_pcode_", "x_sid_liw2007_ua_", "x_sid_liw2007_parl_", "x_sid_liwhh2004_pcode_",
    "x_sid_liwhh2006_fire_", "x_sid_liwhh2006_lsoa_", "x_sid_liwps2004_parl_", "x_sid_liwps2004_police_",
    "x_sid_liw2007_aefa_", "x_sid_liwhh2004_parl_", "x_sid_liwhh2004_police_", "x_sid_liwhh2004_ua_",
    "x_sid_whs2007_03_ua_", "x_sid_liwhh2005_aefa_", "x_sid_whs0306aq1_ua_", "x_sid_liwhh2005_fire_",
    "x_sid_whs2009_03_ua_", "x_sid_liwhh2006_parl_", "x_sid_whs0306aq2_ua_", "x_sid_liwhh2006_police_",
    "x_sid_whs2008_1315_ua_", "x_sid_whs2007_1315_ua_", "x_sid_liwhh2006_ua_", "x_sid_whs0306aq3_ua_",
    "x_sid_liwps2004_aefa_", "x_sid_liwps2004_fire_", "x_sid_whs0306cq1_ua_", "x_sid_liwps2004_ua_",
    "x_sid_whs2007_412_ua_", "x_sid_wersmq2004_wales_", "x_sid_whs0306cq2_ua_", "x_sid_whshh03063_ua_",
    "x_sid_whs0306cq3_ua_", "x_sid_whs2008_412_ua_", "x_sid_whs2007aq_ua_", "x_sid_whs2009aq_ua_",
    "x_sid_whs2009_1315_ua_", "x_sid_whs2008_03_ua_", "x_sid_whs2008aq_ua_", "x_sid_whshh03062_ua_",
    "x_sid_whs2009_412_ua_", "x_sid_whshh03061_ua_", "x_sid_whshh2007_ua_", "x_sid_whshh2009_ua_"]

# grey / admin data?

#     "x_wisid_ad_plasc_ss1115welsh_2004_ua_", "x_wisid_ad_plasc_ethnic_2003_ua_",
#     "x_wisid_ad_plasc_identity_2005_ua_", "x_wisid_ad_plasc_ethnic_2005_ua_", "x_sid_liw2007_fire_",
#     "x_wisid_ad_plasc_ethnic_2006_ua_", "x_wisid_ad_plasc_identity_2006_ua_",
#     "x_wisid_ad_plasc_ethnic_2007_ua_", "x_wisid_ad_plasc_ss1115welsh_2009_ua_",
#     "x_wisid_ad_plasc_ss1115welsh_2005_ua_", "x_wisid_ad_plasc_ethnic_2008_ua_",
#     "x_wisid_ad_plasc_identity_2007_ua_", "x_wisid_ad_plasc_ethnic_2009_ua_",
#     "x_wisid_ad_plasc_identity_2003_ua_", "x_wisid_ad_plasc_identity_2008_ua_",
#     "x_wisid_ad_plasc_identity_2004_ua_", "x_wisid_ad_plasc_ss1115welsh_2006_ua_",
#     "x_wisid_ad_plasc_identity_2009_ua_", "x_wisid_ad_plasc_ss1115welsh_2003_ua_",
#     "x_wisid_ad_plasc_ss1115welsh_2007_ua_", "x_wisid_ad_plasc_ss1115welsh_2008_ua_", "x_sid_whshh2008_ua_"
# ]


for table_name in tablenames:
    if 'pcode' in table_name:
        print ''
        print table_name

        survey_id_segment = table_name.split('_')[2]
        print survey_id_segment

        survey = new_models.Survey.objects.filter(surveyid__icontains=survey_id_segment)[0]

        print survey

        # spatial_table_model = apps.get_model(app_label='old', model_name=table_name.replace('_', ''))
        # fields = spatial_table_model._meta.get_fields()
        #
        # print fields

        cursor = connections['survey'].cursor()
        cursor.execute("select column_name from information_schema.columns where table_name = %s", [table_name])
        column_names = cursor.fetchall()
        # print column_names

        cursor3 = connections['survey'].cursor()
        cursor3.execute("select area_name from " + table_name, [])
        regions = cursor3.fetchall()
        print regions[:20]

        for column in column_names:
            column_header = str(column[0])
            if column_header != 'table_pk' and column_header != 'the_geom' and column_header != 'area_name':

                print column_header

                cursor2 = connections['survey'].cursor()
                cursor2.execute("select " + column_header + " from " + table_name, [])

                data = cursor2.fetchall()
                print len(data)
                print len(regions)

                regions_with_data = {}
                for place_itr in range(len(regions)):
                    regions_with_data[regions[place_itr][0]] = data[place_itr][0]

                new_survey_link = new_models.SpatialSurveyLink()
                new_survey_link.survey = survey
                new_survey_link.data_name = column_header
                new_survey_link.geom_table_name = 'pcode'
                new_survey_link.regional_data = regions_with_data
                new_survey_link.save()

