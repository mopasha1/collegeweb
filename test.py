from pymongo import MongoClient


# MongoDB configuration
client = MongoClient('localhost', 27017)
db = client['rating_and_reviews']
collection = db['reviews']

doc = {
    "name": "Dr. Phil",
    "subjects": "Phsychiatry, Psychology",
    "avg_rating": 5,
    "num_ratings": 1,
    "reviews": [{"name": "Moiz", "rating": 5, "class": "Psychology", "comment": "Talks to people"}],
    "description": "Dr. Dolittle likes working with people"
}

collection.insert_one(doc)