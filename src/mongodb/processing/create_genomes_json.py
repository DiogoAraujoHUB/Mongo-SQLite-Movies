import pandas as pd
import json
from time import time

DATA_PATH = "../../../Dataset/"

genome_tags = pd.read_csv(DATA_PATH + "genome-tags.csv", header=0, index_col="tagId")
genome_tags = dict(zip(genome_tags.index, genome_tags.tag))

genome_scores = pd.read_csv(DATA_PATH + "genome-scores.csv", header=0)
genome_scores["tag"] = genome_scores.tagId.map(genome_tags)
genome_scores.drop(columns="tagId", inplace=True)

start = time()
genome_scores.to_json("../data/genomes.json", "records")
print(time() - start)