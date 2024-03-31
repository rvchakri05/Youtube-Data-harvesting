from youtube import *
import mysql.connector
import youtube
from sqlalchemy import create_engine
engine=create_engine(url="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database_name))
def is_database_exists(database_name):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password)
    cursor = connection.cursor()
    try:
        cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in cursor.fetchall()]
        if database_name in databases:
            for t in tb_name:
                create_tables(t)
        else:
            try:
                cursor.execute(f"CREATE DATABASE {database_name}")
                for t in tb_name:
                    create_tables(t)
            except mysql.connector.Error as err:
                print(f"Error: {err}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

def create_tables(table_name):
    connection = mysql.connector.connect(
                        host=host,
                        user=user,
                        password=password,
                        database=database_name)
    cursor = connection.cursor()
    try:
        if table_name == "channel_data":
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                id VARCHAR(255) PRIMARY KEY,
                c_name VARCHAR(255),
                c_subscriber INT,
                c_views INT,
                c_description VARCHAR(1000),
                c_publish datetime,
                c_dp VARCHAR(1000)
            )""")
        elif table_name == "video_data":
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                id VARCHAR(255) PRIMARY KEY,
                c_id VARCHAR(255),
                v_name VARCHAR(1000),
                v_description VARCHAR(10000),
                V_publish datetime,
                view_count INT,
                like_count INT,
                favourite_count INT,
                comment_count INT,
                duration time,
                thumbnail VARCHAR(1000),
                v_url VARCHAR(255),
                FOREIGN KEY(c_id) REFERENCES channel_data(id) ON DELETE CASCADE
                
            )""")
        elif table_name == "comment_data":
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                id VARCHAR(255) PRIMARY KEY,
                v_id VARCHAR(255),
                c_id VARCHAR(255),
                comment_text VARCHAR(8000),
                comment_author VARCHAR(255),
                comment_published datetime,
                FOREIGN KEY(v_id) REFERENCES video_data(id),
                FOREIGN KEY(c_id) REFERENCES channel_data(id) ON DELETE CASCADE
            )""")
        else:
            print("Invalid table name")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()
        insert_data_into_table(table_name)
def insert_data_into_table(table_name):
    try:
        global data
        if table_name=="channel_data":
            data=channel_data1
        elif table_name== "video_data":
            data=youtube.video_data1
        elif table_name=="comment_data":
            data=youtube.comment_data1
        df = pd.DataFrame.from_dict(data)
        df.to_sql(table_name, con=engine, if_exists="append", index=False)
        print(f"Data inserted into '{table_name}' successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
def id_exist(channel_id):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password)
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [database[0] for database in cursor.fetchall()]
    if database_name not in databases:
        is_database_exists(database_name)
    else:
        connection = mysql.connector.connect(
                        host=host,
                        user=user,
                        password=password,
                        database=database_name)
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM channel_data WHERE id= '{channel_id}'")
        result = cursor.fetchone()[0]
        if result > 0:
            cursor.execute(f"DELETE FROM channel_data WHERE id='{channel_id}'")
        else:
            is_database_exists(database_name)





