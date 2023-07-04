from pymongo import MongoClient
from time import time

client = MongoClient()
db = client.Project_BDA

coll_gen = db["Genome_Scores"]
coll_ratings = db["Ratings"]
coll_movies = db["Movies"]
coll_tags = db["Tags"]

# Update ao rating que um utilizador deu
userid = 134
rating = 3.5
query = [
    { "userId" : userid },
    { "$set" : {"rating" : rating}}
]

start = time()
coll_ratings.update_many(*query)
print(time() - start)
