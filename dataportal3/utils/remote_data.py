from pandasdmx import Request

__author__ = 'ubuntu'


class RemoteData():
    def __init__(self):
        pass

    def get_remote_data(self, survey_id):

        ecb = Request().get(url='https://www.neighbourhood.statistics.gov.uk/NDE2/Deli')
        cat_resp = ecb.get(resource_type = 'categoryscheme')

        print cat_resp.msg.__dict__

rd = RemoteData()
rd.get_remote_data('')