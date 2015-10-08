import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")
import django
django.setup()

__author__ = 'ubuntu'

from old_qual import models as old_qual_models
from dataportal3 import models as new_qual_models

class CreateQualTables():

    def __init__(self):
        pass

    def check_old(self):
        for old_qual_dc in old_qual_models.DcInfo.objects.all():
            print old_qual_dc.values_list(flat=True)

    def full_copy(self):

        to_save = []
        for old_qual_dc in old_qual_models.DcInfo.objects.all():
            q_dc_info = new_qual_models.QualDcInfo()

            q_dc_info.identifier = old_qual_dc.identifier
            q_dc_info.title = old_qual_dc.title
            q_dc_info.creator = old_qual_dc.creator
            q_dc_info.subject = old_qual_dc.subject
            q_dc_info.description = old_qual_dc.description
            q_dc_info.publisher = old_qual_dc.publisher
            q_dc_info.contributor = old_qual_dc.contributor
            q_dc_info.date = old_qual_dc.date
            q_dc_info.type = old_qual_dc.type
            q_dc_info.format = old_qual_dc.format
            q_dc_info.source = old_qual_dc.source
            q_dc_info.language = old_qual_dc.language
            q_dc_info.relation = old_qual_dc.relation
            q_dc_info.coverage = old_qual_dc.coverage
            q_dc_info.rights = old_qual_dc.rights
            q_dc_info.user_id = old_qual_dc.user_id
            q_dc_info.created = old_qual_dc.created
            q_dc_info.words = old_qual_dc.words
            q_dc_info.calais = old_qual_dc.calais
            q_dc_info.vern_geog = old_qual_dc.vern_geog

            q_dc_info.thematic_group = old_qual_dc.thematic_group
            q_dc_info.tier = old_qual_dc.tier
            q_dc_info.identifier2 = old_qual_dc.identifier2

            q_dc_info.the_geom = old_qual_dc.the_geom

            to_save.append(q_dc_info)

        # new_qual_models.QualDcInfo.objects.bulk_create(to_save)

quals = CreateQualTables()
quals.check_old()