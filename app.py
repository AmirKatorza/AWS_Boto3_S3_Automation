import os
from S3Client import S3Client
from credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN


def main():
    s3client = S3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)

    flag = True
    while flag:

        print("-------------MENU---------------------")
        print("1. Create S3 bucket")
        print("2. Upload a single file to S3 bucket")
        print("3. Upload multiple files to S3 bucket")
        print("4. Download File from S3")
        print("5. List files in S3")
        print("6. Delete a S3 bucket")
        print("7. Quit")
        print("--------------------------------------\n")

        user_choice = input("Please enter your choice: ")

        if user_choice == "1":
            bucket_name = input("Please enter bucket name: ")
            s3client.create_s3_bucket(bucket_name)

        elif user_choice == "2":
            file_path = input("Please enter file path to upload: ")
            bucket_name = s3client.choose_bucket()
            s3client.upload_file_to_s3(file_path, bucket_name)

        elif user_choice == "3":
            base_dir = input("Enter directory path to upload: ")
            files_path = []
            for entry in os.listdir(base_dir):
                file_path = os.path.join(base_dir, entry)
                if os.path.isfile(file_path):
                    files_path.append(file_path)
            bucket_name = s3client.choose_bucket()
            s3client.upload_files_to_s3(bucket_name, files_path)

        elif user_choice == "4":
            print("Choose a bucket you wish to download from")
            bucket_name = s3client.choose_bucket()
            print(f"Listing all object in bucket: {bucket_name}")
            objects_list = s3client.list_s3_objects(bucket_name)
            while True:
                idx_file = int(input(f"Please choose file number you wish to download [1-{len(objects_list)}]: "))
                if 1 <= idx_file <= len(objects_list):
                    break
                else:
                    print("Invalid Value, please try again")
            file_name = objects_list[idx_file - 1]['Key']
            download_path = input("please choose folder to download file to: ")
            s3client.download_file_from_s3(bucket_name, file_name, download_path)

        elif user_choice == "5":
            print("Choose a bucket to list objects")
            bucket_name = s3client.choose_bucket()
            objects_list = s3client.list_s3_objects(bucket_name)

        elif user_choice == "6":
            print("Choose a bucket you wish to delete: ")
            bucket_name = s3client.choose_bucket()
            s3client.delete_s3_bucket(bucket_name)

        elif user_choice == "7":
            print("Exiting...")
            flag = False
        else:
            print("Invalid Value, please enter a valid number [1-7]")


if __name__ == "__main__":
    main()
