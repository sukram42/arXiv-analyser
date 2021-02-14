from os import listdir

import pandas as pd

# Load data
from methods import CountPapersMethod, CountsOfWordInSummary

files = filter(lambda x: x.endswith('.json'), listdir('data'))
files = list(map(lambda x: {"query": x.split('.')[0], "data": pd.read_json(f'data/{x}')}, files))

# Count papers
CountPapersMethod()(queries=files)
CountsOfWordInSummary('graph')(queries=files)


if __name__ == '__main__':
    pass