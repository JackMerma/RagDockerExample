import os


def get_messages(history, query):

    # Base message
    messages = [
            ("system", os.getenv('INITIAL_SYSTEM_MESSAGE')),
            ]

    # History
    for message in history:
        messages.append(tuple(message))

    # Adding query
    messages.append(("human", query))

    return messages
