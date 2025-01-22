import pymysql
import os
from dotenv import load_dotenv
load_dotenv()
# import psycopg2

def connection_database():
    connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='to_do',
            charset = "utf8mb4" 
                        )
    
    return connection

def sql_connection_update(query, params=None, safe=False):
    connection = None
    result = None
    try:
        connection = connection_database()
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
            result = cursor.rowcount
    except Exception as e:
        print(e)
    finally:
        if connection:
            connection.close()
    return result


def sqlConnectionFetch(sql, params):
    connection = connection_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchall()  
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in result]

        for row in result:
            for key, value in row.items():
                if isinstance(value, bytes):
                    try:
                        row[key] = value.decode('utf-8')
                    except UnicodeDecodeError:
                        row[key] = value.decode('latin-1')

        connection.commit()
    finally:
        connection.close()
    return result

def fetch_query(sql, params=None):
    try:
        return sqlConnectionFetch(sql, params)
    except Exception as e:
        raise RuntimeError(f"Database query failed: {str(e)}")
    
def update_query(sql, params=None):
    try:
        return sql_connection_update(sql, params)
    except Exception as e:
        raise RuntimeError(f"Database query failed: {str(e)}")