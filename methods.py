from tqdm import tqdm
import matplotlib.pyplot as plt


class Method(object):
    """
    Abstract class to specify how to add new methods
    """

    def __init__(self, name, plot_title):
        assert name is not None, "Method needs to have a name"
        self.name = name
        self.fig = plt.figure(figsize=(15, 7))
        self.plot_title = plot_title

    def __call__(self, queries, log_scale=False, filename="plot.jpg", *args, **kwargs) -> None:
        print(f"Executing Method: {self.name}.")
        t = tqdm(queries)

        for query in t:
            t.set_description(query['query'])
            self._do(query)

        plt.legend()
        plt.title(self.plot_title)
        if log_scale:
            self.fig.gca().set_yscale('log')

        self.fig.savefig(f"plots/{filename}")
        self.fig.show()

    def plot_groupby(self, grp, label):
        self.fig.gca().plot(grp.index, grp.values, label=label)
        plt.xticks(list(grp.index))

    def _do(self, query) -> None:
        """
        Method to execture the method
        :param query:
        :return:
        """
        raise NotImplementedError("This method is abstract. Please implement this method when inherit from 'Method'")


class CountPapersMethod(Method):
    """
    Method to count the numbers of Papers over the years and plotting it.
    """

    def __init__(self):
        super(CountPapersMethod, self).__init__("count_paper", "Number of papers based on the year")

    def _do(self, query) -> None:
        grp = query['data'].groupby('year').count()['title']
        self.plot_groupby(grp, query['query'])


class CountsOfWordInSummary(Method):
    def __init__(self, word: str):
        super(CountsOfWordInSummary, self).__init__('count_words', f"Number of Papers with the word {word} in title")
        self.word = word

    def _do(self, query) -> None:
        query['data']['occ'] = query['data'].summary.str.count(self.word)
        grp = query['data'].groupby('year').sum().occ
        self.plot_groupby(grp, query['query'])
