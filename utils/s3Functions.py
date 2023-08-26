import boto3
import os

# Replace this with the appropriate region alias
cloudflare_region_alias = 'apac'  # For example, 'apac' for Asia-Pacific

s3 = boto3.client(
    's3',
    endpoint_url=f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com/",
    aws_access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
    config=boto3.session.Config(signature_version='s3v4'),
    region_name=cloudflare_region_alias
)

bucket_name = 'audiosense'


def put_object(file_path, file_data):
    s3.put_object(Bucket=bucket_name, Key=file_path, Body=file_data)
    return f"https://{bucket_name}.{cloudflare_region_alias}.{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com/{file_path}"


def get_signed_url(file_path):
    params = {
        'Bucket': bucket_name,
        'Key': file_path
    }
    return s3.generate_presigned_url('get_object', Params=params, ExpiresIn=3600)
