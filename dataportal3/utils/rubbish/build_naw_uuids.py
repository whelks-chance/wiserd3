import os
from requests.packages.chardet.universaldetector import UniversalDetector

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")
from dataportal3 import models
from dataportal3.utils.userAdmin import get_request_user
import csv

__author__ = 'ubuntu'


# Standard CSV DictReader doesn't do unicode, so this provides decoding
def UnicodeDictReader(utf8_data, encoding='utf-8',  **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, encoding) for key, value in row.iteritems()}


def load_shapefile_description():
    filename = '/home/ubuntu/DataPortalGeographies/ConstituencyProfile/NAWDataNamesLookup.csv'
    with open(filename, 'rb') as csvfile:

        # No idea what encoding the csv file is, could have welsh chars which break things
        detector = UniversalDetector()
        detector.reset()
        for line in csvfile:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        print detector.result

        csvfile.seek(0)

        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(csvfile.read(1024))
        has_header = sniffer.has_header(csvfile.read(1024))

        print 'has_header', has_header

        csvfile.seek(0)
        # reader = csv.reader(csvfile, dialect)
        # next(reader, None)  # skip the headers

        reader = UnicodeDictReader(csvfile, encoding=detector.result['encoding'], dialect=dialect)
        for row in reader:
            print ''

            # print ', '.join(row)
            # print row.keys()
            # for key in row.keys():
            #     print(key, ' : ', row[key])
            # Shorthand Name	Category	FullName	Notes	CategoryCY	FullNameCY	NotesCY

            ssls = models.SpatialSurveyLink.objects.filter(data_name=row['Shorthand Name'])
            for link in ssls:

                link.category = row['Category']
                link.full_name = row['FullName']
                link.notes = row['Notes']
                link.category_cy = row['CategoryCY']
                link.full_name_cy = row['FullNameCY']
                link.notes_cy = row['NotesCY']

                print link.__dict__

                # link.save()

def whatever():
    id = 'wisid_RegionProfileData2016_56c377709c1c5'

    data = [u'taccpuPSch', u'accprPhar', u'popEleRol', u'accpuPSch', u'taccprGP', u'accpuFood', u'accprGP', u'hlthLLTI',
            u'taccpuPO', u'popSpkWlsh', u'taccpuLib', u'accprPO', u'taccprPhar', u'pop16to64', u'accprFood', u'taccprPSch',
            u'taccprPO', u'popTotPop', u'emyInact', u'accpuSSch', u'accprLC', u'houFlat', u'houSDet', u'accpuPO',
            u'houAll', u'taccpuFood', u'pop65plus', u'hlthLExpF', u'accprLib', u'eduThres2', u'accpuGP', u'accpuLib',
            u'taccpuLC', u'taccpuSSch', u'eduNQF4', u'hlthLExpM', u'houTer', u'accpuPhar', u'taccpuPhar', u'accprSSch',
            u'accprPetrl', u'emyEmploy', u'taccprLib', u'taccprSSch', u'accpuLC', u'houTaxEF', u'taccprFood',
            u'taccprPetr', u'taccpuGP', u'accprPSch', u'houTaxGI', u'pop0to15', u'eduNoQual', u'houTaxCD', u'emyBenClai',
            u'houDet', u'emyWkEarn', u'houTaxAB', u'taccprLC']


    for d in data:

        uuid_str = str(uuid.uuid4())

        nomis_search = models.NomisSearch()
        nomis_search.uuid = uuid_str
        nomis_search.user = get_request_user(None)
        nomis_search.dataset_id = dataset_id
        nomis_search.geography_id = geog
        nomis_search.search_attributes = codelist_to_attributes(codelist)
        nomis_search.search_type = models.SearchType.objects.get(name='Nomis')
        nomis_search.save()


load_shapefile_description()