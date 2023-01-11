from file_holder import Message


def decode_string(text):
    return text.encode('latin_1').decode('utf-8')


def decode_list_of_dictionaries(dict_list: list[dict]):
    decoded_dict_list = []
    for dictionary in dict_list:
        for key in dictionary:
            if isinstance(dictionary[key], str):
                dictionary[key] = dictionary[key].encode('latin_1').decode('utf-8')
            elif isinstance(dictionary[key], list):
                for inner_dict in dictionary[key]:
                    for inner_key in inner_dict:
                        if isinstance(inner_dict[inner_key], str):
                            inner_dict[inner_key] = inner_dict[inner_key].encode('latin_1').decode('utf-8')
        decoded_dict_list.append(dictionary)
    return decoded_dict_list


def decode_message_list(message_list: list[Message]):
    decoded_message_list = []
    for m in message_list:
        m.sender_name = decode_string(m.sender_name)
        if m.content is not None:
            m.content = decode_string(m.content)
        if m.reaction_list is not None:
            m.reaction_list = decode_list_of_dictionaries(m.reaction_list)
        decoded_message_list.append(m)
    return decoded_message_list


def decode_conversation(conversation):
    conversation.title = decode_string(conversation.title)
    # conversation.participant_list = decode_list_of_dictionaries(conversation.participant_list)
    # conversation.participant_set = {decode_string(p) for p in conversation.participant_set}
    # conversation.message_list = decode_list_of_dictionaries(conversation.message_list)
    conversation.message_list = decode_message_list(conversation.message_list)
    return conversation
