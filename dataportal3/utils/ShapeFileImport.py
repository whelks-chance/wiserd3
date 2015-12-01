import os
from django.db import connections
from django.db.transaction import atomic

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")

import string
from django.utils.crypto import random
import time
import math

import django
django.setup()

from subprocess import call
import uuid
from wiserd3.settings import app
from django.contrib.gis.geos import GEOSGeometry
from dataportal3 import models
import zipfile
from django.contrib.gis.gdal import DataSource, CoordTransform, SpatialReference
from dataportal3.models import FeatureCollectionStore, FeatureStore

__author__ = 'ubuntu'


class ShapeFileImport:

    progress_stage = {
        'init': 'INIT',
        'extract_begun': 'EXTRACTING_ZIP',
        'extracted_success': 'ZIP_EXTRACTION_SUCCESS',
        'extracted_fail': 'ZIP_EXTRACTION_FAILURE',
        'verify_success': 'ZIP_VERIFY_SUCCESS',
        'verify_failure': 'ZIP_VERIFY_FAILURE',
        'import_begun': 'IMPORTING_FEATURES',
        'import_success': 'FEATURE_IMPORT_SUCCESS',
        'import_failure': 'FEATURE_IMPORT_FAILURE'
    }

    def __init__(self, user, zip_file, filename, shapefile_upload_id=None):
        self.user = user
        self.is_valid = False
        self.archive_dir = ''
        self.extract_dir = ''
        self.filenames = {
            'shp': '',
            'dbf': '',
            'prj': '',
            'shx': ''
        }
        self.missing = []

        if shapefile_upload_id is None:
            shapefile_upload = models.ShapeFileUpload()
            shapefile_upload.user = user
            shapefile_upload.uuid = str(uuid.uuid4())
            shapefile_upload.shapefile = zip_file
            shapefile_upload.name = filename
            shapefile_upload.progress = ShapeFileImport.progress_stage['init']
            shapefile_upload.save()
        else:
            shapefile_upload = models.ShapeFileUpload.objects.get(id=shapefile_upload_id)

        self.shapefile_upload = shapefile_upload

    def import_to_gis(self):
        if self.is_valid:
            try:
                extracted_shp = os.path.join(self.extract_dir, self.filenames['shp'])

                lyr = self.get_shp_lyr(extracted_shp)
                self.create_spatial_survey_links(lyr)

                # Deprecated, but saved in case this makes sense some day
                # self.save_feature_collection(ds)

            except Exception as e:
                print e
                self.shapefile_upload.progress = ShapeFileImport.progress_stage['import_failure']
                raise Exception('Invalid or uninitialised shapefile ' + str(e))

            self.shapefile_upload.progress = ShapeFileImport.progress_stage['import_success']
            self.shapefile_upload.save()
            return True
        else:
            self.shapefile_upload.progress = ShapeFileImport.progress_stage['import_failure']
            self.shapefile_upload.save()
            raise Exception('Invalid or uninitialised shapefile')

    def save_feature_collection(self, ds):
        lyr = ds[0]

        feature_collection = FeatureCollectionStore()
        feature_collection.shapefile_upload = self.shapefile_upload
        feature_collection.name = str(lyr)
        feature_collection.topojson_file = self.create_topojson_file()
        feature_collection.save()

        all_features = []

        for layer in ds:
            print 'features in layer', len(lyr.get_geoms(geos=True))

            geoms = layer.get_geoms(geos=True)

            self.shapefile_upload.description = 'ShapeFile ' \
                + ':' + str(lyr) \
                + ', ' + str(len(lyr.get_geoms(geos=True))) \
                + ' features'
            self.shapefile_upload.progress = ShapeFileImport.progress_stage['import_begun']
            self.shapefile_upload.save()

            for count in range(0, len(geoms)):
                data = {}
                for field_count in range(0, len(layer.fields)):
                    key = layer.fields[field_count]
                    value = layer.get_fields(key)[count]
                    # print key, value, type(value)
                    data[key] = value

                feature = FeatureStore()
                feature.feature_collection = feature_collection
                if 'AREA_NAME' in layer.fields:
                    feature.name = layer.get_fields('AREA_NAME')[count]
                else:
                    feature.name = str(layer) + str(count)
                feature.feature_attributes = data
                feature.geometry = geoms[count]

                # feature.save(using='new')
                all_features.append(feature)

                print 'Has_Geom', len(geoms[count]) > 0
                print data
                print ''

        bulk_insert = FeatureStore.objects.using('new').bulk_create(all_features, batch_size=50)

    def create_topojson_file(self):
        extracted_shp = os.path.join(self.extract_dir, self.filenames['shp'])

        cmd = 'mapshaper -i {0} snap -simplify dp 1% keep-shapes -o {0}.topojson format=topojson'.format(
            extracted_shp
        )
        code = call(cmd, shell=True)
        print 'mapshaper topojson convert success', code

        return str(extracted_shp) + '.topojson'

    def __is_valid_zip(self, archive):
        # Try and find details of the zip file

        for zipped_file in archive.infolist():
            print zipped_file.filename

            # Screw that, properly formed URI's or nothing
            # We're not gonna trust root files, or navigation up and out of the zip
            if str(zipped_file).startswith('/') or '..' in str(zipped_file):
                return False, self.filenames, self.missing

            if str(zipped_file.filename).endswith('.shp'):
                self.filenames['shp'] = zipped_file.filename
            if str(zipped_file.filename).endswith('.dbf'):
                self.filenames['dbf'] = zipped_file.filename
            if str(zipped_file.filename).endswith('.prj'):
                self.filenames['prj'] = zipped_file.filename
            if str(zipped_file.filename).endswith('.shx'):
                self.filenames['shx'] = zipped_file.filename

        # Check if any of the blank dict is still blank
        for file_type in self.filenames:
            if self.filenames[file_type] == '':
                self.missing.append(file_type)

        if len(self.missing):
            self.shapefile_upload.progress = ShapeFileImport.progress_stage['verify_failure']

            # If the array of missing things has anything in, it's not valid
            return False, self.filenames, self.missing
        else:
            return True, self.filenames, self.missing

    def extract_zip(self):
        shapefile_zip = self.shapefile_upload.shapefile.url
        print shapefile_zip

        self.archive_dir = os.path.dirname(os.path.realpath(shapefile_zip))
        print self.archive_dir
        self.extract_dir = os.path.join(self.archive_dir, 'extracted')
        print self.extract_dir
        try:
            archive = zipfile.ZipFile(shapefile_zip, "r")
        except:
            self.shapefile_upload.progress = ShapeFileImport.progress_stage['verify_failure']
            self.shapefile_upload.save()
            self.is_valid = False
            raise

        valid, filenames, missing = self.__is_valid_zip(archive)

        self.is_valid = valid
        if self.is_valid:
            self.shapefile_upload.progress = ShapeFileImport.progress_stage['extract_begun']
            self.shapefile_upload.save()
            # only extracting files with extensions we care about
            try:
                for ext in filenames:
                    zip_stream = archive.extract(filenames[ext], path=self.extract_dir)
                    print zip_stream
                self.shapefile_upload.progress = ShapeFileImport.progress_stage['extracted_success']
            except Exception as e98324:
                print e98324, type(e98324)
                self.shapefile_upload.progress = ShapeFileImport.progress_stage['extracted_fail']
        else:
            self.shapefile_upload.progress = ShapeFileImport.progress_stage['verify_failure']
        self.shapefile_upload.save()

    def get_shp_lyr(self, extracted_shp, output=True):

        ds = DataSource(extracted_shp)
        lyr = ds[0]

        if output:
            print 'data source', ds.name
            print 'number of layers', len(ds)
            print 'layer name', lyr
            print 'layer type', lyr.geom_type
            print 'field_precisions', lyr.field_precisions
            print 'extent', lyr.extent
            print 'fields', lyr.fields
            print 'field_widths', lyr.field_widths
            print 'fields_types', lyr.field_types
            print 'geom_type', lyr.geom_type
            print 'number of features', len(lyr)
            print 'spatial reference', lyr.srs

        return lyr

    # We create a spatial_survey_link row for each field in the shapefile
    def create_spatial_survey_links(self, lyr):

        conn_queries = connections['new'].queries
        print 'create_spatial_survey_links start', len(conn_queries)
        # print 'survey queries', conn_queries

        # get name and type data out of shapefile,
        # create Survey object to associate this data with
        survey = self.init_survey(lyr)
        geoms = lyr.get_geoms(geos=False)

        # We want to remove the "reserved fields" this system uses to name regions
        clean_fields = {}
        reserved_fields = {}
        for field_idx, field in enumerate(lyr.fields):
            if field in ['NAME', 'ALT_NAME', 'ALTNAME', 'CODE']:
                reserved_fields[field] = field_idx
            else:
                clean_fields[field] = field_idx

        print 'clean', clean_fields
        print 'reserved', reserved_fields

        # get all the geocodes, assuming they're called "CODE"
        geo_codes = []
        for geo_idx, geom in enumerate(geoms):
            code = lyr.get_fields('CODE')[geo_idx]
            print code
            geo_codes.append(code)

        survey_links_to_save = []

        # clean_fields is a dict of field_name => index_in_lyr.fields
        for field_name in clean_fields:
            # we want the original index
            field_idx = clean_fields[field_name]
            print field_name
            field_type = lyr.get_fields(field_name)[0].__class__.__name__
            print 'field_type', field_type

            regions_with_data = {}

            for geo_idx, geom in enumerate(geoms):

                value = lyr.get_fields(field_name)[geo_idx]
                print geo_codes[geo_idx], value

                regions_with_data[geo_codes[geo_idx]] = value

            new_survey_link = models.SpatialSurveyLink()
            new_survey_link.survey = survey
            new_survey_link.data_name = field_name
            new_survey_link.data_prefix = ''
            new_survey_link.data_suffix = ''
            new_survey_link.data_type = str(field_type)
            new_survey_link.geom_table_name = 'spatialdata_parl'
            new_survey_link.regional_data = regions_with_data
            new_survey_link.boundary_name = "Parliamentary"

            print ''
            survey_links_to_save.append(new_survey_link)

        conn_queries = connections['new'].queries
        print 'create_spatial_survey_links init', len(conn_queries)

        # bulk_create doesn't allow ManyToMany links
        bulk_insert = models.SpatialSurveyLink.objects.using('new').bulk_create(survey_links_to_save, batch_size=50)

        conn_queries = connections['new'].queries
        print 'create_spatial_survey_links end, update_spatial_link_user start', len(conn_queries)

        self.update_spatial_link_user(bulk_insert)

        conn_queries = connections['new'].queries
        print 'update_spatial_link_user end', len(conn_queries)

    # bulk_create doesn't allow ManyToMany links
    # atomic should save all the links at once, faster than multiple save()'s
    @atomic
    def update_spatial_link_user(self, bulk_insert_item_list):
        # So get id's of created survey_links and update the user manually.
        link_ids = []
        for survey_link_to_save in bulk_insert_item_list:
            link_ids.append(survey_link_to_save.id)

        new_survey_links = models.SpatialSurveyLink.objects.using('new').filter(id__in=link_ids)
        for link in new_survey_links:
            link.users.add(self.user)
            link.save()

    def init_survey(self, lyr):

        uid = uniqid()
        dc_id = 'wisid_' + str(lyr) + '_' + uid
        survey_id = 'sid_' + str(lyr) + '_' + uid

        dc = models.DcInfo()
        dc.title = str(lyr)
        dc.identifier = dc_id
        dc.save()

        print 'dc', dc

        survey = models.Survey()
        survey.short_title = self.shapefile_upload.name
        survey.survey_title = str(lyr)
        survey.dublin_core = dc
        survey.identifier = dc_id
        survey.surveyid = survey_id
        survey.save()

        print 'survey', survey
        return survey


def spatial_search():
    geojson = [u'POLYGON ((272268.6283144115 200270.16611863102,272618.35541865695 214073.16809610612,353647.5501633153 212672.1529419519,353520.31875525665 198867.7012925945,272268.6283144115 200270.16611863102))']

    ct = CoordTransform(SpatialReference('EPSG:27700'), SpatialReference('EPSG:4326'))

    # geom = GEOSGeometry(geojson[0], srid=27700).transform(ct)
    geom = GEOSGeometry(geojson[0], srid=27700)

    spatial_intersects = models.FeatureStore.objects.filter(geometry__intersects=geom)
    print spatial_intersects.count()

    response_data = {}
    response_data['data'] = list(spatial_intersects.values_list('name', flat=True))
    print response_data['data']
    print type(response_data['data'])

    f = models.FeatureStore.objects.filter(id=2)[0]
    print f.name

    print f.geometry.distance(geom)


#   From http://gurukhalsa.me/2011/uniqid-in-python/
def uniqid(prefix='', more_entropy=False):
    m = time.time()
    uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0,10,1):
            entropy_string += random.choice(valid_chars)
        uniqid = uniqid + entropy_string
    uniqid = prefix + uniqid
    return uniqid


@app.task
def celery_import(user_id, zip_file, filename, shapefile_upload_id=None):
    user = models.UserProfile.objects.get(id=user_id)
    sf = ShapeFileImport(
        user,
        zip_file=zip_file,
        filename=filename,
        shapefile_upload_id=shapefile_upload_id
    )
    sf.extract_zip()
    a = sf.import_to_gis()
    print a
    return a

