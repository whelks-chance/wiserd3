import os
import random
import string
import sys
import getopt
import subprocess
import pwd
from django.contrib.gis.gdal.datasource import DataSource
import time
import math

__author__ = 'ubuntu'


class ShapefileImporter:
    def __init__(self):
        pass

    def demote(self, user_uid, user_gid):
        def result():
            # self.report_ids('starting demotion')
            os.setgid(user_gid)
            os.setuid(user_uid)
            # self.report_ids('finished demotion')
        return result

    def report_ids(self, msg):
        print 'uid, gid = {}, {}; {}'.format(os.getuid(), os.getgid(), msg)

    def uniqid(self, prefix='', more_entropy=False):
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

    def import_shapefile(self, argv):

        input_filename = ''
        tablename = ''
        db_name = ''
        try:
            opts, args = getopt.getopt(argv, "hi:t:d:", ["ifile=", "tablename", "db_name="])
        except getopt.GetoptError as egiog:
            print egiog
            print 'test.py -i <inputfile> -d <database name>'
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print 'test.py -i <inputfile> -d <database name>'
                sys.exit()

            elif opt in ("-t", "--tablename"):
                tablename = arg

            elif opt in ("-i", "--ifile"):
                input_filename = arg

            elif opt in ("-d", "--db_name"):
                db_name = arg

        print 'Input file is "', input_filename
        print 'db name is "', db_name
        print ''

        input_file = os.path.abspath(input_filename)

        if os.path.isfile(input_file):
            ds = DataSource(input_file)
            lyr = ds[0]

            print 'using {}'.format(input_file)

            if tablename is '':
                tablename = self.uniqid(prefix=str(lyr))

            print 'Tablename ', tablename

            lowered_tablename = tablename.lower()
            if lowered_tablename != tablename:
                tablename = lowered_tablename
                print 'Tablename was converted to lowercase {}'.format(tablename)

            self.do_db_import(input_file, tablename, db_name)

            # for f_idx, f in enumerate(lyr.fields):
            #     # for feature_idx in range(0, len(lyr)):
            #     # print f_idx, f, lyr.field_types[f_idx], lyr.get_fields(f)[feature_idx].__class__.__name__,  lyr.get_fields(f)[feature_idx]
            #     print f_idx, f, lyr.field_types[f_idx], lyr.get_fields(f)[0].__class__.__name__

        else:
            print '{} is not a valid input file'.format(input_file)
            sys.exit()

    def do_db_import(self, input_file, tablename, db_name, schema='public'):
        user_name, cwd = ['postgres', '/home/ubuntu/PycharmProjects/wiserd3/rubbish/TopoJsonGen/imports']
        env_args = ['/bin/bash', '--norc']

        pw_record = pwd.getpwnam('postgres')
        print pw_record
        user_name      = pw_record.pw_name
        user_home_dir  = pw_record.pw_dir
        user_uid       = pw_record.pw_uid
        user_gid       = pw_record.pw_gid
        env = os.environ.copy()
        env[ 'HOME'     ] = user_home_dir
        env[ 'LOGNAME'  ] = user_name
        env[ 'PWD'      ] = cwd
        env[ 'USER'     ] = user_name

        # self.report_ids('starting ' + str(env_args))

        shp2pgsql_cmd = 'shp2pgsql -W LATIN1 -I {} {}'.format(input_file, tablename)

        shp2pgsql_output = subprocess.Popen(
            shp2pgsql_cmd.split(' '),
            stdout=subprocess.PIPE,
            preexec_fn=self.demote(user_uid, user_gid),
            cwd=cwd,
            env=env
        )

        psql_cmd = 'psql -d {}'.format(db_name)

        output = subprocess.check_output(
            psql_cmd.split(' '),
            stdin=shp2pgsql_output.stdout,
            preexec_fn=self.demote(user_uid, user_gid),
            cwd=cwd,
            env=env
        )

        print output

        psql_cmd = [
            'psql',
            '-d', '{}'.format(db_name),
            '-c', 'COPY (select ST_SRID("{}"."geom") from "{}") TO STDOUT WITH CSV;'.format(
                tablename,
                tablename
            )
        ]

        output = subprocess.check_output(
            psql_cmd,
            preexec_fn=self.demote(user_uid, user_gid),
            cwd=cwd,
            env=env,
        )

        line_no = 0
        o_count = 0
        for o in output.split('\n'):
            if not o.isspace() and not len(o) == 0:
                line_no += 1
                # print '{}) {} >>{}<<'.format(line_no, len(o), o)

                if o == '0':
                    o_count += 1

        print o_count, line_no, o_count / line_no
        if o_count > line_no * 0.8:
            print 'Too many 0 lines, overwrite with some optimism'

            sql_line = "COPY (select UpdateGeometrySRID('{}', '{}', '{}', 4326)) TO STDOUT WITH CSV;".format(
                    schema,
                    tablename,
                    'geom'
                )
            print sql_line

            psql_cmd = [
                'psql',
                '-d', '{}'.format(db_name),
                '-c',  sql_line
            ]

            output = subprocess.check_output(
                psql_cmd,
                preexec_fn=self.demote(user_uid, user_gid),
                cwd=cwd,
                env=env,
            )

            print output

        sql_line = "COPY (select column_name, data_type, character_maximum_length, character_octet_length, " \
                   "numeric_precision_radix, numeric_precision " \
                   "from information_schema.columns where table_name = '{}') " \
                   "TO STDOUT WITH CSV;".format(
                    tablename,
                )
        print sql_line

        psql_cmd = [
            'psql',
            '-d', '{}'.format(db_name),
            '-c',  sql_line
        ]

        output = subprocess.check_output(
            psql_cmd,
            preexec_fn=self.demote(user_uid, user_gid),
            cwd=cwd,
            env=env,
        )

        model_field_lines = []
        for o in output.split('\n'):
            # print '>>>{}<<<'.format(o)
            field_data = o.split(',')

            if len(field_data) == 6:
                field_name = field_data[0]
                field_type = field_data[1]

                if field_name == 'gid':
                    model_field_lines.append('''
    gid = models.IntegerField(primary_key=True)
''')
                else:
                    if field_type == 'character varying':
                        model_field_lines.append('''
    {} = models.CharField(max_length=254, blank=True, null=True)'''.format(field_name)
                        )
                    elif field_type == 'double precision':
                        model_field_lines.append('''
    {} = models.IntegerField(blank=True, null=True)'''.format(field_name))

        model_str_head = '''
class {}(models.Model):
'''.format(tablename)

        model_str_tail = '''
    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = '{}'
'''.format(tablename)

        all_model_text = model_str_head + ''.join(model_field_lines) + model_str_tail

        print '\n\n'
        print all_model_text

# grant select, insert, update on all tables in schema public to dataportal;

if __name__ == "__main__":
    ShapefileImporter = ShapefileImporter()
    ShapefileImporter.import_shapefile(sys.argv[1:])
