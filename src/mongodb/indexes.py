import pandas as pd
from pymongo import MongoClient
import time

client = MongoClient()
db = client.Project_BDA

gs=db["Genome Scores"]
m=db["Movies"]
r=db["Ratings"]
t=db["Tags"]
tag = "007 (series)"

GenomesIndex = gs.create_index([("relevance",-1),("movie_id",1)])
MoviesIndex=m.create_index([("_id",1),("title",1)])
RatingsIndex=r.create_index([("userId",1),("rating",-1)])
TagsIndex=t.create_index([("tag",1),("movie_id",1)])

query1={"$and":[{'relevance': {'$gt':0.9}},{"tag":"007"}]}
query2={"$and":[{"genres":{"$regex":"Comedy"}},{"genres":{"$regex":"Horror"}},{"genres":{"$regex":"Drama"}},{"genres":{"$regex":"Thriller"}},{"genres":{"$regex":"Crime"}}]}
query3={"$and":[{"rating":{"$gt":4}},{"movie_id":1}]}
query4={"$and":[{"movie_id":1},{"userId":{"$gt":100000}}]}

#genomefinder=gs.find(query1)
#for i in genomefinder:
    #print(i)

#Moviesfinder=m.find(query2)
#for i in Moviesfinder:
    #print(i)

#Ratingsfinder=r.find(query3)
#for i in Ratingsfinder:
    #print(i)

#Tagsfinder=t.find(query4)
#for i in Tagsfinder:
    #print(i)
