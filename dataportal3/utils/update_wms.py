import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")
import requests
from wiserd3 import settings

__author__ = 'ubuntu'


def update_wms(wms_layer_list):
    for layer in wms_layer_list:
        filename = os.path.join(settings.BASE_DIR, os.path.join('dataportal3', os.path.join('static', layer['filename'])))
        print filename
        with open(filename, 'wb') as handle:
            response = requests.get(layer['url'], stream=True)

            if not response.ok:
                pass

            for block in response.iter_content(1024):
                handle.write(block)

update_wms(settings.WMS_LAYERS)
