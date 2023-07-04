import json
from pymongo import MongoClient

client = MongoClient()
db = client.Project_BDA

coll_gen = db["Genome_Scores"]
coll_ratings = db["Ratings"]
coll_movies = db["Movies"]
coll_tags = db["Tags"]

#Obtain and update the ratings for a movie in the dataset
#This updates the files and not the dataset itself, so it wont be added to queries created
#(As its more a processing file than a query)
query1 = [
    {"$match" : {"_id" : 1}},
    {"$lookup" : {
        "from" : "Ratings",
        "localField" : "ratings",
        "foreignField" : "_id",
        "as" : "ratings"
    }},
    {"$unwind" : "$ratings"},
    {"$project" : {
        "_id" : 0,
        "ratings" : 1
    }}
]

docs = coll_movies.aggregate(query1)
x = {}

def poper(x : dict, *args):
    for key in args:
        x.pop(key)
    return x

ratings = list(map(lambda x: poper(x, "_id", "movieId"), map(lambda x: x["ratings"], docs)))
with open("./data/movie_1_ratings.json","w") as f:
    json.dump(ratings, f)