>> Starting up the application
 1. Ensure that path is in ticket-chatbot
 2. run command - "python app.py"

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

    