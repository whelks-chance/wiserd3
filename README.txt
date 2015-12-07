
apt-get install npm nodejs-legacy

npm install -g mapshaper

ls *.zip|awk -F'.zip' '{print "unzip "$0" -d "$1}'|sh

11, 13, 14


# Convert shapefile from whatever projection it currently is, to 4326 for WGS 84 (web mercator, but ovoid, not sphere)
ogr2ogr -f 'ESRI Shapefile' -t_srs EPSG:4326 input-fixed.shp Wales_lsoa_2011.shp

# This will be massive, and probably unusable
mapshaper -i input-fixed.shp snap -simplify dp 100% keep-shapes -o output-fixed.geojson format=geojson

# Topojson, much better. 1% is around 500k
mapshaper -i input-fixed.shp snap -simplify dp 100% keep-shapes -o output-fixed.json format=topojson
mapshaper -i input-fixed.shp snap -simplify dp 1% keep-shapes -o output-fixed-1.json format=topojson


Build the Database

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
/usr/pgsql-9.4/bin/shp2pgsql
-I spatialdata.parl/spatialdata.parl.shp spatialdata_parl | sudo -u postgres psql -d "NewSurvey"

Dump shp file to DB for spatial search :
shp2pgsql -I ~/shp/x_sid_liw2007_pcode_/x_sid_liw2007_pcode_.shp pcode | sudo -u postgres psql -d "NewSurvey"
do this for one of each type of boundary


The new shpfile tables need the right permissions
grant select, insert, update on all tables in schema public to dataportal;

Celery - Shapefile import process, celery needs explicit export of settings module location
sudo yum install redis
sudo systemctl start redis.service
export DJANGO_SETTINGS_MODULE='wiserd3.settings'
celery -A dataportal3.utils.ShapeFileImport worker --loglevel=info

http://nominatim.openstreetmap.org/reverse?format=json&lat=51.5793876&lon=-3.1731345&zoom=18&addressdetails=1

Credits:
http://blog.webkid.io/maps-with-leaflet-and-topojson/

https://github.com/gka/chroma.js

http://gka.github.io/chroma.js/#chroma-contrast

http://sgillies.net/blog/1159/topojson-with-python

https://github.com/mbloch/mapshaper/wiki/Command-Reference

http://bootsnipp.com/snippets/featured/quotwaiting-forquot-modal-dialog

http://jrue.github.io/coding/2014/exercises/basicbubblepackchart/