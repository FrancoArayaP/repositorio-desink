from .models import Conversation

def get_or_create_conversation(user1, user2):
    conv = Conversation.objects.filter(participants=user1).filter(participants=user2).first()
    if not conv:
        conv = Conversation.objects.create()
        conv.participants.add(user1, user2)
    return conv