# -*- coding: utf-8 -*-
from collections import Counter
import matplotlib.pyplot as plt


TITLES = {
    'basic_messages_sent_res': 'Wysłane wiadomości',
    'basic_photos_sent_res': 'Wysłane zdjęcia',
    'basic_videos_sent_res': 'Wysłane filmiki',
    'basic_hearts_sent_res': 'Wysłane ❤ (nie reakcje)',
    'basic_xd_sent_res': 'Wysłane "XD" (w każdej odmianie)',
    'basic_question_sent_res': 'Wysłane znaki zapytania "?"',
    'basic_unsent_res': 'Usunięte wiadomości',
    'basic_avg_msg_len_ratio_res': 'Średnia długość wiadomości [liczba znaków]',

    'adv_photos_and_videos_sent_res': 'Wysłane zdjęcia i filmiki',
    'adv_text_only_sent_res': 'Wiadomości bez multimediów',

    'full_reactions_res': 'Liczba reakcji',
    'full_heart_reactions_res': 'Reakcje ❤',
    'full_haha_reactions_res': 'Reakcje 😆',
    'full_like_reactions_res': 'Reakcje "like"',
    'full_wow_reactions_res': 'Reakcje 😮',
    'full_reactions_to_all_msgs_ratio_res': 'Stosunek reakcji do wszystkich wiadomości [%]',
    'full_hearts_to_all_msgs_ratio_res': 'Stosunek wysłanych ❤ do wszystkich wiadomości [%]',

    'conv_reactions_received_res': 'Otrzymane reakcje',
    'conv_reactions_given_res': 'Dane reakcje',
    'conv_heart_reactions_received_res': 'Otrzymane reakcje ❤',
    'conv_haha_reactions_received_res': 'Otrzymane reakcje 😆',
    'conv_like_reactions_received_res': 'Otrzymane reakcje "like"',
    'conv_wow_reactions_received_res': 'Otrzymane reakcje 😮',
    'conv_heart_reactions_given_res': 'Dane reakcje ❤',
    'conv_haha_reactions_given_res': 'Dane reakcje 😆',
    'conv_like_reactions_given_res': 'Dane reakcje "like"',
    'conv_wow_reactions_given_res': 'Dane reakcje 😮',
    'conv_reactions_given_to_all_messages_ratio_res': 'Stosunek reakcji danych do wszystkich wiadomości [%]',
    'conv_reactions_received_to_all_msgs_ratio_res': 'Stosunek reakcji otrzymanych do wszystkich wiadomości [%]',
    'conv_hearts_received_to_all_msgs_ratio_res': 'Stosunek otrzymanych reakcji ❤ do wszystkich wiadomości [%]',

    'optional_haha_sent_res': 'Wysłane "haha"',
    'optional_no_xd_sent_res': 'Wiadomości bez "XD"',
    'optional_xd_to_no_xd_msgs_ratio_res': 'Stosunek wiadomości "XD" do niezawierających "XD" [%]',
    'optional_questions_to_all_messages_ratio_res': 'Stosunek wiadomości zawierających "?" do wszystkich wiadomości [%]'
}


def _get_chart_description(name_counter: str, res_counter: Counter, word: str = None) -> tuple[str, str, Counter, bool]:
    name_top, val_top = res_counter.most_common(1)[0]
    name_top = name_top[:77]
    if word is not None:
        total = sum(res_counter.values())
        title = f'Wysłane "{word}" ze wszystkich {total}'
        leader_label = f"Najwięcej: {name_top} - {val_top}"
        pie = False
    elif "ratio" in name_counter:
        title_txt = TITLES.get(name_counter)
        title = f"{title_txt}"
        leader_label = f"Lider: {name_top} - {val_top}"
        pie = False
    else:
        res_counter_val = res_counter.values()
        total = sum(res_counter_val)
        title_context = TITLES.get(name_counter)
        title = f"{title_context} ze wszystkich {total}"
        leader_label = f"Najwięcej: {name_top} - {val_top}"
        pie = True if len(res_counter_val) < 3 else False
    renamed_keys_counter_dict = Counter({f"{key[:37]} - {val}": val for key, val in res_counter.items()})
    return title, leader_label, renamed_keys_counter_dict, pie


def prepare_chart_data(res_dict: dict, n_most_common=40, word=None) -> dict:
    chart_data_dict = dict()
    for attr, res_counter in res_dict.items():
        if res_counter is None or not res_counter:
            continue
        title, leader_label, renamed_keys_counter_dict, pie = _get_chart_description(attr, res_counter, word)
        chart_data_dict[attr] = {
            "title": title,
            "leader_label": leader_label,
            "res_list": renamed_keys_counter_dict.most_common(n_most_common),
            "pie": pie,
        }
    return chart_data_dict


def make_charts(chart_data_dict: dict) -> list[plt.Figure]:
    chart_fig_list = []
    for val_data_dict in chart_data_dict.values():
        plt.figure(figsize=(11.5, 9), dpi=100)
        plt.title(val_data_dict.get("title"))
        plt.xlabel(val_data_dict.get("leader_label"))
        if val_data_dict.get("pie"):
            zipped = [x for x in zip(*val_data_dict.get("res_list"))]
            plt.pie(zipped[1], labels=zipped[0])
            plt.legend()
        else:
            plt.subplots_adjust(left=0.35)
            plt.margins(0.02)
            plt.barh(*zip(*val_data_dict.get("res_list")))
            plt.gca().invert_yaxis()
        chart_fig_list.append(plt.gcf())
    return chart_fig_list


def get_chart_list(res_dict: dict, n_most_common=40, word=None):
    return make_charts(prepare_chart_data(res_dict, n_most_common, word))
