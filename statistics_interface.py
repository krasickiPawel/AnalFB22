import matplotlib.pyplot as plt
from statistics import Statistics
from charts import get_chart_list as gcl
from statistics_conversation import ConversationStatistics


class StatisticsInterface:
    def __init__(self, statistics_obj: Statistics, n_most_common: int = 40):
        self._statistics_obj = statistics_obj
        self._n_most_common = n_most_common

    @classmethod
    def from_dir(cls, statistics_class: Statistics, dirname: str, n_most_common: int = 40):
        statistics_obj = statistics_class.from_dir(dirname)
        return StatisticsInterface(statistics_obj) if statistics_obj is not None else None

    def set_n_most_common(self, n_most_common):
        self._n_most_common = n_most_common

    def calculate(self) -> None:
        self._statistics_obj.calculate()

    def check_specific_word(self, word: str):
        res = self.check_specific_word(word)
        return gcl(res, self._n_most_common, word)

    def get_chart_list(self) -> list[plt.Figure]:
        res = self._statistics_obj.get_res_dict()
        return gcl(res, self._n_most_common)


path3 = "censored"


if __name__ == '__main__':
    stat = StatisticsInterface.from_dir(ConversationStatistics, path3)
    stat.calculate()
    charts = stat.get_chart_list()
    for c in charts:
        c.show()
