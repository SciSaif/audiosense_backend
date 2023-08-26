import os
import mysql.connector


def establish_db_connection():
    """
    Establishes a connection to the MySQL database using environment variables.

    Returns:
        mysql.connector.connect: The database connection object.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        ssl_ca=os.getenv("SSL_CERT")
    )
