# import relevant libraries
from flask import render_template, request, jsonify, redirect, url_for
from application import app
from groq import GroqError
from models.chatbot import ticket_chatbot_agent
from application.utils import load_chats, save_chats
import uuid



# Store chats in memory (id → chat data)

# initialising variables
chats = load_chats()
current_chat_id = None
messageStartUp = "Good [Morning/Afternoon/Evening]!\n\nWelcome to the Go-Live National Billing System support chatbot. Below are some prompts to start the conversation.\n\n1. Report an issue with NBS\n2. Track a ticket number\n3. Checking system performance\n4. Top reported issues\n\nIf you want to speak to an agent, please dial our hotline [NBS deployment hotline]. Alternatively, you can email us at [NBS deployment email]"

# generating unique chat ID using UUID 
def generate_chat_id():
    return str(uuid.uuid4())

# calling model 
def call_model(query):
    try:
        result = ticket_chatbot_agent.invoke(query)

        return result["output"]
    
    except GroqError as e: # rate limit error because we are broke students
        if "rate limit" in str(e).lower():
            rate_limit_error = ("Oops, seems like the rate limit has been reached. This error is occurring as we are using the free version of Groq model in this prototype/test.")

        return rate_limit_error

# startup page
@app.route("/")
def index():
    global current_chat_id

    if current_chat_id is None or current_chat_id not in chats: # start a new chat if none exists
        current_chat_id = generate_chat_id()
        chats[current_chat_id] = {"title": None, 
                                  "messages": [{"role": "ai", "content": messageStartUp}]}
        save_chats(chats)

    return render_template("chat.html", messages=chats[current_chat_id]["messages"], chats=chats)

# get specific chat from chat ID
@app.route("/chat/<chat_id>")
def chat(chat_id):
    global current_chat_id

    if chat_id not in chats:
        return redirect(url_for("index"))

    current_chat_id = chat_id
    return render_template("chat.html", messages=chats[chat_id]["messages"], chats=chats)

# send message
@app.route("/send_message", methods=["POST"])
def send_message():
    global current_chat_id

    if current_chat_id is None or current_chat_id not in chats:
        return jsonify({"error": "No active chat"}), 400

    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    chat = chats[current_chat_id]

    # add user message
    chat["messages"].append({"role": "human", "content": user_input})

    # generate chatbot response
    ai_response = call_model(user_input)
    chat["messages"].append({"role": "ai", "content": ai_response})

    save_chats(chats)

    return jsonify({"reply": ai_response, "chat_id": current_chat_id, "chat_title": chat["title"]})

# new chat !!!
@app.route("/new_chat", methods=["POST"])
def new_chat():
    global current_chat_id

    new_id = generate_chat_id()
    chats[new_id] = {"title": None,
                     "messages": [{"role": "ai", "content": messageStartUp}]}
    current_chat_id = new_id
    save_chats(chats)
    
    return jsonify({"chat_id": new_id})