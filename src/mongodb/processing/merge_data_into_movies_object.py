import pandas as pd
import time
import json

def get_json(file):
    with open(file, "r") as f:
        var = json.load(f)
        f.close()
    return var

DATA_PATH = "../../../Dataset/"

### Merge movies and links in a single table ###
movies = pd.read_csv(DATA_PATH + "movies.csv", header=0)
movies_rank = pd.read_csv(DATA_PATH + "links.csv", header=0)
movies = movies.merge(movies_rank, on="movieId")
movies = movies.to_dict(orient="records")

genomes = get_json("../data/genomes.json")
tic=time.time()
movies = list(map(lambda x,y: x|{"genome_scores": y}, movies, genomes))
print(time.time() - tic)
del genomes

with open("../data/tags_list.json", "r") as f:
    tags = json.load(f)
    f.close()

tic=time.time()
movies = list(map(lambda x,y: x|{"tags": y}, movies, tags))
print(time.time() - tic)
del tags

with open("../data/ratings_list.json", "r") as f:
    ratings = json.load(f)
    f.close()

tic = time.time()
movies = list(map(lambda x,y: x|{"ratings":y}, movies, ratings))
print(time.time() - tic)

print(json.dumps(movies[0], indent=4))
with open("../data/all_data.json", "w") as f:
    json.dump(movies, f)
    f.close()
