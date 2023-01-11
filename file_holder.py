from dataclasses import dataclass
# from dataclasses import field


@dataclass
class Message:
    sender_name: str
    is_unsent: bool
    content: str = None
    photo_list: list = None
    video_list: list = None
    reaction_list: list = None


@dataclass
class Conversation:
    title: str
    thread_type: str
    # participant_set: set
    message_list: list


@dataclass
class ConversationList(list[Conversation]):
    pass
    # conversation_list: list[Conversation] = field(default_factory=list)
