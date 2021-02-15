from os import listdir

import pandas as pd

# Load data
from methods import CountPapersMethod, CountsOfWordInSummary
exlude_file = ["anomaly+detection+time+series+analysis.json"]

files = filter(lambda x: x.endswith('.json'), listdir('data'))
files = set(files) - set(exlude_file)
files = list(map(lambda x: {"query": x.split('.')[0], "data": pd.read_json(f'data/{x}')}, files))

# Count papers
CountPapersMethod()(queries=files, filename="paper-count.jpg ")
CountsOfWordInSummary('graph')(queries=files,
                               log_scale=True,
                               filename="word-count-log.jpg")
CountsOfWordInSummary('graph')(queries=files,
                               log_scale=False,
                               filename="word-count-not-log.jpg")


if __name__ == '__main__':
    pass