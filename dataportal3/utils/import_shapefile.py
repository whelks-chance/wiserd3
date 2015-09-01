import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")
from subprocess import call
from django.db import connections


class createSpatialTables():
    def __init__(self, shapefile_path, db_table, srid='4269', schema="Public", db_name="NewSurvey", sql_file=None):
        self.shapefile_path = shapefile_path
        self.db_table = db_table
        self.srid = srid
        self.schema = schema
        self.db_name = db_name
        self.sql_file = None

    def make(self):

        # shp2pgsql -I -s <SRID> <PATH/TO/SHAPEFILE> <SCHEMA>.<DBTABLE> | psql -U postgres -d <DBNAME>

        self.sql_file = 'shapefile.sql'
        cmd = 'shp2pgsql -I -s {0} {1} {2}.{3} > {4}'.format(
            self.srid,
            self.shapefile_path,
            self.schema,
            self.db_table,
            self.sql_file
        )
        code = call(cmd, shell=True)
        print code

    def insert(self):
        if self.sql_file is not None:
            cursor = connections['default'].cursor()
            with cursor:
                cursor.execute(open(self.sql_file, "r").read())

        # write_sql = 'sudo -U postgres psql -d {0} -f {1}'.format(
        #     self.db_name,
        #     self.sql_file
        # )
        # code = Popen(write_sql, shell=True).communicate()
        # print code


cst = createSpatialTables(
    shapefile_path='/tmp/shapefiles/235fffc9-fb41-49a0-a56d-da0ff70663b3/x_sid_liw2007_police_.shp',
    db_table='x_sid_liw2007_police_'
)
cst.make()
cst.insert()