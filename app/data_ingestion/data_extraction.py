from abc import ABCMeta, abstractmethod
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

DATA_DEFAULT_LOCATION = '/Users/saeed.anwar/Projects/Data-Integration-framework/data'


class ExtractKaggleData():
    """ It simply downloads the data file from web """

    def __init__(self):
        pass

    def get(self, dataset_name, file_name, seperator=','):
        api = KaggleApi()
        api.authenticate()

        api.dataset_download_file(dataset=dataset_name, file_name=file_name, path=DATA_DEFAULT_LOCATION)
        df = pd.read_csv(DATA_DEFAULT_LOCATION + file_name, sep=seperator)
        return df


def extractor(source="Kaggle"):
    """Factory Method"""
    extractors = {
        "Kaggle": ExtractKaggleData,
    }

    return extractors[source]()

