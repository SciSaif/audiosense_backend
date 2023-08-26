import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.s3Functions import put_object, get_signed_url, delete_object
from utils.db import establish_db_connection
import json
from dotenv import load_dotenv
from mysql.connector import Error
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Upload files to the database and s3


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Uploads files to the database and S3 storage.

    This endpoint expects the 'files' and 'metadata' fields in the request.
    'files' should contain the uploaded files, and 'metadata' should contain
    corresponding metadata JSON strings.

    Returns:
        JSON: Response message.
    """
    try:
        # Establish a new database connection
        connection = establish_db_connection()

        if 'files' not in request.files:
            return jsonify({"error": "No files provided"}), 400

        files = request.files.getlist('files')
        metadata_list = request.form.getlist('metadata')
        uploaded_urls = []
        cursor = connection.cursor()

        for i, file in enumerate(files):
            if file.filename == '':
                continue

            now = datetime.now()
            filepath = 'uploads/' + \
                now.strftime("%d-%m-%Y_%H-%M-%S") + '_' + file.filename
            metadata = json.loads(metadata_list[i])
            put_object(filepath, file.read())
            uploaded_urls.append(filepath)

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

# Get all files from the database


@app.route('/getFiles', methods=['GET'])
def getAllFiles():
    """
    Retrieves all files' metadata from the database along with signed URLs.

    Returns:
        JSON: List of file metadata.
    """
    try:
        connection = establish_db_connection()

        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, filename, url, duration, fileSize, fileType, uploadDate FROM uploaded_files")
        rows = cursor.fetchall()
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

# Reset the database and delete files from S3


@app.route('/reset', methods=['GET'])
def reset():
    """
    Resets the database and deletes all files from S3 storage.

    Returns:
        JSON: Response message.
    """
    try:
        connection = establish_db_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT url FROM uploaded_files")
        rows = cursor.fetchall()
        for row in rows:
            delete_object(row[0])
        cursor.execute("DELETE FROM uploaded_files")
        connection.commit()
        cursor.close()
        return jsonify({"message": "Database reset successfully!"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False)
    # Uncomment this section if using waitress
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
