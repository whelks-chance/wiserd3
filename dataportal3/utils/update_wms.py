import json
import os

from BeautifulSoup import BeautifulSoup

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


def get_wms_layer():
    wms_layers = []
    for layer in settings.WMS_LAYERS:
        try:
            filename = os.path.join(settings.BASE_DIR,
                                    os.path.join('dataportal3', os.path.join('static', layer['filename'])))
            print filename
            capabilities = open(filename, 'r').read()
            soup = BeautifulSoup(capabilities)
            x = soup.wms_capabilities.capability.findAll('layer', queryable=1)

            for y in x:

                desc = {
                    'tile_name': [z.string for z in y.findAll('name')][0],
                    'name': [z.string for z in y.findAll('title')][0].replace('_', ' '),
                    'source': layer['url_wms']
                }

                if y.style:
                    if y.style.legendurl:
                        desc['legend_img'] = y.style.legendurl.onlineresource['xlink:href']

                wms_layers.append(desc)

        except Exception as e9832478:
            print type(e9832478), e9832478

    lle_filename = os.path.join(settings.BASE_DIR,
                            os.path.join('dataportal3', os.path.join('static', 'lle.json')))
    with open(lle_filename, 'w') as lle:
        lle.write(json.dumps(wms_layers, indent=4))

# update_wms(settings.WMS_LAYERS)

get_wms_layer()