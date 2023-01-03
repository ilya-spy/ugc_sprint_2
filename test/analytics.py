import datetime
import uuid
import random

from pymongo import MongoClient
from pymongo.database import Database

NUM_INSERT = 10000
NUM_FETCH = 1000

mongo = MongoClient('localhost', 27017)
db = mongo.default

# Retrieve initialized collections
ratings = db.ratings
bookmarks = db.bookmarks

print(ratings)
print(bookmarks)

# insert data measure
start = datetime.datetime.now()
for i in range(NUM_INSERT):
    ratings.insert_one({"id": i, "user_id": str(uuid.uuid4()), "film_id": str(uuid.uuid4()), "rating": random.randint(1,10)})
end = datetime.datetime.now()

print('MongoDB INSERT runtime performance: ', end-start)

# search for records
start = datetime.datetime.now()
for i in range(NUM_FETCH):
    id_num = random.randint(0, 15000)
    ratings.find_one({"id": id_num})
end = datetime.datetime.now()

print('MongoDB FETCH runtime performance: ', end-start)
