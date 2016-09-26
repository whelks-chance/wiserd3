import requests


def do_post_xls(xls_file):
    url = 'http://localhost:8000/data_api?method=topojson_layer_by_name&name=region'
    data = {

    }
    res = requests.post(url, data=data)

if __name__ == '__main__':
    xls_file = '/home/ianh/Downloads/Copy of place and welshness new percentages.xlsx'

    resp1 = do_post_xls(xls_file)
