import json
import glob
from file_holder import Conversation, Message, ConversationList
from file_decoder import decode_string, decode_list_of_dictionaries


def read_json(filename):
    with open(filename, 'r') as file:
        dictionary = json.load(file)
    return dictionary


def read_conversation_json(filename):
    dictionary = read_json(filename)
    return Conversation(
        title=decode_string(dictionary.get("title")),
        thread_type=dictionary.get("thread_type"),
        # participant_set={decode_string(participant_dict.get("name")) for participant_dict in dictionary.get("participants")},
        message_list=[Message(
            sender_name=decode_string(m.get("sender_name")),
            is_unsent=m.get("is_unsent"),
            content=decode_string(m.get("content")).lower() if m.get("content") is not None else None,
            photo_list=m.get("photos"),
            video_list=m.get("videos"),
            reaction_list=decode_list_of_dictionaries(m.get("reactions")) if m.get("reactions") is not None else None,
        )for m in dictionary.get("messages")],
    )


def read_conversation(dirname):
    file_list = glob.glob(f"{dirname}/*.json")
    if not file_list:
        return None     # nie znaleziono plikow json konwersacji
    first_json = file_list.pop(0)
    conversation = read_conversation_json(first_json)
    for filename in file_list:
        conversation_part = read_conversation_json(filename)
        # conversation.participant_set = conversation.participant_set | conversation_part.participant_set
        conversation.message_list += conversation_part.message_list
    return conversation


def read_conversation_list(inbox_path, without_groups=False):
    conversation_list = ConversationList()
    for dirname in glob.glob(f"{inbox_path}/**"):
        conversation = read_conversation(dirname)
        if conversation is not None:
            if without_groups and conversation.thread_type != "Regular":
                continue
            conversation_list.append(conversation)
    return conversation_list if conversation_list else None     # jesli są foldery konwersacji ale wszystkie puste


def read_file_as_str(filename):
    with open(filename, 'r') as file:
        return file.read()


def read_file_as_str_list(filename):
    with open(filename, 'r') as file:
        return file.readlines()


def get_group_conversation_name_path_dict(inbox_path):
    name_path_dict = dict()
    dir_list = glob.glob(f"{inbox_path}/**")
    for dirname in dir_list:
        file_list = glob.glob(f"{dirname}/*.json")
        for file_path in file_list:
            dictionary = read_json(file_path)
            if dictionary.get("thread_type") == "RegularGroup":
                name_path_dict[decode_string(dictionary.get("title"))] = dirname
                break
    return name_path_dict


def get_conversation_dir_name_dict(inbox_path):
    name_path_dict = dict()
    for dirname in glob.glob(f"{inbox_path}/**"):
        for file in glob.glob(f"{dirname}/*.json"):
            name_path_dict[decode_string(read_json(file).get("title"))] = dirname
            break
    return name_path_dict


from time import perf_counter
if __name__ == '__main__':
    path = r"C:\Users\Paweł\Documents\_studia\development\aplikacje\AnalFB\inbox"
    n_times = 10

    start = perf_counter()
    for _ in range(n_times):
        res = get_conversation_dir_name_dict(path)
    stop = perf_counter()
    time = stop - start

    print(res)
    print("time:", time/n_times)


