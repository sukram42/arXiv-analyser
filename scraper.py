import time
import datetime
import feedparser
import pandas as pd
from tqdm import trange

import matplotlib.pyplot as plt

# If debug is True, then only one of the queries is applied on 2 years
DEBUG = False

TOPICS = [#"graph",
          "anomaly detection time series",
          "anomaly detection",
          "anomaly detection graphs",
          "anomaly detection autoencoder VAE",
          "anomaly detection GAN generative", "meta learning"]


if DEBUG:
    TOPICS = ['graph']
    START_YEAR = 1995
    END_YEAR = 1996
else:
    START_YEAR = 1995
    END_YEAR = 2021


def map_entries(entry):
    """
    Function to map over each scientific paper.
    :param entry:
    :return:
    """
    _res = {}
    date = datetime.datetime.strptime(entry['published'], "%Y-%m-%dT%H:%M:%SZ")
    _res['published'] = date
    _res['summary'] = entry['summary']
    _res['year'] = date.year
    _res['title'] = entry['title']
    _res['authors'] = list(map(lambda x: x['name'], entry['authors']))
    _res['cat'] = entry['arxiv_primary_category']['term']
    return _res


def filter_year(p_year):
    def _filter(entry):
        return entry['year'] == int(p_year)

    return _filter


plt.figure(figsize=(15, 7))
for topic in TOPICS:
    MAX_NUMBER = 10000
    URL = "http://export.arxiv.org/api/query"
    QUERY_ITEM = "search_query"

    entries = []
    t = trange(START_YEAR, END_YEAR + 1)
    t.set_description(topic.replace(' ', '+'))
    for year in t:
        t.set_postfix({"year": str(year)})
        query = f"{URL}?{QUERY_ITEM}=all:{topic.replace(' ', '+')}+'{year}'&max_results={MAX_NUMBER}"
        res = feedparser.parse(query)
        res = list(filter(filter_year(year), map(map_entries, res['entries'])))
        entries.extend(res)

        # Wait a bit in behalf of the server
        for i in range(6):
            time.sleep(5)

    res_df = pd.DataFrame.from_dict(entries)

    grp = res_df.groupby('year').count()['title']
    plt.plot(list(grp.index.astype(str)), grp.values, label=f"{topic.replace(' ', '+')}+<year>")

    # Waiting to not send too many requests
    print("Wait 30 seconds ... ")
    for i in trange(6):
        time.sleep(5)

    res_df.to_json(f"data/{topic.replace(' ', '+')}.json", orient="records")
plt.legend()
plt.title('Development of Research in Anomaly Detection based on $arxiv.com$')
plt.savefig(f'data/analysis_{START_YEAR}_to_{END_YEAR}.png')
plt.show()

if __name__ == '__main__':
    pass
