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
        print 'options', options, 'constants', constants

        # value_id = 'WIMD2014'
        # geog_id = 'LSOACode'
        # name_id = 'LSOAName'

        value_id = ''
        geog_id = ''
        name_id = ''

        for op in options:
            if op[0] == 'Name_Code':
                name_id = op[1]
            if op[0] == 'Value_Code':
                value_id = op[1]
            if op[0] == 'Geography_Code':
                geog_id = op[1]

        if name_id == '':
            name_id = value_id

        ckan_api = self.init()

        offset = 0
        return_data = {}

        while offset < 2000:

            data = ckan_api.action.datastore_search(resource_id=dataset_id, offset=offset)
            for d in data['records']:

                return_data[d[name_id]] = [
                    {
                        "name": d[name_id],
                        "value": d[value_id],
                        "geography_code": d[geog_id],
                        "data_status": "A",
                        "geography": d[name_id]
                    }
                ]

            offset += 100
        return return_data

    def get_metadata_for_dataset(self, dataset_id):
        pass

    def get_dataset_overview(self, dataset_id):
        ckan_api = self.init()
        data = ckan_api.action.datastore_search(resource_id=dataset_id)

        dimensions = {}
        value_measures = []
        geog_measures = []
        name_measures = []

        for f in data['fields']:
            if f['id'] != '_id':

                value_measures.append(
                    {
                        'id': f['id'],
                        'name': f['id']
                    }
                )
                geog_measures.append(
                    {
                        'id': f['id'],
                        'name': f['id']
                    }
                )
                name_measures.append(
                    {
                        'id': f['id'],
                        'name': f['id']
                    }
                )

        dimensions['Geography'] = {
            "concept": 'Geography',
            "name": 'Geography',
            'measures': geog_measures
        }
        dimensions['Value'] = {
            "concept": 'Value',
            "name": 'Value',
            'measures': value_measures
        }
        dimensions['Name'] = {
            "concept": 'Name',
            "name": 'Name',
            'measures': name_measures
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

        found_datasets = []

        ckan_api = self.init()

        organization_show = ckan_api.action.organization_show(id=ckan_org_name, include_datasets=True)

        # print organization_show['packages']

        for p in organization_show['packages']:
            print '\n', p['id']
            package_data = ckan_api.action.package_show(id=p['id'])

            for r in package_data['resources']:
                print '\n', r['package_id'], r['datastore_active'], r['id']

                if r['datastore_active']:
                    found_datasets.append(
                        {
                            'id': r['id'],
                            'name': r['name'],
                            'source': 'CKAN_datahub'
                        }
                    )
        return found_datasets, None

