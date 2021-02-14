from tqdm import tqdm
import matplotlib.pyplot as plt


class Method(object):
    """
    Abstract class to specify how to add new methods
    """
    def __init__(self, name):
        assert name is not None, "Method needs to have a name"
        self.name = name
        self.fig = plt.figure(figsize=(15, 7))

    def __call__(self, queries, *args, **kwargs) -> None:
        print(f"Executing Method: {self.name}.")
        t = tqdm(queries)

        for query in t:
            t.set_description(query['query'])
            self._do(query)

        plt.legend()
        plt.title('Number of Papers based on the year')
        self.fig.show()

    def plot_groupby(self, grp, label):
        self.fig.gca().plot(grp.index, grp.values, label=label)

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
        super(CountPapersMethod, self).__init__("count_paper")

    def _do(self, query) -> None:
        grp = query['data'].groupby('year').count()['title']
        self.plot_groupby(grp, query['query'])


class CountsOfWordInSummary(Method):
    def __init__(self, word: str):
        super(CountsOfWordInSummary, self).__init__('count_words')
        self.word = word

    def _do(self, query) -> None:
        query['data']['occ'] = query['data'].summary.str.count(self.word)
        grp = query['data'].groupby('year').sum().occ
        self.plot_groupby(grp, query['query'])

