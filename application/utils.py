# import relevant libraries
from pathlib import Path
from .db import db
from .table import Messages, ChatHistory
from sqlalchemy import select
from application import app

# chats stored in JSON file
CHAT_FILE = Path("application/data/chats.json")

# save chats to sql database
def save_chats(chats: dict):

    with app.app_context():

        # remove all messages from messages
        db.session.query(Messages).delete()

        # For each message in Json
        for chat_id in chats.keys():
            for msg in chats[chat_id]["messages"]:
                db.session.add(Messages(chat_id=chat_id, role=msg["role"], content=msg["content"]))

        #save database 
        db.session.commit()

# load chats from sql database to dict format
def load_chats():

    with app.app_context():
        chats = ChatHistory.query.all()

        chat_ids = [(row.chat_id, row.title) for row in chats]

        d1 = dict()
        # convert to dict
        for chat_id, title in chat_ids:
            messages = Messages.query.filter_by(chat_id=chat_id).all()
            l = list()
            for msg in messages:
                d2 = dict()

                d2["role"] = msg.role
                d2["content"] = msg.content

                l.append(d2)

            d1[chat_id] = {
                "title": title,
                "messages": l
            }

    return d1