#%% 


from sql_info import sql_info

from info_insta import info_insta
from profiles_names import profiles
import numpy as np
import pandas as pd
from instagram_posts_scraper import InstagramPostsScraper
from sqlalchemy import create_engine

class MySQLConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.engine = create_engine(f'mysql+mysqlconnector://{self.user}:{self.password}@{self.host}/{self.database}')

    def insert_rows(self, table_name: str, dataframe: pd.DataFrame):
        if dataframe is None or dataframe.empty:
            print("Dataframe is null or empty, nothing to insert.")
            return
        with self.engine.connect() as con:
            result = con.execute(f"SHOW TABLES LIKE '{table_name}'")
            if not result.fetchone():
                raise ValueError(f"Table {table_name} does not exist.")
            dataframe.to_sql(table_name, self.engine, if_exists='append', index=False)

    
    def select_all_from_data(self, table_name: str) -> pd.DataFrame:
        with self.engine.connect() as con:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, self.engine)
            return df

        
    def universal_query(self, querry: str, returnList = False) -> pd.DataFrame:
        with self.engine.connect() as con:
            df = pd.read_sql(querry, self.engine)
            if returnList:
                return np.hstack(df.values.tolist())
            return df
    def create_table(self, table_name: str):
        with self.engine.connect() as con:
            result = con.execute(f"SHOW TABLES LIKE '{table_name}'")
            if result.fetchone():
                print(f"Table {table_name} already exists.")
            else:
                con.execute(f"""CREATE TABLE {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    profile_name VARCHAR(255) NOT NULL,
                    date DATE NOT NULL,
                    content TEXT NOT NULL
                )""")
                print(f"Table {table_name} has been created.")

    def check_table_existence(self, table_name: str) -> bool:
        with self.engine.connect() as con:
            result = con.execute(f"SHOW TABLES LIKE '{table_name}'")
            return bool(result.fetchone())

    def add_table(self, table_name: str, columns: dict):
        if self.check_table_existence(table_name):
            print(f"Table {table_name} already exists.")
            return
        with self.engine.connect() as con:
            column_definitions = [f"{column} {data_type}" for column, data_type in columns.items()]
            column_definitions_str = ", ".join(column_definitions)
            con.execute(f"CREATE TABLE {table_name} ({column_definitions_str})")
            print(f"Table {table_name} has been created.")
                

        
#%%
def main():
    connection = MySQLConnection(sql_info['host'], sql_info['user'],
                                 sql_info['password'], sql_info['database'])

    columns = {"id": "INT AUTO_INCREMENT PRIMARY KEY", "column1": "VARCHAR(255) NOT NULL", "column2": "DATE NOT NULL"}
    connection.add_table("new_table", columns)

    df = connection.universal_query('SELECT profile_name, COUNT(*) FROM posts GROUP BY profile_name')
    print(df.head())
if __name__ == '__main__':
    main() 

#%%

# def create_table_and_insert_rows():
    
#     scraper = InstagramPostsScraper(info_insta['user'], info_insta['password'])
#     df = scraper.get_posts_from_timerange('harrykane')
    
#     connection = MySQLConnection(host=sql_info['host'], user=sql_info['user'],
#                                  password=sql_info['password'], database=sql_info['database'])
    
#     table_name = 'create_table_and_insert_rows'
    
#     connection.create_table(table_name)
#     connection.insert_rows(table_name, df)

# def insert_many_rows():
#     scraper = InstagramPostsScraper(info_insta['user'], info_insta['password'])
#     connection = MySQLConnection(host=sql_info['host'], user=sql_info['user'],
#                                     password=sql_info['password'], database=sql_info['database'])
#     for profile in profiles:
#         print(profile)
#         df = scraper.get_posts_from_timerange(profile)
#         connection.insert_rows('insert_many_rows', df)


# # %%
# connection = MySQLConnection(host=sql_info['host'], user=sql_info['user'],
#                                 password=sql_info['password'], database=sql_info['database'])


# connection.universal_query('SELECT count(distinct(profile_name)) FROM instagram.posts')
# %%
