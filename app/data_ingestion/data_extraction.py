from abc import ABCMeta, abstractmethod
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import zipfile

DATA_DEFAULT_LOCATION = '/Users/saeed.anwar/Projects/Data-Integration-framework/data/'


def unzip(file_name):
    zip_file_path = DATA_DEFAULT_LOCATION + file_name + ".zip"
    print(f"Zip File Path: {zip_file_path}")

    try:
        with zipfile.ZipFile(zip_file_path) as z:
            z.extractall(DATA_DEFAULT_LOCATION)
    except zipfile.BadZipFile as e:
        raise ValueError(
            'Bad zip file, please report on '
            'www.github.com/kaggle/kaggle-api', e)
    except FileNotFoundError as e:
        print(f"File not zipped!", e)
        return


class ExtractKaggleData():
    """ It simply downloads the data file from web """

    def get_data(self, dataset_name, file_name, seperator=','):
        api = KaggleApi()
        api.authenticate()

        response = api.dataset_download_file(dataset=dataset_name, file_name=file_name, path=DATA_DEFAULT_LOCATION)
        print("Kaggle API download response: ", response)

        unzip(file_name)

        df = pd.read_csv(DATA_DEFAULT_LOCATION + file_name, sep=seperator)
        return df


def extractor(source="Kaggle"):
    """Factory Method"""
    extractors = {
        "Kaggle": ExtractKaggleData,
    }

    return extractors[source]()


if __name__ == "__main__":
    dataset_name = 'johnybhiduri/us-crime-data'
    file_name = 'US_Crime_Data.csv'

    df = extractor("Kaggle").get_data(dataset_name=dataset_name, file_name=file_name)
    print(df)
