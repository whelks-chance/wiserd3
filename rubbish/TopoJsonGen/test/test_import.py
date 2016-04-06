from rubbish.TopoJsonGen.imports.import_shapefile import ShapefileImporter

__author__ = 'ubuntu'


si = ShapefileImporter()

si.import_shapefile(['-i', '44234', '-o', '242432'])

# si.import_shapefile({
#     '-i': '1234',
#     '-o': '69342',
#     '-h': '9783456'
# })
