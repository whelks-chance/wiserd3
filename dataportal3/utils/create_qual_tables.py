import os
from django.contrib.gis.geos import GEOSGeometry
from django.db import OperationalError
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")
import django
django.setup()
from dataportal3.utils.ReadQual import ReadQual
import json
import pprint

__author__ = 'ubuntu'

from old_qual import models as old_qual_models
from dataportal3 import models as new_qual_models


class CreateQualTables():

    def __init__(self):
        self.rq = ReadQual()

    def check_old(self):
        for old_qual_dc in old_qual_models.DcInfo.objects.all()[:1]:

            for model_field in old_qual_models.DcInfo._meta.get_fields():
                print '\n'

                print '***', model_field.name

                try:
                    o = getattr(old_qual_dc, model_field.name)
                    print model_field.name, ':\n', type(o), ':\n', o
                except Exception as e24:
                    print 'error24', e24

            # print pprint.pformat(self.rq.get_coverage_items(old_qual_dc['coverage']))
            try:
                calais_text = old_qual_dc.calais.strip().rstrip(',')
                calais_text = '{"data": [' + calais_text + ']}'
                print '*' + calais_text + '*'
                calais_object = json.loads(calais_text, strict=False)
                # print pprint.pformat(calais_object)
            except Exception as e:
                print 'error', e

            try:
                calais_text = old_qual_dc.words.strip().rstrip(',')
                calais_text = '{"data": [' + calais_text + ']}'
                print '*' + calais_text + '*'
                calais_object = json.loads(calais_text, strict=False)
                # print pprint.pformat(calais_object)
            except Exception as e:
                print 'error', e

    def get_word_usages(self, words):

        words_text = words.strip().rstrip(',')
        words_text = '{"data": [' + words_text + ']}'
        # print '*' + words_text + '*'
        words_object = json.loads(words_text, strict=False)

        word_dict = {}
        for word in words_object['data']:
            try:
                word_dict[word['word']] = word['count']
            except Exception as e984273:
                print e984273, word
        return word_dict

    def get_geom(self, geom_string):
        print type(geom_string), geom_string[:3]
        if geom_string[:3] == 'SRID':
            srid_split = geom_string[geom_string.index(';')]
            print srid_split[0]
            print srid_split[1]

            geom = GEOSGeometry(srid_split[1], srid=srid_split[0])
            return geom
        else:
            raise

    def full_copy(self):

        to_save = []
        for old_qual_dc in old_qual_models.DcInfo.objects.all()[:1]:
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

            coverage_object = self.rq.get_coverage_items(old_qual_dc.coverage)
            # q_dc_info.coverage = coverage_object

            q_dc_info.rights = old_qual_dc.rights
            q_dc_info.user_id = old_qual_dc.user_id
            q_dc_info.created = old_qual_dc.created

            words_arr = self.get_word_usages(old_qual_dc.words)
            # print pprint.pformat(words_arr, indent=4)
            q_dc_info.words = words_arr

            q_dc_info.calais = self.rq.get_calais_object(old_qual_dc.calais)

            q_dc_info.vern_geog = old_qual_dc.vern_geog

            if thematics:
                q_dc_info.thematic_group = old_qual_dc.thematic_group
                if len(old_qual_dc.thematic_group.strip()):
                    for tg in old_qual_dc.thematic_group.strip().split(','):
                        tg_model = new_qual_models.ThematicGroup.objects.get(grouptitle=tg.strip())
                        print tg_model
                        q_dc_info.thematic_groups_set.add(tg_model)

            q_dc_info.tier = old_qual_dc.tier

            # geom_string = old_qual_dc.the_geom
            # print geom_string
            # geom = self.get_geom(geom_string)
            q_dc_info.the_geom = old_qual_dc.the_geom

            try:
                q_dc_info.save()
            except OperationalError:
                print connection.queries[-1]

            to_save.append(q_dc_info)

        # new_qual_models.QualDcInfo.objects.bulk_create(to_save)

thematics = False
quals = CreateQualTables()
# quals.check_old()
quals.full_copy()