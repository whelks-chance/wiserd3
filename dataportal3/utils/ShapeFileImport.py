import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")
import uuid
from wiserd3.settings import app
from django.contrib.gis.geos import GEOSGeometry
from dataportal3 import models
import zipfile
from django.contrib.gis.gdal import DataSource, CoordTransform, SpatialReference
# from django.contrib.gis.utils import ogrinspect
# import django_hstore.models
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

                # print extracted_shp

                ds = DataSource(extracted_shp)
                print ds.name

                # number of layers
                print 'number of layers', len(ds)
                lyr = ds[0]

                # layer name
                print 'layer name', lyr

                # layers type
                print 'layer type', lyr.geom_type

                print 'field_precisions', lyr.field_precisions
                print 'extent', lyr.extent
                print 'fields', lyr.fields
                print 'field_widths', lyr.field_widths
                print 'field_types', lyr.field_types[0].__dict__
                print ''
                print 'fields_types', lyr.field_types
                print 'geom_type', lyr.geom_type

                # number of features
                print 'number of features', len(lyr)

                # spatial reference
                srs = lyr.srs
                print 'spatial reference', srs

                # new_model = ogrinspect(ds, str(lyr))
                # print new_model

                feature_collection = FeatureCollectionStore()
                feature_collection.shapefile_upload = self.shapefile_upload
                feature_collection.name = str(lyr)
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
                            value = layer.get_fields(layer.fields[field_count])[count]
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

                        print feature.__dict__
                        # feature.save(using='new')
                        all_features.append(feature)

                        print 'Has_Geom', len(geoms[count]) > 0
                        print data
                        print ''

                bulk_insert = FeatureStore.objects.using('new').bulk_create(all_features, batch_size=50)

            except:
                self.shapefile_upload.progress = ShapeFileImport.progress_stage['import_failure']

            self.shapefile_upload.progress = ShapeFileImport.progress_stage['import_success']
            self.shapefile_upload.save()
            return True
        else:
            self.shapefile_upload.progress = ShapeFileImport.progress_stage['import_failure']
            self.shapefile_upload.save()
            raise Exception('Invalid or uninitialised shapefile')

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
            valid = False
            raise

        valid, filenames, missing =  self.__is_valid_zip(archive)

        self.is_valid = valid
        if self.is_valid:
            self.shapefile_upload.progress = ShapeFileImport.progress_stage['extract_begun']
            self.shapefile_upload.save()
            # only extracting files with extentions we care about
            try:
                for ext in filenames:
                    zip_stream = archive.extract(filenames[ext], path=self.extract_dir)
                    print zip_stream
                self.shapefile_upload.progress = ShapeFileImport.progress_stage['extracted_success']
            except:
                self.shapefile_upload.progress = ShapeFileImport.progress_stage['extracted_fail']
        else:
            self.shapefile_upload.progress = ShapeFileImport.progress_stage['verify_failure']
        self.shapefile_upload.save()


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

