import ckanapi

from dataportal3.utils.generic.remote_data_default import RemoteDataDefault
from wiserd3.settings import ckan_api_key, ckan_org_name


class CKANdata(RemoteDataDefault):
    def __init__(self):
        RemoteDataDefault.__init__(self)
        self.ckan_api = None

    def init(self):
        if not self.ckan_api:
            self.ckan_api = ckanapi.RemoteCKAN(
                'https://datahub.io',
                user_agent='ckanapiexample/1.0 (+http://data.wiserd.ac.uk)',
                apikey=ckan_api_key
            )
        return self.ckan_api

    def get_data_dict(self, dataset_id, options, constants):
        ckan_api = self.init()

        offset = 0
        return_data = {}

        while offset < 2000:

            data = ckan_api.action.datastore_search(resource_id=dataset_id, offset=offset)

            # print data, '\n\n'


            for d in data['records']:
                print '\n', d

                return_data[d['LSOAName']] = [
                    {
                        "name": d['LSOAName'],
                        "value": d['WIMD2014'],
                        # "geography_id": 1946157398,
                        "geography_code": d['LSOACode'],
                        "data_status": "A",
                        "geography": d['LSOAName']
                    }
                ]

            offset += 100
        return return_data

    def get_metadata_for_dataset(self, dataset_id):
        pass

    def get_dataset_overview(self, dataset_id):

        dimensions = {}

        dimensions['LSOACode'] = {
            "concept": 'LSOACode',
            "name": 'LSOACode',
            'measures': [{
                'id': 'LSOACode',
                'name': 'LSOACode'
            }]
        }

        return_data = {
            'concepts': [],
            'codelists': dimensions,
            'geographies': [
                {
                    'name': 'LSOA',
                    'id': 'lsoa'
                }
            ]
        }

        return return_data

    def keyword_search(self, keyword_string, args=None):

        ckan_api = self.init()

        found_datasets = [
            {
                'id': '650200e9-cfad-4efa-9fbf-cf35483b1e36',
                'name': 'wimd2014',
                'source': 'CKAN_datahub'
            }
        ]
        return found_datasets, None

