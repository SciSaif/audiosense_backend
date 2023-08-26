import os
import mysql.connector


def establish_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        ssl_ca=os.getenv("SSL_CERT")
    )


# try:
#     if connection.is_connected():
#         cursor = connection.cursor()
#     cursor.execute("select @@version ")
#     version = cursor.fetchone()
#     if version:
#         print('Running version: ', version)
#     else:
#         print('Not connected.')
#     # get all the tables
#     # cursor.execute("select * from uploaded_files")
#     # tables = cursor.fetchall()
#     # print(tables)
# except Error as e:
#     print("Error while connecting to MySQL", e)
