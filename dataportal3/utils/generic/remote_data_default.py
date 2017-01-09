
class RemoteDataDefault():
    def __init__(self):
        pass

    def get_metadata_for_dataset(self, dataset_id):
        raise NotImplemented('')

    def keyword_search(self, keyword_string, args=None):
        raise NotImplemented('')

    def get_data_dict(self, dataset_id, options, constants):
        raise NotImplemented('')
