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

print '\norganization_show'

organization_show = ckan.action.organization_show(id=ckan_org_name, include_datasets=True)

print organization_show['packages']

print 'group_show'

print ckan.action.group_show(id=ckan_org_name)

print ckan.action.group_package_show(id=ckan_org_name)
