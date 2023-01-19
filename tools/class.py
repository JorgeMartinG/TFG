import json
import mysql.connector
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
RED = "\033[91m"
GRE = "\033[92m"
END = "\033[0m"


class GetConfig:

    def __init__(self) -> None:
        
        self.config_file = 'config.json'
        self.config_path = f'{PROJECT_ROOT}\\{self.config_file}'
        
    def get_data(self) -> dict:

        with open(self.config_path) as f:
            config = json.load(f)
        return config

    def db_data(self) -> dict:

        data = self.get_data().get('database')
        return data

    def error_data(self) -> dict:

        errors = self.get_data().get('errorcode')
        return errors
    
    def data_files(self) -> dict:

        datafiles = self.get_data().get('datafile')
        return datafiles 


class Database:

    def __init__(self) -> None:

        self.data = GetConfig().db_data()
        self.errors = GetConfig().error_data()
        self.datafiles = GetConfig().data_files()

        # Database Parameters
        self.sql_file = self.data.get('file')
        self.hostname = self.data.get('host')
        self.database = self.data.get('database')
        self.username = self.data.get('username')
        self.password = self.data.get('password')
        self.sql_file_path = '{}\\{}'.format(PROJECT_ROOT, self.sql_file)

        # Connection error messages
        self.mysql_connection = self.errors.get('connect')
        self.create = self.errors.get('create')
        self.db_connect = self.errors.get('db_connect')
        self.insert = self.errors.get('data_insert')
        self.success = self.errors.get('success') 
        self.failed = self.errors.get('failed')

        # Database data file
        self.data = '{}\\{}'.format(PROJECT_ROOT, self.datafiles.get('data'))

    def creation_database(self) -> None:

        try:
            database = mysql.connector.connect(
                host=self.hostname,
                username=self.username, 
                password=self.password)

        except mysql.connector.Error as err:
            print(f'{self.mysql_connection}{RED}{self.failed}{END}: {err}')

        else:
            print(f'{self.mysql_connection}{GRE}{self.success}{END}\t({database.get_server_info()})')
            cursor = database.cursor()
            

            with open(self.sql_file_path, 'r') as f:
                try:
                    for query in cursor.execute(f.read() , multi=True):
                        query.fetchall()
                    
                    database.commit()

                except mysql.connector.Error as err:
                    print(f'{self.create}{RED}{self.failed}{END}, {err}')

                else:     
                    print(f'{self.create}{GRE}{self.success}{END}')
                    cursor.close()
                    database.close()
                    
    def connection_database(self):

        try:
            database = mysql.connector.connect(
                host=self.hostname,
                database=self.database,
                username=self.username, 
                password=self.password)

        except mysql.connector.Error as err:
            print(f'{self.db_connect}{self.database}: {RED}{self.failed}{END}, {err}')

        else:
            print(f'{self.db_connect}{self.database}: {GRE}{self.success}{END}')
            cursor = database.cursor()

            with open(self.data, 'r') as f:

                try:
                    for query in cursor.execute(f.read() , multi=True):
                        query.fetchall()

                    database.commit()

                except mysql.connector.Error as err:
                    print(f'{self.insert}{self.database}: {RED}{self.failed}{END}, {err}')
                
                else:
                    print(f'{self.insert}{self.database}: {GRE}{self.success}{END}')
                    cursor.close()
                    database.close()



 
Database().creation_database()
Database().connection_database()