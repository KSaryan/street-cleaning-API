from sqlalchemy import func
from chparkingmodel import (Cleaning, Month)
#remove this when import app
from flask import Flask
from chparkingmodel import connect_to_db, db
import requests
# from server import app


def create_months():
    """Creates months in months tables"""

    print("Months")

    Month.query.delete()

    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
    "october", "november", "december"]
    
    for month in months:
        mon = Month(month_name=month)
        db.session.add(mon)
        db.session.commit()




def create_cleanings():
    """creates cleanings in cleanings table"""

    print("Cleanings")

    Cleaning.query.delete()

    url = "https://data.cityofchicago.org/resource/6qug-dskz.json?$limit=100000"



    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        for item in data:
            month = item["month_name"].lower()
            m = Month.query.filter_by(month_name=month).first()
            month_id = m.month_id
            dates = item["dates"].split(",")
            for date in dates:
                c = Cleaning(month_id = month_id,
                             date = date,
                             ward = item["ward"])

                db.session.add(c)
                db.session.commit()

    # while(1):
    #     requestOK = True
    #     try:
    #        r = session.get(requestURL, headers=headers, timeout=None)
    #     except requests.exceptions.ConnectionError: 
    #        print ("'Connection aborted.', error(54, 'Connection reset by peer')")
    #        print ("\tResend request...")
    #        requestOK = False
    #     if requestOK:
    #        break

if __name__ == "__main__":
    #later can import app from server
    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()

    
    create_months()
    create_cleanings()


