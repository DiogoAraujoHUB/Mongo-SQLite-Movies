import pandas as pd

DATA_PATH = "../../../Dataset/"

tags = pd.read_csv(DATA_PATH + "tags.csv", header=0)

tags.to_json("../data/tags.json", orient="records")