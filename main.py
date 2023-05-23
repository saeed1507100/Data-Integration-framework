import os

from app.data_ingestion.data_extraction import extractor
from app.data_ingestion.data_load import loader
from pymongo.mongo_client import MongoClient

QUERY = "SELECT * FROM `bigquery-public-data.covid19_nyt.us_states` where date='2020-10-01'"
FILE_NAME = "covid19_us_states_20201001.csv"


def get_config():
    uri = "mongodb+srv://dev:xQinxvkB8D7zn7tF@configdb.krybqe8.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client['configdb']
    config = db['integration_configuration'].find()
    return config


if __name__ == '__main__':
    dataset_name = 'johnybhiduri/us-crime-data'
    file_name = 'US_Crime_Data.csv'

    # df = extractor("Kaggle").get_data(dataset_name=dataset_name, file_name=file_name)
    # print(df)
    #
    # df = extractor("Google-Cloud").get_data(query=QUERY,file_name=FILE_NAME)
    # print(df)
    # loader("Supabase").load_data(file_name="covid19_us_states_20201001.csv",
    #                              table='covid19_us_states',
    #                              db_reference_id=os.environ['SUPABASE_DB_REFERENCE_ID'],
    #                              db_password=os.environ['SUPABASE_DB_PASSWORD'])

    configurations = get_config()
    for config in configurations:
        print(config['description'])
        source_type = config['source']['type']
        df = extractor(source_type).get_data(config)
        print(df)

        destination_type = config['destination']['type']
        loader(destination_type).load_data(config)


