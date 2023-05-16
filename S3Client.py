import boto3
import os
from botocore.exceptions import ClientError


class S3Client:

    def __init__(self, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, region='us-west-2'):
        self.region = region
        self.session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                             aws_session_token=AWS_SESSION_TOKEN, region_name=region)
        self.s3_client = self.session.client('s3')
        self.s3_resource = self.session.resource('s3')

    # This function creates a new S3 bucket with the given name.
    def create_s3_bucket(self, bucket_name):
        try:
            response = self.s3_client.create_bucket(Bucket=bucket_name,
                                                    CreateBucketConfiguration={'LocationConstraint': self.region})
        except ClientError as error:
            print("Error creating Bucket!")
            print(error, "\n")
        else:
            print("Bucket created successfully!")
            print(response, "\n")

    def _user_bucket_choice(self, bucket_list):
        while True:
            bucket_number = int(input(f"Choose bucket [1-{len(bucket_list)}]: "))
            if 1 <= bucket_number <= len(bucket_list):
                return bucket_number - 1
            else:
                print("Invalid choice please try again")

    def choose_bucket(self):
        # List available buckets
        print("Listing available S3 buckets:")
        try:
            response = self.s3_client.list_buckets()
        except ClientError as error:
            print("Error!\n")
            print(error)
        else:
            bucket_list = response['Buckets']
            for idx, bucket in enumerate(bucket_list):
                print(f"{idx + 1}. {bucket['Name']}")
            # Choose bucket name
            user_choice = self._user_bucket_choice(bucket_list)
            return bucket_list[user_choice]['Name']

    # This function uploads a single file to the given S3 bucket.
    def upload_file_to_s3(self, file_path, bucket_name):
        object_name = os.path.basename(file_path)
        # Upload the file
        try:
            response = self.s3_client.upload_file(file_path, bucket_name, object_name)
        except ClientError as error:
            print("Error uploading file!\n")
            print(error)
        else:
            print("File was uploaded successfully!\n")

    # This function uploads all the files in the given directory to the given
    # S3 bucket.
    def upload_files_to_s3(self, bucket_name, files):
        for file in files:
            print(f"Uploading {file}")
            self.upload_file_to_s3(file, bucket_name)
        print("Finished uploading files\n")

    # This function lists all the objects in the given S3 bucket.
    def list_s3_objects(self, bucket_name):
        try:
            objects = self.s3_client.list_objects_v2(Bucket=bucket_name)
        except ClientError as error:
            print("Error!")
            print(error, "\n")
        else:
            file_count = objects['KeyCount']
            if file_count == 0:
                print(f"Bucket: {bucket_name}, is empty!")
                return []
            else:
                objects_list = objects['Contents']
                print("Listing all bucket\'s objects:")
                for idx, obj in enumerate(objects_list):
                    print(f"{idx + 1}. {obj['Key']}")
                return objects_list

    # This function downloads the given file from the given S3 bucket to
    # the specified path.
    def download_file_from_s3(self, bucket_name, file_name, download_path):
        local_file_path = os.path.join(download_path, file_name)
        try:
            self.s3_client.download_file(bucket_name, file_name, local_file_path)
        except ClientError as error:
            print(f"Error Downloading file {file_name}")
            print(error)
        else:
            print(f"{file_name} was downloaded successfully!")

    def _user_delete_choice(self):
        while True:
            del_choice = input("Do you wish to continue (Y/N): ")
            if (del_choice == "Y") or (del_choice == "y"):
                return True
            elif del_choice == "N" or del_choice == "n":
                return False
            else:
                print("Invalid Value, try again!")

    # This function deletes the given S3 bucket.
    def delete_s3_bucket(self, bucket_name):
        print("Checking if bucket is empty...")
        objects = self.s3_client.list_objects_v2(Bucket=bucket_name)
        file_count = objects['KeyCount']
        if file_count == 0:
            response = self.s3_client.delete_bucket(Bucket=bucket_name)
            print(f"{bucket_name} has been deleted successfully !!!")
        else:
            print(f"{bucket_name} is not empty {file_count} objects present")
            user_choice = self._user_delete_choice()
            if user_choice:
                print("Deleting objects from S3 bucket")
                objects_dict = {'Objects': [{'Key': obj['Key']} for obj in objects['Contents']], 'Quiet': False}
                del_obj_response = self.s3_client.delete_objects(Bucket=bucket_name, Delete=objects_dict)
                del_bucket_response = self.s3_client.delete_bucket(Bucket=bucket_name)
                print("Bucket was deleted successfully")
            else:
                print("Cancelling Deletion...")
