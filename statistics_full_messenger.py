from collections import Counter
from statistics import Statistics
from file_reader import read_conversation_list


class FullMessengerStatistics(Statistics):
    def __init__(self, conversation_list):
        super().__init__()
        self._conversation_list = conversation_list

    @classmethod
    def from_dir(cls, dirname, without_groups=False):
        conversation_list = read_conversation_list(dirname, without_groups)
        return FullMessengerStatistics(conversation_list) if conversation_list is not None else None

    def check_specific_word_sent(self, word: str):
        word = word.lower()
        return {"specific_word_sent_res": self._basic_specific_word_sent(word)}

    def calculate(self):
        self.res.basic_messages_sent_res = self._basic_message_sent()
        self.res.basic_photos_sent_res = self._basic_photo_sent()
        self.res.basic_videos_sent_res = self._basic_video_sent()
        self.res.basic_xd_sent_res = self._basic_xd_sent()
        self.res.basic_hearts_sent_res = self._basic_heart_sent()
        self.res.basic_question_sent_res = self._basic_question_sent()
        self.res.basic_unsent_res = self._basic_unsent()
        self.res.basic_avg_msg_len_ratio_res = self._basic_avg_msg_len()

        self.res.adv_photos_and_videos_sent_res = self._adv_photos_and_videos_sent()
        self.res.adv_text_only_sent_res = self._adv_text_only_sent()

        self.res.full_reactions_res = self._reaction_sent()
        self.res.full_heart_reactions_res = self._heart_reaction()
        self.res.full_haha_reactions_res = self._haha_reaction()
        self.res.full_like_reactions_res = self._like_reaction()
        self.res.full_wow_reactions_res = self._wow_reaction()
        self.res.full_hearts_to_all_msgs_ratio_res = self._adv_hearts_to_all_msgs()
        self.res.full_reactions_to_all_msgs_ratio_res = self._adv_reactions_to_all_msgs()

        self.res.optional_haha_sent_res = self._haha_sent()
        self.res.optional_xd_to_no_xd_msgs_ratio_res = self._adv_xd_to_all_msgs()
        self.res.optional_no_xd_sent_res = self.res.basic_messages_sent_res - self.res.basic_xd_sent_res

        # self.prepare_res()

    def _basic_message_sent(self):
        res_dict = {}
        for conversation in self._conversation_list:
            res_dict[conversation.title] = len(conversation.message_list)
        return Counter(res_dict)

    def _basic_inner_list_counter(self, msg_inner_list_name):
        res_dict = {}
        for conversation in self._conversation_list:
            photos = 0
            for msg in conversation.message_list:
                msg_inner_list = getattr(msg, msg_inner_list_name)
                if msg_inner_list is not None:
                    photos += len(msg_inner_list)
            res_dict[conversation.title] = photos
        return Counter(res_dict)

    def _basic_photo_sent(self):
        return self._basic_inner_list_counter("photo_list")

    def _basic_video_sent(self):
        return self._basic_inner_list_counter("video_list")

    def _reaction_sent(self):
        return self._basic_inner_list_counter("reaction_list")

    def _basic_avg_msg_len(self):
        char_sent = self._basic_inner_list_counter("content")
        avg_msg_len = {title: round(chars / self.res.basic_messages_sent_res.get(title), 2) for title, chars
                       in char_sent.items() if self.res.basic_messages_sent_res.get(title)}
        return Counter(avg_msg_len)

    def _basic_specific_word_sent(self, word: str):
        res_dict = {}
        for conversation in self._conversation_list:
            word_per_conv = 0
            for msg in conversation.message_list:
                if msg.content is not None:
                    word_per_conv += msg.content.count(word)
            res_dict[conversation.title] = word_per_conv
        return Counter(res_dict)

    def _basic_msgs_containing_specific_word_sent(self, word: str):
        res_dict = {}
        for conversation in self._conversation_list:
            res_dict[conversation.title] = len(
                ["" for msg in conversation.message_list if msg.content is not None and word in msg.content]
            )
        return Counter(res_dict)

    def _basic_question_sent(self):
        return self._basic_msgs_containing_specific_word_sent("?")

    def _basic_xd_sent(self):
        return self._basic_specific_word_sent("xd")

    def _haha_sent(self):
        return self._basic_specific_word_sent("haha")

    def _basic_heart_sent(self):
        h1 = self._basic_specific_word_sent("❤")
        h2 = self._basic_specific_word_sent("💕")
        h3 = self._basic_specific_word_sent("💖")
        h4 = self._basic_specific_word_sent("💞")
        h5 = self._basic_specific_word_sent("💓")
        h6 = self._basic_specific_word_sent("💘")
        return h1 + h2 + h3 + h4 + h5 + h6

    def _basic_specific_reaction(self, reaction: str):
        res_dict = {}
        for conversation in self._conversation_list:
            reactions = 0
            for msg in conversation.message_list:
                if msg.reaction_list is not None:
                    for reaction_dictionary in msg.reaction_list:
                        if reaction in reaction_dictionary.values():
                            reactions += 1
            res_dict[conversation.title] = reactions
        return Counter(res_dict)

    def _heart_reaction(self):
        h1 = self._basic_specific_reaction("❤")
        h2 = self._basic_specific_reaction("💕")
        h3 = self._basic_specific_reaction("💖")
        h4 = self._basic_specific_reaction("💞")
        h5 = self._basic_specific_reaction("💓")
        h6 = self._basic_specific_reaction("💘")
        return h1 + h2 + h3 + h4 + h5 + h6

    def _haha_reaction(self):
        h1 = self._basic_specific_reaction("😂")
        h2 = self._basic_specific_reaction("😆")
        return h1 + h2

    def _like_reaction(self):
        return self._basic_specific_reaction("👍")

    def _wow_reaction(self):
        return self._basic_specific_reaction("😮")

    def _basic_unsent(self):
        res_dict = {}
        for conversation in self._conversation_list:
            res_dict[conversation.title] = len([msg for msg in conversation.message_list if msg.is_unsent])
        return Counter(res_dict)

    def _adv_ratio_x_to_all_msgs(self, x: Counter):
        ratio = {title: round(x.get(title) * 100 / msgs, 2) for title, msgs
                 in self.res.basic_messages_sent_res.items() if msgs > 1 and x.get(title) is not None}
        return Counter(ratio)

    def _adv_xd_to_all_msgs(self):
        return self._adv_ratio_x_to_all_msgs(self.res.basic_xd_sent_res)

    def _adv_hearts_to_all_msgs(self):
        return self._adv_ratio_x_to_all_msgs(self.res.basic_hearts_sent_res)

    def _adv_reactions_to_all_msgs(self):
        return self._adv_ratio_x_to_all_msgs(self.res.full_reactions_res)

    def _adv_photos_and_videos_sent(self):
        return self.res.basic_photos_sent_res + self.res.basic_videos_sent_res

    def _adv_text_only_sent(self):
        return self.res.basic_messages_sent_res - self.res.adv_photos_and_videos_sent_res

