import sqlalchemy


class LoadDataToSupabase:

    def load_data(self, dataframe, table: str, db_reference_id: str, db_password: str):
        """
            Utility function to insert a Dataframe to a table in Supabase postgres DB.
            If the table does not exist, it will be created.

            Args:
                dataframe (pandas.DataFrame): The pandas dataframe to be inserted in DB
                table (str): The Name of the Table
                db_reference_id (str): The reference_id from supabase db
                db_password (str): The password of the supabase db
        """
        try:
            engine = sqlalchemy.create_engine(
                f'postgresql://postgres:{db_password}@db.{db_reference_id}.supabase.co:5432/postgres')
            dataframe.to_sql(table, con=engine, if_exists="append", index=False)
            print(f"Data loaded into table: {table}")
        except Exception as E:
            error_msg = '{}: Data insertion failed {}'.format(table, E)
            print(error_msg)
            raise ValueError(error_msg)



def loader(destination="Supabase"):
    """Factory Method"""
    loaders = {
        "Supabase": LoadDataToSupabase,
        # "Google-Cloud": ExtractGoogleCloudData
    }

    return loaders[destination]()
