import random
import pymongo.errors
import boto3
import logging
from pymongo import MongoClient
from botocore.exceptions import ClientError


class Advertisement:
    def __init__(self, email, description, path):
        self.email = email
        self.description = description
        self.path = path
        self.id = 0
        self.state = "pending"
        self.category = ""
        self.db = DataBase()

    def post(self):
        try:
            self.id = int(random.randrange(0, pow(10, 10)))
            self.db.post({"_id": self.id, "email": self.email, "description": self.description,
                          "path": self.path, "state": self.state, "category": self.category})
        except pymongo.errors.DuplicateKeyError:
            self.post()

    def update(self, post_id):
        self.db.update(post_id, "accepted", "vehicle")


class S3:
    def __init__(self):
        self.bucket_name = 'adimages'
        logging.basicConfig(level=logging.INFO)
        try:
            self.s3_client = boto3.client(
                's3',
                endpoint_url='your s3 url',
                aws_access_key_id='your s3 access key',
                aws_secret_access_key='your s3 secret access key'
            )

        except Exception as exc:
            logging.error(exc)

    def upload(self, path, name):
        try:
            self.s3_client.upload_file(path, self.bucket_name, name)
        except ClientError as e:
            logging.error(e)

    def download(self, path, name):
        try:
            self.s3_client.download_file(self.bucket_name, name, path)

        except ClientError as e:
            logging.error(e)


class DataBase:
    def __init__(self):
        self.cluster = MongoClient("your mongoDB cluster")
        self.db = self.cluster["Advertisements"]
        self.collection = self.db["Advertisement"]

    def post(self, post):
        self.collection.insert_one(post)

    def update(self, post_id, state, category):
        newvals = {"$set": {"state": state, "category": category}}
        self.collection.update_one({"_id": post_id}, newvals)

    def show(self, post_id):
        results = self.collection.find_one({"_id": post_id})
        return results

