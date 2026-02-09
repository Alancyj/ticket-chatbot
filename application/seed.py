import pandas as pd
from datetime import datetime
from application.db import db
from application.table import Tickets

DATE_FMT = "%m/%d/%y %I:%M %p"

def seed_tickets_if_empty():

    # stops immediately if table already has data
    if db.session.query(Tickets).first():
        return

    df = pd.read_csv("models/data/ntfh_golive_incidents_mockup_v1_original.csv")

    tickets = []

    for _, row in df.iterrows():
        tickets.append(
            Tickets(
                incident_number=row["Incident Number"],
                incident_title=row["Incident Title"],
                incident_description=row["Incident Description"],
                incident_resolution=row.get("Incident Resolution"),
                resolution_team=row.get("Resolution Team"),
                status=row["Status"],
                status_update_date=parse_date(row["Status Update Date"]),
                reported_by=row["Reported By"],
                institution=row["Institution"],
                institution_name=row["Institution Name"],
                reported_date=parse_date(row["Reported Date"]),
                location=row["Location"],
                affected_person_department=row["Affected Person Department"],
                resolution_code=row.get("Resolution Code"),
                source=row["Source"],
                priority=int(row["Application Priority"]),
                close_date=parse_date(row.get("Close Date"))
            )
        )

    db.session.bulk_save_objects(tickets)
    db.session.commit()


def parse_date(value):
    if pd.isna(value) or value == "":
        return None
    return datetime.strptime(value, DATE_FMT)