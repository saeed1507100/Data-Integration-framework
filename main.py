from app.data_ingestion.data_extraction import extractor

if __name__ == '__main__':
    dataset_name = 'johnybhiduri/us-crime-data'
    file_name = 'US_Crime_Data.csv'

    df = extractor("Kaggle").get_data(dataset_name=dataset_name, file_name=file_name)
    print(df)