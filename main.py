import os

from app.data_ingestion.data_extraction import extractor
from app.data_ingestion.data_load import loader

QUERY = "SELECT * FROM `bigquery-public-data.covid19_nyt.us_states` where date='2020-10-01'"
FILE_NAME = "covid19_us_states_20201001.csv"

if __name__ == '__main__':
    dataset_name = 'johnybhiduri/us-crime-data'
    file_name = 'US_Crime_Data.csv'

    df = extractor("Kaggle").get_data(dataset_name=dataset_name, file_name=file_name)
    print(df)

    df = extractor("Google-Cloud").get_data(query=QUERY,file_name=FILE_NAME)
    print(df)
    loader("Supabase").load_data(file_name="covid19_us_states_20201001.csv",
                                 table='covid19_us_states',
                                 db_reference_id=os.environ['SUPABASE_DB_REFERENCE_ID'],
                                 db_password=os.environ['SUPABASE_DB_PASSWORD'])
