
apt-get install npm nodejs-legacy

npm install -g mapshaper

# Convert shapefile from whatever projection it currently is, to 4326 for WGS 84 (web mercator, but ovoid, not sphere)
ogr2ogr -f 'ESRI Shapefile' -t_srs EPSG:4326 input-fixed.shp Wales_lsoa_2011.shp

# This will be massive, and probably unusable
mapshaper -i input-fixed.shp snap -simplify dp 100% keep-shapes -o output-fixed.geojson format=geojson

# Topojson, much better. 1% is around 500k
mapshaper -i input-fixed.shp snap -simplify dp 100% keep-shapes -o output-fixed.json format=topojson
mapshaper -i input-fixed.shp snap -simplify dp 1% keep-shapes -o output-fixed-1.json format=topojson


Credits:
http://blog.webkid.io/maps-with-leaflet-and-topojson/

https://github.com/gka/chroma.js

http://gka.github.io/chroma.js/#chroma-contrast

http://sgillies.net/blog/1159/topojson-with-python

https://github.com/mbloch/mapshaper/wiki/Command-Reference

