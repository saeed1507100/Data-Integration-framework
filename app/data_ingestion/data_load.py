import pandas as pd
import sqlalchemy

DATA_DEFAULT_LOCATION = './'


class LoadDataToPostgres:

    def load_data(self, config):
        """
            Utility function to insert a Dataframe to a table in Supabase postgres DB.
            If the table does not exist, it will be created.

            Args:
                file_name (str): The csv file name of downloaded data
                table (str): The Name of the Table
                db_reference_id (str): The reference_id from supabase db
                db_password (str): The password of the supabase db
        """
        try:
            file_name = config['file_name']
            table = config['table_name']
            dest = config['destination']
            if_exists = config['if_exists']

            db = dest['database']
            user = dest['username']
            password = dest['password']
            host = dest['host']
            port = dest['port']

            engine = sqlalchemy.create_engine(
                f'postgresql://{user}:{password}@{host}:{port}/{db}')
            dataframe = pd.read_csv(DATA_DEFAULT_LOCATION + file_name, index_col=False)
            dataframe.to_sql(table, con=engine, if_exists=if_exists, index=False)
            print(f"Data loaded into table: {table}")
        except Exception as E:
            error_msg = '{}: Data insertion failed {}'.format(table, E)
            print(error_msg)
            raise ValueError(error_msg)


def loader(destination="Supabase"):
    """Factory Method"""
    loaders = {
        "postgres": LoadDataToPostgres,
        # "Google-Cloud": ExtractGoogleCloudData
    }

    return loaders[destination]()
