import pandas as pd
import json
import time

DATA_PATH = "../../../Dataset/"

ratings = pd.read_csv(DATA_PATH + "ratings.csv", header=0)

ratings.to_json("../data/ratings.json", "records")