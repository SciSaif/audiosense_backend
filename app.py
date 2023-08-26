import MySQLdb
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.s3Functions import put_object, get_signed_url
import json

from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
from datetime import datetime


load_dotenv()

# connection = MySQLdb.connect(
#     host=os.getenv("DB_HOST"),
#     user=os.getenv("DB_USERNAME"),
#     passwd=os.getenv("DB_PASSWORD"),
#     db=os.getenv("DB_NAME"),
#     autocommit=True,
#     ssl_mode="VERIFY_IDENTITY",
#     ssl={
#         "ca": "/etc/ssl/cert.pem"
#     }
# )

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    ssl_ca=os.getenv("SSL_CERT")
)


try:
    if connection.is_connected():
        cursor = connection.cursor()
    cursor.execute("select @@version ")
    version = cursor.fetchone()
    if version:
        print('Running version: ', version)
    else:
        print('Not connected.')
    # get all the tables
    # cursor.execute("select * from uploaded_files")
    # tables = cursor.fetchall()
    # print(tables)
except Error as e:
    print("Error while connecting to MySQL", e)


app = Flask(__name__)
CORS(app)


uploaded_files = []


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files provided"}), 400

        files = request.files.getlist('files')
        # Get list of metadata JSON strings
        metadata_list = request.form.getlist('metadata')
        uploaded_urls = []
        cursor = connection.cursor()

        for i, file in enumerate(files):
            if file.filename == '':
                continue

            # current date and time
            now = datetime.now()

            filepath = 'uploads/' + \
                now.strftime("%d-%m-%Y_%H-%M-%S") + '_' + file.filename

            # Parse metadata JSON string
            metadata = json.loads(metadata_list[i])
            put_object(filepath, file.read())
            uploaded_urls.append(filepath)
            print(metadata)

            # Save the file metadata to the database along with uploaded file URL
            cursor.execute(
                "INSERT INTO uploaded_files (filename, url, duration, fileSize, fileType) VALUES (%s, %s, %s, %s, %s)",
                (file.filename, filepath,
                 metadata['duration'], metadata['fileSize'], metadata['fileType'])
            )
            connection.commit()
        cursor.close()

        return jsonify({"uploaded_urls": uploaded_urls}), 201

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/getFiles', methods=['GET'])
def getAllFiles():
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, filename, url, duration, fileSize, fileType FROM uploaded_files")
        rows = cursor.fetchall()
        # fetch the signed url for each file
        for i, row in enumerate(rows):
            rows[i] = {
                "id": row[0],
                "filename": row[1],
                "url": get_signed_url(row[2]),
                "duration": row[3],
                "fileSize": row[4],
                "fileType": row[5]
            }
            print(rows[i])
        cursor.close()
        return jsonify({"files": rows}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    # signed_url = get_signed_url(file_name)
    # return jsonify({"download_url": signed_url})


if __name__ == '__main__':
    app.run(debug=True)
