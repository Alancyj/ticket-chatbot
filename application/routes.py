# import relevant libraries
from flask import render_template, request, jsonify, redirect, url_for
from application import app
from groq import GroqError
from models.chatbot import ticket_chatbot_agent
from models.tools import check_system_status
from application.utils import load_chats, save_chats
import uuid
import random
from datetime import datetime, timezone, timedelta
from application.email_mod import email_class
import pandas as pd
from flask import request

from .db import db
from .table import ChatHistory, Tickets

print("Finish imports for routes.py")

# initialising variables
chats = load_chats()
current_chat_id = None
part_of_day = lambda hour : "Morning" if hour < 12  else "Afternoon" if hour < 18 else "Evening" if hour <= 24 else "Morning"
right_arrow_img = '<img src="../static/images/right arrow.png" alt="btn" style="width: 1em; margin: auto;">'

messageStartUp = f"Good {part_of_day(datetime.now().hour)}!\n\nWelcome to the Go-Live Public Billing System support chatbot. Below are some prompts to start the conversation.\n\n<span class='link-in-message'>1. Report an issue with PBS {right_arrow_img}</span>\n<span class='link-in-message'>2. Request authorisation in PBS {right_arrow_img}</span>\n<span class='link-in-message'>3. Track a ticket number {right_arrow_img}</span>\n<span class='link-in-message'>4. List commonly recurring issues {right_arrow_img}</span>\n\nIf you want to speak to an agent, please dial our hotline 1234 5678. Alternatively, you can email us at example@email.com"

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

        return "Chatbot has encountered an error.\n\n" + str(e)

# startup page
@app.route("/")
def index():
    global current_chat_id

    if chats == {}: # start a new chat if none exists
    # if current_chat_id is None or current_chat_id not in chats: # start a new chat if none exists
        current_chat_id = generate_chat_id()

        db.session.add(ChatHistory(chat_id=current_chat_id, title = 'Chat 1'))
        db.session.commit()

        chats[current_chat_id] = {"title": 'Chat 1', 
                                  "messages": [{"role": "ai", "content": messageStartUp}]}
        
        save_chats(chats)
    
    else:
        # take the first chat in chat json
        current_chat_id = list(chats.keys())[0]

    return render_template("chat.html", messages=chats[current_chat_id]["messages"], chats=chats, current_chat_id=current_chat_id)

# faq page
@app.route("/faq")
def faq():
    current_chat_id = None
    return render_template("faq.html", chats=chats, current_chat_id=current_chat_id)


# show system performance in top right popup
@app.route("/system_status")
def system_status():
    status_str = check_system_status()
    status_text = status_str.split(". Last updated")[0]
    
    # determine emoji based on status
    emoji = "🟢" if status_text.lower() == "normal" else "🟡" if "slowness" in status_text.lower() else "🔴"
    
    return jsonify({"status": f"{status_text} {emoji}"})

# get specific chat from chat ID
@app.route("/chat/<chat_id>")
def chat(chat_id):
    global current_chat_id

    # Clear AI memory
    ticket_chatbot_agent.memory.clear()

    if chat_id not in chats:
        return redirect(url_for("index"))

    current_chat_id = chat_id
    return render_template("chat.html", messages=chats[chat_id]["messages"], chats=chats, current_chat_id=current_chat_id)

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
    
    # For issue reporting template
    if "Fill Issue Reporting Form" in ai_response:
        ai_response = 'Reporting Form has timed out.'

        chat["messages"].append({"role": "ai", "content": ai_response})
        
        save_chats(chats)

        file_path = 'application/templates/reporting_form.html'

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                ai_response =  str(file.read())
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")

    elif "Fill Authorisation Form" in ai_response:
        ai_response = 'Authorisation Form has timed out.'

        chat["messages"].append({"role": "ai", "content": ai_response})

        save_chats(chats)

        file_path = 'application/templates/authorisation_form.html'

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                ai_response =  str(file.read())
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
    else:
        chat["messages"].append({"role": "ai", "content": ai_response})
        save_chats(chats)

    return jsonify({"reply": ai_response, "chat_id": current_chat_id, "chat_title": chat["title"]})

# new chat !!!
@app.route("/new_chat", methods=["POST"])
def new_chat():
    global current_chat_id

    chatTitle = [chat["title"] for chat in list(chats.values())]
    chatTitleNumber = [int(title.split(' ')[1]) for title in chatTitle]
    newTitle = 'Chat ' + str(max(chatTitleNumber) + 1)

    new_id = generate_chat_id()

    db.session.add(ChatHistory(chat_id=new_id, title = newTitle))
    db.session.commit()

    chats[new_id] = {"title": newTitle,
                     "messages": [{"role": "ai", "content": messageStartUp}]}
    
    current_chat_id = new_id
    save_chats(chats)
    
    return jsonify({"chat_id": new_id})

# refresh chat from sidebar
@app.route("/reset_chat/<chat_id>", methods=["POST"])
def reset_chat(chat_id):
    if chat_id not in chats:
        return jsonify({"error": "Chat not found"}), 404

    # keep title, reset messages
    chats[chat_id]["messages"] = [
        {"role": "ai", "content": messageStartUp}
    ]

    save_chats(chats)
    return jsonify({"chat_id": chat_id})


# remove chat from list
@app.route("/delete_chat/<chat_id>", methods=["DELETE"])
def delete_chat(chat_id):
    global current_chat_id

    print(1)
    with app.app_context():
        print(2)
        db.session.query(ChatHistory).filter_by(chat_id=chat_id).delete()
        db.session.commit()
        print(3)

    # delete chat key from chats
    if chat_id in chats: del chats[chat_id]
    save_chats(chats)

    # if user current chat is the one being deleted -> redirect user to first chat_id
    if len(list(chats.keys())) < 1:
        return jsonify({"chat_id": None}) 
    elif current_chat_id == chat_id:
        return jsonify({"chat_id": list(chats.keys())[0]}) 

    # if user current chat is not the one being deleted -> stay in chat
    return jsonify({"chat_id": current_chat_id})

# submit issue reporting form
@app.route("/submit_reporting_form", methods=["POST"])
def submit_report_form():
    global current_chat_id
    
    # define dataset file path
    fpath = "models/data/ntfh_golive_incidents_mockup_v1.csv" # -- get file path
    table = pd.read_csv(fpath) # -- read file
    
    # logic to generate ticket number after form has been submitted
    generated_ticket_number = 'IN'

    for _ in range(7):
        generated_ticket_number += str(random.randint(0, 9))

    while generated_ticket_number in list(table['Incident Number']): # -- in the case that tix no already exists in dataset
        generated_ticket_number = 'IN'
        for _ in range(7):
            generated_ticket_number += str(random.randint(0, 9))

    generated_ticket_number_str = f"We have received your submission. You can track the ticket using ticket number <strong>{generated_ticket_number}</strong>" 

    # save to chat history
    chat = chats[current_chat_id]

    chat["messages"][-1] = {"role": "ai", "content": generated_ticket_number_str}

    save_chats(chats)

    # -- save incident to excel file -- 
    now = datetime.now()
    formatted_date = now.strftime("%m/%d/%y %I:%M %p") # current datetime

    # create row and match value to column
    new_row = {
        'Incident Number': generated_ticket_number, 
        'Incident Title': request.form['title'],
        'Incident Description': request.form['description'],
        'Status': "INPROGRESS",
        'Status Update Date': formatted_date,
        'Reported By': request.form['userid'],
        'Institution': 'NTFH',
        'Institution Name': 'Ng Teng Fong General Hospital',
        'Reported Date': formatted_date,
        'Location': 'NTFH',
        'Affected Person Department': request.form['location'],
        'Source': 'Chatbot',
        'Application Priority': request.form['priority']
               }

    # add row in
    table = pd.concat([table, pd.DataFrame([new_row])], ignore_index=True)
    
    # save table to excel
    # save table to excel and sql
    try:
        table.to_csv(fpath, index=False)

        # ---- SAVE INCIDENT TO SQL TABLE ----
        new_ticket = Tickets(
            incident_number=generated_ticket_number,
            incident_title=request.form['title'],
            incident_description=request.form['description'],
            incident_resolution=None,
            resolution_team=None,
            status="INPROGRESS",
            reported_by=request.form['userid'],
            institution="NTFH",
            institution_name="Ng Teng Fong General Hospital",
            location="NTFH",
            affected_person_department=request.form['location'],
            resolution_code=None,  
            source="Chatbot",
            priority=int(request.form['priority']),
            close_date=None
        )

        with app.app_context(): 
            db.session.add(new_ticket)
            print("THIS CODE RAN")
            print(db.session.query(Tickets).all())
            print('before', db.session.query(Tickets.status_update_date).all())
            db.session.commit()
            print('after', db.session.query(Tickets.status_update_date).all())
                
    except Exception as e:
        db.session.rollback()
        chat["messages"][-1] = {"role": "ai", "content": "Please fill the form again, ticket was not created successfully."}
    
    return redirect(url_for('chat', chat_id = current_chat_id))

# submit auth form
@app.route("/submit_authorisation_form", methods=["POST"])
def submit_auth_form():
    global current_chat_id

    # -- content for the email --
    recipent_email = request.form['email']
    userid = request.form['userid']
    pwReset = "Yes" if 'Reset Password' in request.form else "No"
    vCharges = "\t- Verifying Charges\n" if 'Verifying Charges' in request.form else ""
    vBills = "\t- Editing Bills\n" if 'Editing Bills' in request.form else ""
    finance = "\t- Finance" if 'Finance' in request.form else ""

    # -- emailing logic here --      

    msg = f"""
Dear user,

This email is to acknowledged your authorisation request for the Public Billing System for Ng Teng Fong Hospital.

    User ID: {userid}
    Password Reset: {pwReset}
    Roles:
{vCharges} {vBills} {finance}

Regards,
PBS Authorisation Team
    """

    if len(request.form) < 3:
        msg = """
Dear user,

This email is to you that your authorisation request for the Public Billing System for Ng Teng Fong Hospital has failed as there were no request selected in the form submitted.

Regards,
PBS Authorisation Team
"""

    email = email_class(sender_email= "yeejiealan1@gmail.com", recipent_email= recipent_email, message=msg) 
    email.send_email()

    # change message after user submitted
    msg = f'Email has been sent out to {recipent_email}, please check your inbox.'

    # save to chat history
    chat = chats[current_chat_id]

    chat["messages"][-1] = {"role": "ai", "content": msg}

    # -- save incident to excel file -- 
    return redirect(url_for('chat', chat_id = current_chat_id))

