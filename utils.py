from bson.objectid import ObjectId

# For mongo-db queries
def fetch_all(collection):
    all_docs = list(collection.find())
    for doc in all_docs:
        print(doc)

def del_record_with_name(name,collection):
    collection.delete_one({"name": name})

def delete_all(collection):
    collection.delete_many({})

