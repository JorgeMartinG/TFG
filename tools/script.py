import json
import mysql.connector
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


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


class Database:

    def __init__(self) -> None:

        self.data = GetConfig().db_data()

        # Database Parameters
        self.sql_file = self.data.get('file')
        self.hostname = self.data.get('host')
        self.database = self.data.get('database')
        self.username = self.data.get('username')
        self.password = self.data.get('password')
        self.sql_file_path = '{}\\{}'.format(PROJECT_ROOT, self.sql_file)

        self.errors = GetConfig().error_data()

        # Connection error messages
        self.create_success = self.errors.get('create_success')
        self.connect_success = self.errors.get('con_success')
        self.create_error = self.errors.get('create_error')
        self.connect_error = self.errors.get('con_error')
        
    def connection(self) -> None:

        try:
            database = mysql.connector.connect(
                host=self.hostname,
                username=self.username, 
                password=self.password)
        except mysql.connector.Error as err:
            print(f"{self.connect_error}{self.database}:{err}")
        else:
            print(f"{self.connect_success}{self.database}")
            cursor = database.cursor()
            with open(self.sql_file_path, 'r') as f:
                try:
                    cursor.execute(f.read(), multi=True)
                except mysql.connector.Error as err:
                    print(f"{self.create_error}{self.database}:{err}")
                else:
                    print(f"{self.create_success}{self.database}")
                    return database


Database().connection()
