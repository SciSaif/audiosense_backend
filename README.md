# AudioSense backend

AudioSense is a web application for uploading and managing audio files. This project provides a Flask server that handles file uploads, stores metadata in a MySQL database, and stores the files on a Cloudflare R2 storage service.

## Prerequisites

- Python >= 3.6
- Set up an environment with required packages: `pip install -r requirements.txt`

## Setup

1. Clone the repository: `git clone https://github.com/scisaif/audiosense_backend.git`
2. Install required packages: `pip install -r requirements.txt`
3. Set up your environment variables by creating a `.env` file in the root directory:
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USERNAME=your_database_username
DB_PASSWORD=your_database_password
SSL_CERT=your_ssl_certificate_path
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key_id
R2_SECRET_ACCESS_KEY=your_secret_access_key


## Usage

1. Run the Flask application: `python main.py`
2. Access the endpoints:
   - `POST /upload`: Upload files to the database and S3 storage.
   - `GET /getFiles`: Retrieve all files' metadata along with signed URLs.
   - `GET /reset`: Reset the database and delete files from S3 storage.

## Client Repository

For the client-side code that interacts with this server, check out the [Client Repo](https://github.com/scisaif/audiosense_client).

## Demo

Check out the live demo of the AudioSense app at [audiosense.vercel.app](https://audiosense.vercel.app).

## Additional Information

Provide any other relevant information about your project.

