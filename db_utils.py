import subprocess
from pymongo import MongoClient


def get_connection(link):
    try:
        client = MongoClient(link)
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")
    return client


def dump_db():
    cmd = "mongodump --port=27117 --out=/home/artem/projects/course_work/backup"
    print(subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True))


def restore_db():
    cmd = "mongorestore --port=27117 /home/artem/projects/course_work/backup"
    print(subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True))
