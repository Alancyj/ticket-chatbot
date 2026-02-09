-> Starting up the application <br>
 1. Ensure that path is in ticket-chatbot
 2. Ensure in you .env file, you have keys for
   GROQ_API_KEY
   HF_TOKEN
   GOOGLE_PASSWORD
   DATABASE_URL=postgresql://ticket_chatbot_user:YMZaWz7IXHZm9Y0xYj1SEBmyrobBxgzn@dpg-d640g6er433s73e16150-a.singapore-postgres.render.com/ticket_chatbot
 3. run command - "python app.py"

-> Starting using Docker <br>
"docker run  --env-file .env -p 8080:8000 -e PORT=8000 alanyj/ticketchatbot"

-> Github link <br>
https://github.com/Alancyj/ticket-chatbot

-> Demo video link <br>
https://youtu.be/bshyGKUsccY



-> Tree file directory <br>

ticket-chatbot/                        
├─ application/                           
│  ├─ static/
│  │  ├─ css/
│  │  │  ├─ form.css                       # Handle styling for forms
│  │  │  └─ main.css                       # Handle styling for all
│  │  ├─ images/
│  │  │  ├─ bill-logo.png
│  │  │  ├─ pbs-logo.png                 
│  │  │  └─ right arrow.png                  
│  │  └─ js/
│  │     └─ script.js
│  ├─ templates/
│  │  ├─ authorisation_form.html           # Authorisation form
│  │  ├─ chat.html                         # Chat layout for main page
│  │  ├─ faq.html                          # FAQ page
│  │  ├─ layout.html                       # Layout for main page
│  │  └─ reporting_form.html               # Reporting form
│  ├─ __init__.py
│  ├─ db.py                                # Initialise database
│  ├─ email_mod.py                         # Handles emailing logic for 3rd function
│  ├─ routes.py                            # Specify routes for website
│  ├─ seed.py                              # Populate tickets in database
│  ├─ table.py                             # Stores table format
│  └─ utils.py                             # Handles saving and retrieving chats from db
├─ chroma_data/
│  └─ chroma.sqlite3                       # Stores vector data for retrieving similar incidents
├─ models/
│  ├─ __init__.py
│  ├─ chatbot.py                           # Create chatbot agent
│  ├─ create_retriever.py                  # Converts excel file to vector storage
│  ├─ groq_llm.py                          # Initialise model
│  └─ tools.py                             # Handle chatbot agent's tools
├─ .dockerignore
├─ .env                                    # Store secret keys
├─ .gitignore
├─ app.py                                  # Main file
├─ docker-compose.yml                     
├─ DockerFile                              # Commands to start Docker 
├─ README.md                               # Contain simple documentation for project
├─ requirements.txt                        # Project's main dependencies

>> The data used for chatbot 
Two types of data are used for the chatbot:
 1. 
    [Description] 
    List of incidents that has been reported for the Public Billing System in Excel format
    
    [Columns] 
    Incident Number, Prefix, Incident Title, Incident Description, Incident Resolution, Resolution Team, Status, Status Update Date, Reported By, Institution, Institution Name, Reported Date, Location, Affected Person Department, Resolution Code, Source, Application Priority, Close Date
    
    [Usage] 
    To search up specific incident using ticket number or top recurring incident 

 2. 
    [Description] 
    List of unique incidents in ChromaDB format
    
    [Columns]
    Unique incidents including incidents from previous instituition's golive in a vector database format

    [Usage]
    To search up similar incidents according to incident description

    