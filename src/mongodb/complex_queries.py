from pymongo import MongoClient
from time import time
from pprint import pprint
client = MongoClient()
db = client.Project_BDA

#Selecionar os filmes com maior 'rating' relevantes a uma tag (tagid).
#Os filmes em consideração para a pesquisa 
#são que têm uma certa tag como a mais relevante
tag = "007 (series)"
query1 = [
            {"$group" : {
                    "_id" : "$movieId",
                    "relevance" : {"$max" : "$relevance"},
                }
            },
            {"$lookup" : {
                "from" : "Genome_Scores",
                "let" : {"movieid":"$_id", "rel":"$relevance"},
                "pipeline":[{
                    "$match" : {"$expr" : {
                        "$and" : [
                            {"$eq" : ["$movieId", "$$movieid"]},
                            {"$eq" : ["$relevance", "$$rel"]}
                        ]
                    }}
                }],
                "as" : "records"
                }
            },
            {"$unwind" : "$records"},
            { "$match" : {"records.tag" : tag}},
            # { "$project" : {
            #     "_id" : 1,
            #     "tag" : "$records.tag"
            # }},
            # {"$match" : {"tag" : tag}},
            # {"$project" : {
            #     "_id" : 1,
            # }},
            {"$lookup" : {
                "from" : "Ratings",
                "localField" : "_id",
                "foreignField" : "movieId",
                "as" : "rating"
            }},
            {"$unwind" : "$rating"},
            {"$group" : {
                "_id" : "$_id",
                "rating" : {"$avg" : "$rating.rating"},
                "counts" : {"$sum" : 1}
            }}, 
            {"$match" : {
                "counts" : {"$gte" : 100}
            }},
            {"$lookup" : {
                "from" : "Movies",
                "localField" : "_id",
                "foreignField" : "_id",
                "as" : "movie"
            }},
            {"$unwind" : "$movie"},
            {"$project" : {
                "_id" : 0,
                "title" : "$movie.title",
                "rating" : 1
            }},
            {"$sort" : {"rating" : -1}}
        ]

# Subqueries utilizadas na query 2
movieid = 1
subsubquery = [
    # {"$project" : {"_id" : 0,"movieId" : 1,"tag" : {"$toLower" : {"$trim" : {"input": "$tag"}}},}},
    {"$group" : {
        "_id" : {
            "movieid" : "$movieId", 
            "tag" : "$tag"
        },
        "counts" : {"$sum" : 1}
    }},
]
subquery = [
    *subsubquery,
    {"$group" : {
        "_id" : "$_id.movieid",
        "counts" : {"$max" : "$counts"}
    }},
    {"$lookup" : {
        "from" : "Tags",
        "let" : {
            "movieid": "$_id", 
            "counts" : "$counts"
        },
        "pipeline" : [
            *subsubquery,
            {"$match" : {
                "$expr" : {
                    "$and" : [
                        {"$eq" : ["$_id.movieid", "$$movieid"]},
                        {"$eq" : ["$counts", "$$counts"]}
                    ]
                }
            }},
        ],
        "as" : "tags"
    }},
    {"$unwind":"$tags"},
    # {"$limit" : 10}
]

#Obter os filmes cujas tags por
# utilizador mais frequentes
# coincidem com as de um
# certo filme escolhido à priori
## ** Procurar por filmes semelhantes ao selecionado **
query2 = [
    *subquery,
    {"$match" : {"_id" : movieid}},
    {"$lookup" : {
        "from" : "Tags",
        "let" : {
            "movieid" : "$_id",
            "tag" : "$tags._id.tag"
        },
        "pipeline" : [
            *subquery,
            {"$match" : {
                "$expr" : {
                    "$and" : [
                        {"$ne" : ["$_id", "$$movieid"]},
                        {"$eq" : ["$tags._id.tag", "$$tag"]}
                    ]
                }
            }},
        ],
        "as" :"matches"
    }},
    {"$unwind" : "$matches"},
    {"$project" : {
        "_id" : 0,
        "_id1" : "$_id",
        # "tag1" : "$tags._id.tag",
        "_id2" : "$matches._id",
        # "tag2" : "$matches.tags._id.tag"
    }},
    {"$sort" : {"_id2": 1}}
]

# Obter o average rating de um filme
movieid = 200
query3 = [
    {"$match" : {"_id" : movieid}},
    {"$lookup" : {
        "from" : "Ratings_v2",
        "localField" : "_id",
        "foreignField" : "movieId",
        "as": "rating"
    }},
    {"$unwind" : "$rating"},
    {"$group" : {
        "_id" : "$title",
        "rating" : {"$avg" : "$rating.rating"}
    }}
]

# Obter o average rating de um filme
# Igual à query anterior, só que utilizando um agrupamento dos ratings em vez dos movies (resultado igual)
query3_2 = [
    {"$match" : {"movieId" : movieid}},
    {"$group" : {
        "_id" : "$movieId",
        "rating" : {"$avg" : "$rating"}
    }},
    {"$lookup" : {
        "from" : "Movies",
        "localField" : "_id",
        "foreignField" : "_id",
        "as" : "movie"
    }},
    {"$unwind" : "$movie"},
    {"$project" : {
        "_id" : "$movie.title",
        "rating" : "$rating"
    }}
]

# Obter o average rating de um filme
# Igual á query anterior, só que mais simples
query4 = [
    {"$match" : {"_id" : movieid}},
    {"$project" : {
        "_id" : "$title",
        "rating" : {"$avg" : "$ratings.rating"}
    }},
]

coll_gen = db["Genome_Scores"]
coll_ratings = db["Ratings"]
coll_movies = db["Movies"]
coll_tags = db["Tags"]


start = time()
# pprint(db.command('aggregate', 'Genome_Scores', pipeline=query, explain=True))
# docs = coll_gen.aggregate(query1)
docs = coll_tags.aggregate(query2, collation = {"locale" : "en", "strength":2})

# docs = coll_movies.aggregate(query3)
# docs = coll_ratings.aggregate(query3_2)
# docs = coll_movies.aggregate(query4)

print(time() - start)

input()
for item in docs:
    print(item)