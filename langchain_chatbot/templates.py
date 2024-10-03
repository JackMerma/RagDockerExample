import os


def template_from_messages(query):

    messages = [
            ("system", os.getenv('INITIAL_SYSTEM_MESSAGE')),
            ("human", query)
            ]

    return messages
