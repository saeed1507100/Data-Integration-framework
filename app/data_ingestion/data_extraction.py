from kaggle.api.kaggle_api_extended import KaggleApi
from google.cloud import bigquery
import pandas as pd
import os
from app.data_ingestion import utils

DATA_DEFAULT_LOCATION = './'


class ExtractKaggleData():
    """ It simply downloads the data file from Kaggle """

    def get_data(self, dataset_name, file_name, user_name, key, seperator=','):
        api = KaggleApi()
        api.authenticate()

        os.environ['KAGGLE_USERNAME'] = user_name
        os.environ['KAGGLE_KEY'] = key

        response = api.dataset_download_file(dataset=dataset_name, file_name=file_name, path=DATA_DEFAULT_LOCATION)
        print("Kaggle API download response: ", response)
        utils.unzip(DATA_DEFAULT_LOCATION, file_name)

        return pd.read_csv(DATA_DEFAULT_LOCATION + file_name, sep=seperator)


class ExtractGoogleCloudData:
    """ It simply downloads data from Google cloud public Dataset """

    def get_data(self, query, file_name):
        client = bigquery.Client()
        query_job = client.query(query)
        query_result = query_job.result()
        df = query_result.to_dataframe()
        print(df)
        df.to_csv(DATA_DEFAULT_LOCATION+file_name, index=False)

        return df


def extractor(source="Kaggle"):
    """Factory Method"""
    extractors = {
        "Kaggle": ExtractKaggleData,
        "Google-Cloud": ExtractGoogleCloudData
    }

    return extractors[source]()


if __name__ == "__main__":
    dataset_name = 'johnybhiduri/us-crime-data'
    file_name = 'US_Crime_Data.csv'

    # Kaggle example
    # df = extractor("Kaggle").get_data(dataset_name=dataset_name, file_name=file_name)
    # print(df)
    df = extractor("Google-Cloud").get_data(
        query="SELECT * FROM `bigquery-public-data.covid19_nyt.us_states` where date='2020-10-01'")
    print(df)
