from classes import *
import mysql.connector
import pandas as pd


def main():
    
    Database().creation_database()
    Database().connection_database()

def runQuery(sql):

    db_data = GetConfig().db_data()

    database = mysql.connector.connect(
        host=db_data.get('host'),
    database=db_data.get('database'),
    username=db_data.get('username'), 
    password=db_data.get('password'))

    cursor = database.cursor(dictionary=True)

    try:
        cursor.execute(sql)
        data = cursor.fetchall()

    except mysql.connector.Error as e:

        database.close()
        print(e)

    else:       
        dataframe = pd.DataFrame(data)
        cursor.close()
        database.close()
        print(dataframe)