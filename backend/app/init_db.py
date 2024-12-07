import os
from pymongo import MongoClient
import subprocess

def is_database_empty(db):
    collections = db.list_collection_names()
    return len(collections) == 0

def main():
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client.credit_database
    if is_database_empty(db):
        print("База данных пустая или не существует. Выполняем дамп...")
        subprocess.run(["python", "-m", "database.dump"])
    else:
        print("База данных уже существует и не пустая. Дамп не требуется.")

if __name__ == "__main__":
    main()
