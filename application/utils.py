# import relevant libraries
import json
from pathlib import Path
from .db import db
from .table import Messages, ChatHistory
from sqlalchemy import select
from application import app

# chats stored in JSON file
CHAT_FILE = Path("application/data/chats.json")

# save chats to chats.json
# def save_chats(chats: dict):
#     CHAT_FILE.parent.mkdir(parents=True, exist_ok=True)
#     with open(CHAT_FILE, "w", encoding="utf-8") as f:
#         json.dump(chats, f, indent=2, ensure_ascii=False)


# save chats to chats.json
def save_chats(chats: dict):

    with app.app_context():

        # remove all messages from messages
        db.session.query(Messages).delete()
        
        # db.session.add(ChatHistory(chat_id="0291c9dd-acfa-497f-89c9-24e6a9821382", title= "Chat 1"))

        # For each message in Json
        for chat_id in chats.keys():
            for msg in chats[chat_id]["messages"]:
                db.session.add(Messages(chat_id=chat_id, role=msg["role"], content=msg["content"]))

        #save database 
        db.session.commit()

# load chats to chats.json
def load_chats():

    # convert SQL to json

    # if CHAT_FILE.exists() and CHAT_FILE.stat().st_size > 0:
    #     with open(CHAT_FILE, "r", encoding="utf-8") as f:
    #         try:
    #             return json.load(f)
    #         except json.JSONDecodeError:
    #             return {}
    # return {}

    # retrieve all data from message table
    # chats =  db.session.execute(select(Messages)).scalars().all()
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