import pandas as pd
import time
import json

DATA_PATH = "../../../Dataset/"

### Merge movies and links in a single table ###
movies = pd.read_csv(DATA_PATH + "movies.csv", header=0)
movies_rank = pd.read_csv(DATA_PATH + "links.csv", header=0)
movies = movies.merge(movies_rank, on="movieId")
movies.columns=["_id", "title", "genres", "imdbId", "tmdbId"]
movies = movies.to_json("../data/movies.json", orient="records")