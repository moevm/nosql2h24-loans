from pymongo import MongoClient
from flask import Flask, jsonify, request

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["credit_database"]

if 'credit_collection' not in db.list_collection_names():
    collection = db.create_collection('credit_collection')
else:
    collection = db['credit_collection']
    collection.drop()

data = {"message": "Hello world!"}
collection.insert_one(data)

@app.route("/", methods=["GET"])
def get_items():
    items = list(collection.find())
    for item in items:
        item["_id"] = str(item["_id"])
    return jsonify(items)


@app.route("/", methods=["POST"])
def add_item():
    # new_item = request.json
    # collection.insert_one(new_item)
    return jsonify(data), 201


def main():
    app.run(host="0.0.0.0", port=1234, debug=True)


if __name__ == "__main__":
    main()
