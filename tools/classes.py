import json
import mysql.connector
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
RED = "\033[91m"
GRE = "\033[92m"
END = "\033[0m"


class GetConfig:

    def __init__(self) -> None:
        
        self.config_file = 'json\config.json'
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
        self.sql_conn = self.errors.get('sql_conn')
        self.db_creat = self.errors.get('creation')
        self.dbs_conn = self.errors.get('dbs_conn')
        self.data_ins = self.errors.get('data_ins')
        self.scess_in = self.errors.get('scss_msg')   
        self.faild_at = self.errors.get('fail_msg')

        # Database data file
        self.data = '{}\\{}'.format(PROJECT_ROOT, self.datafiles.get('data'))

    def creation_database(self) -> None:

        try:
            database = mysql.connector.connect(
                host=self.hostname,
                username=self.username, 
                password=self.password)

        except mysql.connector.Error as mysql_conn_e:
            print(f'{self.sql_conn}{RED}{self.faild_at}{END}: {mysql_conn_e}')

        else:
            print(f'{self.sql_conn}{GRE}{self.scess_in}{END}\t({database.get_server_info()})')
            cursor = database.cursor()
            

            with open(self.sql_file_path, 'r') as f:
                try:
                    for query in cursor.execute(f.read() , multi=True):
                        query.fetchall()
                    
                    database.commit()

                except mysql.connector.Error as db_creation_e:
                    print(f'{self.db_creat}{RED}{self.faild_at}{END}, {db_creation_e}')

                else:     
                    print(f'{self.db_creat}{GRE}{self.scess_in}{END}')
                    cursor.close()
                    database.close()
                    
    def connection_database(self) -> None:

        try:
            database = mysql.connector.connect(
                host=self.hostname,
                database=self.database,
                username=self.username, 
                password=self.password)

        except mysql.connector.Error as db_conn_e:
            print(f'{self.dbs_conn}{self.database}: {RED}{self.faild_at}{END}, {db_conn_e}')

        else:
            print(f'{self.dbs_conn}{self.database}: {GRE}{self.scess_in}{END}')
            cursor = database.cursor()

            with open(self.data, 'r') as f:

                try:
                    for query in cursor.execute(f.read() , multi=True):
                        query.fetchall()

                    database.commit()

                except mysql.connector.Error as data_ins_e:
                    print(f'{self.data_ins}{self.database}: {RED}{self.faild_at}{END}, {data_ins_e}')
                
                else:
                    print(f'{self.data_ins}{self.database}: {GRE}{self.scess_in}{END}')
                    cursor.close()
                    database.close()