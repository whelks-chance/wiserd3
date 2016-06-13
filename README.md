# WISERD DataPortal v3

## Install and runtime notes

This doesn't entirely explain how to get it all running, but it may help future debugging...

## Static files

In nginx.conf make sure /static points to the right django dir

## Mapshaper install

    apt-get install npm nodejs-legacy
    npm install -g mapshaper
    ls *.zip|awk -F'.zip' '{print "unzip "$0" -d "$1}'|sh

11, 13, 14

## ShapeFiles
Convert shapefile from whatever projection it currently is, to 4326 for WGS 84 (web mercator, but ovoid, not sphere)

    ogr2ogr -f 'ESRI Shapefile' -t_srs EPSG:4326 input-fixed.shp Wales_lsoa_2011.shp

This will be massive, and probably unusable

    mapshaper -i input-fixed.shp snap -simplify dp 100% keep-shapes -o output-fixed.geojson format=geojson

### Topojson
Topojson, much better. 1% is around 500k
    
    mapshaper -i input-fixed.shp snap -simplify dp 100% keep-shapes -o output-fixed.json format=topojson
    mapshaper -i input-fixed.shp snap -simplify dp 1% keep-shapes -o output-fixed-1.json format=topojson

### Prettyprint
The topojson file is printed all on a single line in the file, which breaks editors

    node -e "console.log(JSON.stringify(JSON.parse(require('fs') \
      .readFileSync(process.argv[1])), null, 4));" output-fixed-1.json > pretty.json

## Build the Database

DB VM

    sudo -u postgres psql < build_sql.sql

Django VM

    source ~/venv/bin/activate
    python manage.py makemigrations dataportal3

Centos7 is a pain with shp2pgsql:

    sudo yum install pgdg-centos94-9.4-2.noarch.rpm
    yum install postgis2_94 postgis2_94-client postgis2_94-utils

may also need the full postgresql9.4 packages

note alternate shp2pgsql binaries location due to messed up install not updating alternatives
left alone this time as previous postgresql version expects postgis-2.0.7
at this point, 2 versions of each are installed....

    /usr/pgsql-9.4/bin/shp2pgsql -I spatialdata.parl/spatialdata.parl.shp spatialdata_parl | sudo -u postgres psql -d "NewSurvey"

## SHP to Database
Dump shp file to DB for spatial search :

    shp2pgsql -W LATIN1 -I ~/shp/x_sid_liw2007_pcode_/x_sid_liw2007_pcode_.shp pcode | sudo -u postgres psql -d "NewSurvey"

do this for one of each type of boundary

### Check the geo data is valid 
Check the SRID is set, if it's '0', you need to set it, probably to 4326:

    select code, ST_SRID("table"."geom") from "table";

(public is the schema)

    select UpdateGeometrySRID('public', 'table', 'geom_column', 4326) ;

Existing WISERD localities boundaries need to be 27700, not 4326:

    select UpdateGeometrySRID('public', 'heads_of_the_valleys', 'geom', 27700) ;
    select UpdateGeometrySRID('public', 'aberystwyth_locality_dissolved', 'geom', 27700) ;
    select UpdateGeometrySRID('public', 'bangor_locality_dissolved', 'geom', 27700) ;

### Allow access to the table
The new shpfile tables need the right permissions

    grant select, insert, update on all tables in schema public to dataportal;

### Then update the spatial search code:
In dataportal3/utils/spatial_search/spatial_search.py
The "geometry_columns" array needs a new dict for this models data.

        {
            'table_name': 'spatialdata_aefa',
            'geometry_column': 'geom',
            'label': 'label',
            'table_model': models.SpatialdataAEFA
        },

Obviously a new model needs to be made which describes the new table, in models.py
Inspect the table in the database with
    
    sudo -u postgres psql
    d+ new_table_name
    
Similar to this, but with the correct field/ column names:

    class SpatialdataAEFA(models.Model):
        gid = models.IntegerField(primary_key=True)
        name = models.CharField(max_length=254, blank=True, null=True)
        label = models.CharField(max_length=254, blank=True, null=True)
        geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
        objects = models.GeoManager()
    
        class Meta:
            managed = False
            db_table = 'spatialdata_aefa'

## Celery
Shapefile import process, celery needs explicit export of settings module location

    sudo yum install redis
    sudo systemctl start redis.service
    export DJANGO_SETTINGS_MODULE='wiserd3.settings'
    celery -A dataportal3.utils.ShapeFileImport worker --loglevel=info

http://nominatim.openstreetmap.org/reverse?format=json&lat=51.5793876&lon=-3.1731345&zoom=18&addressdetails=1

## Process for adding data and rendering a map layer

Assume a search has given us a UUID

Home › Dataportal3 › Nomis searchs › winning_party_11:4bcb579a-e507-404b-9412-c6a89065ca4a:constituency

A "NomisSearch" has this UUID
The NomisSearch object has a geography (ie ua, constituency)
The NomisSearch has a search attributes dictionary, with key:value data_name:< an identifier for some data >
If the NomisSearch type is "Survey" then the Dataset_ID is the an "identifier" of a Survey object

Home › Dataportal3 › Spatial survey links › wisid_AssemblyConstituency_Data_57057b24ed6a1:nawer:aecMaj11

Find "a" SpatialSurveyLink where the Survey_ID, the boundary name and the data_name match the above.
This SpatialSurveyLink has a RegionalData dictionary, with key:value < region id > : <data value for this region >
Here <region id> is any identifier which matches the ID in the topojson/geojson (created from a shapefile), defined during the shapefile importing process

Once we have that SpatialSurveyLink

## Auto import NAW data/ create sidebar searches

###Constituencies

    python dataportal3/utils/ShapeFileImport.py -i path/NAW_3_constituencies.zip -s wisid_AssemblyConstituency_Data_57057b24ed6a1 -u a_user -n constituency_test -g nawer -b "National Assembly Constituency"

    python dataportal3/utils/rubbish/update_survey_region_metadata.py -i path/NAW_3/NAWConstituencyDataNamesLookup.csv -s wisid_AssemblyConstituency_Data_57057b24ed6a1

    python dataportal3/utils/ShapeFileImport.py -i path/NAW_3_constituencies.zip -s wisid_AssemblyConstituency_Data_57057b24ed6a1 -u a_user -n constituency_test -g nawer -b "National Assembly Constituency" -x True -r constituency


### Regions

    python dataportal3/utils/ShapeFileImport.py -i path/NAW_3/NAW_3_regions.zip -s wisid_AssemblyRegions_Data_5705394bb0ec5 -u ubuntu -n region_test -g nawer -b "National Assembly Region"

    python dataportal3/utils/rubbish/update_survey_region_metadata.py -i path/NAW_3/NAWRegionDataNamesLookup.csv -s wisid_AssemblyRegions_Data_5705394bb0ec5

    python dataportal3/utils/ShapeFileImport.py -i path/NAW_3/NAW_3_regions.zip -s wisid_AssemblyRegions_Data_5705394bb0ec5 -u ubuntu -n region_test -g nawer -b "National Assembly Region" -x True -r region


## Languages
    python manage.py compilemessages --locale=cy

    python manage.py makemessages --locale=cy

    tail --bytes=+4 UTF8WithBom.txt > UTF8WithoutBom.txt

## Rights/ Visibility Management:
A UserGroup has a name and a collection of users
The UserGroupSurveyCollection is a collection of surveys which the user group has a read/access claim over
A SurveyVisibilityMetadata defines the visibility of a single survey as seen as part of a single UserGroupSurveyCollection

This means:
A survey can have multiple visibilities, as multiple UserGroupSurveyCollection's can "own" it
e.g.
Surveys A, B, C, D, E
UserGroups X, Y, Z

Members of group X can view Surveys A, B, C
Members of group Y can view C, D, E
Members of group Z can view A, E

A single user can be in any/ all groups without any contradictions.
If a user both *Can* and *Cannot* view a survey due to visibilities specifically denying access, access is still granted.

## Credits
### Code not necessarily lifted entirely, but debugging help or guidance was found here:

http://blog.webkid.io/maps-with-leaflet-and-topojson/

https://github.com/gka/chroma.js

http://gka.github.io/chroma.js/#chroma-contrast

http://sgillies.net/blog/1159/topojson-with-python

https://github.com/mbloch/mapshaper/wiki/Command-Reference

http://bootsnipp.com/snippets/featured/quotwaiting-forquot-modal-dialog

http://jrue.github.io/coding/2014/exercises/basicbubblepackchart/

http://stackoverflow.com/questions/1770209/run-child-processes-as-different-user-from-a-long-running-process/6037494#6037494

http://stackoverflow.com/a/13332300/2943238

https://github.com/calvinmetcalf/topojson.py

https://github.com/komoot/staticmap

https://dzone.com/articles/taking-browser-screenshots-no

http://selenium-python.readthedocs.io/waits.html

## Awkwardness

    ALTER TABLE django_content_type ADD COLUMN name character varying(50) NOT NULL DEFAULT 'someName';

