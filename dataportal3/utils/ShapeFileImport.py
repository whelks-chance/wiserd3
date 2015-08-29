import json
import os
import zipfile
from django.contrib.gis.gdal import DataSource

__author__ = 'ubuntu'


class ShapeFileImport:
    def __init__(self):
        self.is_valid = False
        self.archive_dir = ''
        self.filenames = {
            'shp': '',
            'dbf': '',
            'prj': '',
            'shx': ''
        }
        self.missing = []

    def get_shp_info(self):
        if self.is_valid:
            extracted_shp = os.path.join(self.archive_dir, self.filenames['shp'])

            # print extracted_shp

            ds = DataSource(extracted_shp)
            # print ds.name

            # number of layers
            # print 'number of layers', len(ds)
            lyr = ds[0]

            # layer name
            # print 'layer name', lyr

            # layers type
            # print 'layer type', lyr.geom_type

            # number of features
            # print 'number of features', len(lyr)

            # spatial reference
            srs = lyr.srs
            # print 'spatial reference', srs

            return str(srs)
        else:
            return 'Invalid or uninitialised shapefile'

    def is_valid_zip(self, archive):
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
            # If the array of missing things has anything in, it's not valid
            return False, self.filenames, self.missing
        else:
            return True, self.filenames, self.missing

    def extract_zip(self, shapefile_zip):

        self.archive_dir = os.path.dirname(os.path.realpath(shapefile_zip))
        try:
            archive = zipfile.ZipFile(shapefile_zip, "r")
        except:
            valid = False
            raise

        valid, filenames, missing =  self.is_valid_zip(archive)

        self.is_valid = valid
        if self.is_valid:
            # only extracting files with extentions we care about
            for ext in filenames:
                zip_stream = archive.extract(filenames[ext], path=self.archive_dir)
                print zip_stream




z = '/tmp/shp/x_sid_liw2007_police_/x_sid_liw2007_police_.zip'
# z = '/home/ubuntu/PycharmProjects/wiserd3/dataportal3/utils/x_sid_liw2007_police_.shp'
# z = '/tmp/shp/x_sid_liw2007_police_/x_sid_liw2007_police_.shp'
# z = '/tmp/shp/x_sid_liw2007_police_/x_sid_liw2007_police_.zip/x_sid_liw2007_police_.shp'
# z = '/tmp/shapefiles/eac88890-0784-4f68-8d92-363a8aa95f66/x_sid_liw2007_police_.zip'

sf = ShapeFileImport()
sf.extract_zip(z)
a = sf.get_shp_info()
print a
