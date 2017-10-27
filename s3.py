import os
import boto3, botocore

S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
S3_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

# SECRET_KEY = os.urandom(32)
# DEBUG = True
# PORT = 5000
s3 = boto3.client(
   "s3",
   aws_access_key_id = S3_KEY,
   aws_secret_access_key = S3_SECRET)


def upload_file_to_s3(file, bucket_name, acl = "public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs = {
                "ACL": acl,
                "ContentType": file.content_type
            })
    except:
        return {'Error': 'Image upload failed.'}
    return "{}{}".format(app.config["S3_LOCATION"], file.filename)
