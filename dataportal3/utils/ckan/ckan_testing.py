import json
import pprint

import ckanapi

# demo = ckanapi.RemoteCKAN('http://demo.ckan.org',
#     user_agent='ckanapiexample/1.0 (+http://example.com/my/website)')
# groups = demo.action.group_list(id='data-explorer')
# print groups
from wiserd3.settings import ckan_api_key, ckan_org_name

ckan = ckanapi.RemoteCKAN('https://datahub.io',
    user_agent='ckanapiexample/1.0 (+http://example.com/my/website)',
                          apikey=ckan_api_key)

print '\nuser_show'

print ckan.action.user_show(id='wiserd_dataportal')

print '\norganization_activity_list'

print ckan.action.organization_activity_list(id=ckan_org_name)

print '\norganization_revision_list'

print ckan.action.organization_revision_list(id=ckan_org_name)

print '\norganization_show:packages'

organization_show = ckan.action.organization_show(id=ckan_org_name, include_datasets=True)

print organization_show['packages']

for p in organization_show['packages']:
    print '\n', p['id']

    print '\npackage data'

    package_data = ckan.action.package_show(id=p['id'])

    print package_data['resources']

    for r in package_data['resources']:

        print '\n', r['package_id'], r['datastore_active'], r['id']

        print '\ndatastore_search'

        print ckan.action.datastore_search(resource_id=r['id'])

