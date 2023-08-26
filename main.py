import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.s3Functions import put_object, get_signed_url, delete_object
from utils.db import establish_db_connection
import json

from dotenv import load_dotenv
from mysql.connector import Error
from datetime import datetime


# s
load_dotenv()


app = Flask(__name__)
CORS(app)


uploaded_files = []


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})


# Upload files, will also receive name of user
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # check if user exists
        # if not throw error
        connection = establish_db_connection()

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

        return jsonify({"message": "Files uploaded successfully!"}), 201

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/getFiles', methods=['GET'])
def getAllFiles():
    try:
        connection = establish_db_connection()

        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM uploaded_files")
        rows = cursor.fetchall()
        print(rows)
        # fetch the signed url for each file
        for i, row in enumerate(rows):
            rows[i] = {
                "id": row[0],
                "filename": row[1],
                "url": get_signed_url(row[2]),
                "duration": row[3],
                "fileSize": row[4],
                "fileType": row[5],
                "uploadDate": row[6]
            }
        cursor.close()
        return jsonify({"files": rows}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

# Reset the database


@app.route('/reset', methods=['GET'])
def reset():
    try:
        connection = establish_db_connection()

        cursor = connection.cursor()
        # get all the files
        cursor.execute("SELECT url FROM uploaded_files")
        rows = cursor.fetchall()
        # delete all the files
        for row in rows:
            delete_object(row[0])
        # delete all the rows
        cursor.execute("DELETE FROM uploaded_files")
        connection.commit()
        cursor.close()
        return jsonify({"message": "Database reset successfully!"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False)
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
