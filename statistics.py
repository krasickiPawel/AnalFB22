from dataclasses import dataclass
from abc import abstractmethod
from typing import TypeVar, Type


T = TypeVar('T', bound='Statistics')


@dataclass
class StatisticResults:
    basic_messages_sent_res = None
    basic_photos_sent_res = None
    basic_videos_sent_res = None
    basic_hearts_sent_res = None
    basic_xd_sent_res = None
    basic_question_sent_res = None
    basic_unsent_res = None
    basic_avg_msg_len_ratio_res = None

    adv_photos_and_videos_sent_res = None
    adv_text_only_sent_res = None

    full_reactions_res = None
    full_heart_reactions_res = None
    full_haha_reactions_res = None
    full_like_reactions_res = None
    full_wow_reactions_res = None
    full_reactions_to_all_msgs_ratio_res = None
    full_hearts_to_all_msgs_ratio_res = None

    conv_reactions_received_res = None
    conv_reactions_given_res = None
    conv_heart_reactions_received_res = None
    conv_haha_reactions_received_res = None
    conv_like_reactions_received_res = None
    conv_wow_reactions_received_res = None
    conv_heart_reactions_given_res = None
    conv_haha_reactions_given_res = None
    conv_like_reactions_given_res = None
    conv_wow_reactions_given_res = None
    conv_reactions_given_to_all_messages_ratio_res = None
    conv_reactions_received_to_all_msgs_ratio_res = None
    conv_hearts_received_to_all_msgs_ratio_res = None

    optional_haha_sent_res = None
    optional_no_xd_sent_res = None
    optional_xd_to_no_xd_msgs_ratio_res = None
    optional_questions_to_all_messages_ratio_res = None

    # nieuzywane
    # wykres zdj, filmiki, tekst
    total_messages_sent_res = None
    total_photos_sent_res = None
    total_videos_sent_res = None
    total_photos_and_videos_res = None
    total_text_only_res = None

    # wykres reakcji
    total_reactions_res = None
    total_heart_reactions_res = None
    total_haha_reactions_res = None
    total_like_reactions_res = None
    total_wow_reactions_res = None

    # wykres pytania, xd, serce i pozostale
    total_xd_total_res = None
    total_question_total_res = None
    total_hearts_total_res = None

    # nieuzywane
    def _calculate_total(self):
        self.total_messages_sent_res = sum(self.basic_messages_sent_res.values())
        self.total_photos_sent_res = sum(self.basic_photos_sent_res.values())
        self.total_videos_sent_res = sum(self.basic_videos_sent_res.values())
        self.total_photos_and_videos_res = sum(self.adv_photos_and_videos_sent_res.values())
        self.total_photototal_text_only_ress_sent_res = sum(self.adv_text_only_sent_res.values())

        self.total_reactions_res = sum(self.basic_reactions_res.values())
        self.total_heart_reactions_res = sum(self.basic_heart_reactions_res.values())
        self.total_haha_reactions_res = sum(self.basic_haha_reactions_res.values())
        self.total_like_reactions_res = sum(self.basic_like_reactions_res.values())
        self.total_wow_reactions_res = sum(self.basic_wow_reactions_res.values())

        self.total_xd_total_res = sum(self.basic_xd_sent_res.values())
        self.total_question_total_res = sum(self.basic_question_sent_res.values())
        self.total_hearts_total_res = sum(self.basic_hearts_sent_res.values())

    # nieuzywane
    def _prepare_results_by_prefix(self, prefix: str, n_most_common: int):
        for attr in dir(self):
            if attr.startswith(prefix):
                setattr(self, attr, getattr(self, attr).most_common(n_most_common))

    # nieuzywane
    def _prepare_optional_results(self, n_most_common: int):
        for attr in dir(self):
            if attr.startswith("optional") and getattr(self, attr) is not None:
                setattr(self, attr, getattr(self, attr).most_common(n_most_common))

    # nieuzywane
    def prepare_results(self, n_most_common: int):
        self._calculate_total()
        self._prepare_results_by_prefix("basic", n_most_common)
        self._prepare_results_by_prefix("adv", n_most_common)
        self._prepare_optional_results(n_most_common)

    # nieuzywane
    def get_result_dict_by_prefix(self, prefix: str):
        return {attr: getattr(self, attr) for attr in dir(self) if attr.startswith(prefix) and attr.endswith("res")}

    def get_result_dict(self):
        suffix = "res"
        return {attr: getattr(self, attr) for attr in dir(self) if attr.endswith(suffix)}

    def print_result_names(self):
        suffix = "res"
        for attr in dir(self):
            if attr.endswith(suffix):
                print(attr)


class Statistics:
    def __init__(self):
        self.res = StatisticResults()

    @abstractmethod
    def calculate(self) -> None:
        pass

    @abstractmethod
    def check_specific_word_sent(self, word: str) -> list[tuple]:
        pass

    @classmethod
    @abstractmethod
    def from_dir(cls: Type[T], dirname: str) -> T:
        pass

    # def prepare_res(self) -> None:
    #     self.res.prepare_results(self.n_most_common)

    def get_res_dict(self) -> dict:
        return self.res.get_result_dict()
