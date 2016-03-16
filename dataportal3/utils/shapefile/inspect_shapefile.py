import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")
import django
django.setup()

import pprint
from django.contrib.gis.db import models
from django.contrib.gis.db.models import fields
from dataportal3.utils.spatial_search.spatial_search import geometry_columns
from django.db import connections
from django.db.transaction import atomic
from django.contrib.gis.gdal.datasource import DataSource

__author__ = 'ubuntu'


class ShapeFileWrapper:
    def __init__(self, shp_filename):
        self.shp_filename = shp_filename
        self.ds = DataSource(shp_filename)

    def get_fields(self, layer_number=0):
        layer = self.ds[layer_number]
        return layer.fields

    def get_number_of_fields(self, layer_number=0):
        return len(self.get_fields(layer_number))

    def get_field_value(self, field, layer_number=0):
        return self.ds[layer_number].get_fields(field)

# filename = '/home/ubuntu/DataPortalGeographies/AssemblyRegions/AssemblyRegions.shp'
# sfw = ShapeFileWrapper(filename)
# print sfw.get_fields()
# print sfw.get_field_value(sfw.get_fields()[0])


class ShapefileModelMatching:

    def __init__(self):

        self.action_count = 0

    def get_shp_lyr(self, extracted_shp, output=True):

        ds = DataSource(extracted_shp)
        lyr = ds[0]

        if output:
            print ''
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
            print ''

        return lyr

    def list_fields(self, lyr):
        print 'list_fields()'
        data = []

        # For each field in the shp layer, get all the values, in order
        for f_idx, f in enumerate(lyr.fields):

            field_data = {
                'field': f,
                'values': []
            }
            for feature_idx in range(0, len(lyr)):
                self.action_count += 1

                # This line is good, keep it
                # print f_idx, f, lyr.field_types[f_idx], lyr.get_fields(f)[feature_idx].__class__.__name__,  lyr.get_fields(f)[feature_idx]

                field_data['values'].append(lyr.get_fields(f)[feature_idx])

            data.append(field_data)

        # print pprint.pformat(data)
        return data

    def list_spatial_model_fields(self):
        print 'list_spatial_model_fields'
        shp_model_field_data_arr = []

        for model_description in geometry_columns:

            model_object = model_description['table_model']
            model_instance = model_object()
            # print type(model_object), model_object

            # Check we have an actual Django model
            if isinstance(model_instance, models.Model):
                model_fields = model_instance._meta.get_fields()
                # print model_instance._meta.model_name

                valid_fields = []

                for field in model_fields:
                    self.action_count += 1
                    if isinstance(field, fields.GeometryField):
                        pass
                    elif 'gid' in field.attname:
                        pass
                    else:
                        # We only want the fields which aren't geoms or gid
                        valid_fields.append(field.attname)

                # print model_object
                # print valid_fields
                try:
                    model_data = model_object.objects.all().values_list(*valid_fields)  # [:10]
                    # print list(model_data)

                    # Massive dict of all the model values, minus the geom stuff
                    shp_model_field_data = {
                        'table_name': model_instance._meta.db_table,
                        'fields': valid_fields,
                        'name': model_description['name']
                    }
                    print 'shp_model_field_data'
                    print pprint.pformat(shp_model_field_data)
                    shp_model_field_data['data'] = list(model_data)

                    # Creating an even bigger list of stuff across all models
                    shp_model_field_data_arr.append(shp_model_field_data)

                except Exception as e:
                    print e, type(e)

        # Basically printing half a database here...
        # print pprint.pformat(shp_model_field_data_arr)
        return shp_model_field_data_arr

    def get_best_match(self, filename=None):
        print 'get_best_match()'
        # filename = '/tmp/shapefiles/0d6bf8b0-dc83-4c2d-b1dd-874efd0cd1b0/extracted/wales_parl_2011_GeneralElection20102015.shp'
        if not filename:
            filename = '/home/ubuntu/DataPortalGeographies/AssemblyRegions/AssemblyRegions.shp'

        # Build a huge array of geom models, but without the geom data
        # We'll use this to compare stuff with to try and find a match
        shp_model_field_data_arr = self.list_spatial_model_fields()

        lyr = self.get_shp_lyr(filename)
        shp_file_field_data = self.list_fields(lyr)

        return self.find_matches(shp_file_field_data, shp_model_field_data_arr)

    def get_name_for_model(self, model_object):
        for geom in geometry_columns:
            if isinstance(geom['table_model'], model_object):
                if 'name' in geom:
                    return geom['name']
        return None

    def find_matches(self, shp_file_field_data, shp_model_field_data_arr):
        print 'find_matches()'
        hit = 0

        hits_arr = []

        best_hit_percentage = 0
        hit_model = None
        hit_model_field = None
        hit_shapefile_field = None
        hit_model_name = None

        for field in shp_file_field_data:

            print 'action count', self.action_count
            print 'shapefile field', field['field']

            for model_data in shp_model_field_data_arr:
                # How many hits for this model?
                model_hits = 0
                model_field_data = []

                print model_data['table_name']
                for model_field_idx, model_field in enumerate(model_data['fields']):
                    field_hits = 0

                    # print 'action count', self.action_count
                    # print 'model field :', model_field

                    for d in model_data['data']:

                        self.action_count += 1

                        if d[model_field_idx] is not None:
                            if d[model_field_idx] in field['values']:
                                print "Matched : " + str(d[model_field_idx]) + ' in ' + str(model_field)

                                hit += 1
                                model_hits += 1
                                field_hits += 1

                    hit_percentage = float(field_hits / len(model_data['data'])) * 100
                    model_field_data.append(
                        {
                            'field': model_field,
                            'field_hits': field_hits,
                            'hit_percent': hit_percentage
                        }
                    )

                    # If the number of hits for this field are larger percentage-wise than any other
                    # This is our new hit_model
                    if hit_percentage > best_hit_percentage:
                        hit_model = model_data['table_name']
                        hit_model_name = model_data['name']
                        hit_model_field = model_field
                        hit_shapefile_field = field['field']

                    print ''
                if model_hits > 0:
                    hits_arr.append({
                        'hits': model_hits,
                        'table_name': model_data['table_name'],
                        'model_field_data': model_field_data
                    })

            print ''
        print 'hits_arr', pprint.pformat(hits_arr, indent=4)
        print 'hits:', hit, 'model:', hit_model, 'model_field', hit_model_field, 'shp_field', hit_shapefile_field
        print 'action count', self.action_count

        # model_name = self.get_name_for_model(hit_model)

        return {
            'hits': hit,
            'table_name': hit_model,
            'model_field': hit_model_field,
            'shp_field': hit_shapefile_field,
            'name': hit_model_name

        }

        # matcher = ShapefileModelMatching()
        # matcher.get_best_match()