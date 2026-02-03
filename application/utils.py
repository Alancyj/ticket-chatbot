# import relevant libraries
import json
from pathlib import Path

# chats stored in JSON file
CHAT_FILE = Path("application/data/chats.json")

# save chats to chats.json
def save_chats(chats: dict):
    CHAT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(chats, f, indent=2, ensure_ascii=False)

# load chats to chats.json
def load_chats():
    if CHAT_FILE.exists() and CHAT_FILE.stat().st_size > 0:
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}