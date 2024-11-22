import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["foodpicker"]
meals_collection = db["meals"]

def filter_foods(tag):
    print(tag)
    if tag == "kinder" or tag == "eltern":
        query = {"tags": tag}
        results = [food for food in meals_collection.find(query)]
        return results
    return []
