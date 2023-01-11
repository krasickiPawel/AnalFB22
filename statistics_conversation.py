from collections import Counter
from statistics import Statistics
from file_reader import read_conversation


class ConversationStatistics(Statistics):
    def __init__(self, conversation):
        super().__init__()
        self._conversation = conversation

    @classmethod
    def from_dir(cls, dirname):
        conversation = read_conversation(dirname)
        return ConversationStatistics(conversation) if conversation is not None else None

    def check_specific_word_sent(self, word: str):
        word = word.lower()
        return {"specific_word_sent_res": self._basic_specific_word_sent(word)}

    def calculate(self):
        self._calculate_basic_results()
        self._calculate_adv_results()
        # self.prepare_res()

    def _calculate_basic_results(self):
        self.res.basic_messages_sent_res = Counter([msg.sender_name for msg in self._conversation.message_list])
        self.res.basic_photos_sent_res = self._basic_inner_list_counter("photo_list")
        self.res.basic_videos_sent_res = self._basic_inner_list_counter("video_list")
        self.res.basic_xd_sent_res = self._basic_specific_word_sent("xd")
        self.res.basic_hearts_sent_res = self._basic_hearts_sent()
        self.res.basic_question_sent_res = self._basic_question_sent()
        self.res.basic_unsent_res = Counter([msg.sender_name for msg in self._conversation.message_list if msg.is_unsent])
        self.res.basic_avg_msg_len_ratio_res = self._basic_avg_msg_len()

        self.res.conv_reactions_received_res = self._basic_inner_list_counter("reaction_list")
        self.res.conv_reactions_given_res = self._reactions_given()
        self.res.conv_heart_reactions_received_res, self.res.conv_heart_reactions_given_res = self._heart_reactions()
        self.res.conv_haha_reactions_received_res, self.res.conv_haha_reactions_given_res = self._haha_reactions()
        self.res.conv_like_reactions_received_res, self.res.conv_like_reactions_given_res = self._like_reactions()
        self.res.conv_wow_reactions_received_res, self.res.conv_wow_reactions_given_res = self._wow_reactions()

    def _calculate_adv_results(self):
        self.res.basic_hearts_sent_res = self._adv_hearts_sent()

        self.res.conv_reactions_given_to_all_messages_ratio_res = self._adv_ratio_x_to_all_msgs(self.res.conv_reactions_given_res)
        self.res.conv_reactions_received_to_all_msgs_ratio_res = self._adv_ratio_x_to_all_msgs(self.res.conv_reactions_received_res)
        self.res.conv_hearts_received_to_all_msgs_ratio_res = self._adv_ratio_x_to_all_msgs(self.res.conv_heart_reactions_received_res)

        self.res.adv_photos_and_videos_sent_res = self.res.basic_photos_sent_res + self.res.basic_videos_sent_res
        self.res.adv_text_only_sent_res = self.res.basic_messages_sent_res - self.res.adv_photos_and_videos_sent_res

        self.res.optional_no_xd_sent_res = self.res.basic_messages_sent_res - self.res.basic_xd_sent_res
        self.res.optional_xd_to_no_xd_msgs_ratio_res = self._adv_ratio_x_to_all_msgs(self.res.basic_xd_sent_res)
        self.res.optional_questions_to_all_messages_ratio_res = self._adv_ratio_x_to_all_msgs(self.res.basic_question_sent_res)

    def _reactions_given(self):
        name_list = []
        for msg in self._conversation.message_list:
            if msg.reaction_list is not None:
                for dictionary in msg.reaction_list:
                    name_list.append(dictionary["actor"])
        return Counter(name_list)

    def _basic_inner_list_counter(self, msg_inner_list_name: str):
        name_list = []
        for msg in self._conversation.message_list:
            msg_inner_list = getattr(msg, msg_inner_list_name)
            if msg_inner_list is not None:
                for _ in msg_inner_list:
                    name_list.append(msg.sender_name)
        return Counter(name_list)

    def _basic_avg_msg_len(self):
        char_sent = self._basic_inner_list_counter("content")
        avg_msg_len = {name: round(chars / self.res.basic_messages_sent_res.get(name), 2) for name, chars
                       in char_sent.items() if self.res.basic_messages_sent_res.get(name)}
        return Counter(avg_msg_len)

    def _basic_specific_word_sent(self, word: str):
        name_list = []
        for msg in self._conversation.message_list:
            if msg.content is not None:
                for _ in range(msg.content.count(word)):
                    name_list.append(msg.sender_name)
        return Counter(name_list)

    def _basic_msgs_containing_specific_word_sent(self, word: str):
        name_list = []
        for msg in self._conversation.message_list:
            if msg.content is not None and word in msg.content:
                name_list.append(msg.sender_name)
        return Counter(name_list)

    def _basic_question_sent(self):
        return self._basic_msgs_containing_specific_word_sent("?")

    def _basic_hearts_sent(self):
        single = self._basic_specific_word_sent("❤")
        double = self._basic_specific_word_sent("💕")
        sparkling = self._basic_specific_word_sent("💖")
        beating = self._basic_specific_word_sent("💓")
        revolving = self._basic_specific_word_sent("💞")
        arrow = self._basic_specific_word_sent("💘")
        return single + double + sparkling + arrow + beating + revolving

    def _specific_reactions(self, reaction: str):
        received = []
        given = []
        for msg in self._conversation.message_list:
            if msg.reaction_list is not None:
                for reaction_dictionary in msg.reaction_list:
                    if reaction_dictionary.get("reaction") == reaction:
                        given.append(reaction_dictionary.get("actor"))
                        received.append(msg.sender_name)
        return Counter(given), Counter(received)

    def _heart_reactions(self):
        h1_s, h1_r = self._specific_reactions('❤')
        h2_s, h2_r = self._specific_reactions('💕')
        return h1_r + h2_r, h1_s + h2_s

    def _haha_reactions(self):
        h1_s, h1_r = self._specific_reactions('😂')
        h2_s, h2_r = self._specific_reactions('😆')
        return h1_r + h2_r, h1_s + h2_s

    def _adv_hearts_sent(self):
        exclamation = self._basic_specific_word_sent("❣")
        y = self._basic_specific_word_sent("💛")
        g = self._basic_specific_word_sent("💚")
        b = self._basic_specific_word_sent("❣")
        p = self._basic_specific_word_sent("💜")
        bck = self._basic_specific_word_sent("🖤")
        w = self._basic_specific_word_sent("🤍")
        return self.res.basic_hearts_sent_res + exclamation + y + g + b + p + bck + w

    def _like_reactions(self):
        l1_s, l1_r = self._specific_reactions('👍')
        return l1_r, l1_s

    def _wow_reactions(self):
        w1_s, w1_r = self._specific_reactions('😮')
        return w1_r, w1_s

    def _adv_ratio_x_to_all_msgs(self, x: Counter):
        ratio = {name: round(x.get(name) * 100 / msgs, 2) for name, msgs
                 in self.res.basic_messages_sent_res.items() if msgs and x.get(name) is not None}
        return Counter(ratio)

