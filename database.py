from msilib.schema import Error
import psycopg2
import logging
import ipdb

conn = psycopg2.connect(database="postgres", user="postgres",
                        password="qwe123", host="127.0.0.1")

def init_tables():
    pass


def execute(sql,*args):
    try:
        cursor = conn.cursor()
        cursor.execute(sql, *args)
        cursor.close()
    except Error as e:
        logging.error(e)
