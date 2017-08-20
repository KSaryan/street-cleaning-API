from sqlalchemy import func
from sdparkingmodel import Location, Cleaning, Day, Street, Side
#remove this when import app
from flask import Flask
from sdparkingmodel import connect_to_db, db
import requests
import csv
# from server import app


def create_days():
    """Creates days in days tables"""

    print "Days"

    Day.query.delete()

    mon = Day(day_id="Mon", day_name="Monday")
    tue = Day(day_id="Tue", day_name="Tuesday")
    wed = Day(day_id="Wed", day_name="Wednesday")
    thu = Day(day_id="Thu", day_name="Thursday")
    fri = Day(day_id="Fri", day_name="Friday")
    sat = Day(day_id="Sat", day_name="Saturday")
    sun = Day(day_id="Sun", day_name="Sunday")
    hol = Day(day_id="Hol", day_name="Holiday")

    db.session.add_all([mon, tue, wed, thu, fri, sat, sun, hol])
    db.session.commit()



def create_cleanings():
    """Loads locations and cleanings from routes_all_datasd.csv"""

    with file('routes_all_datasd.csv', 'rb') as f:
    reader = csv.reader(f)
    cleanings_list = list(reader)
    
    Location.query.delete()

    
    print "Locations"

    for item in cleanings_list:
        #add street to streets table
        s = Street.query.filter_by(street_name=item[1]).first()
        if s is None:
            s = Street(street_name=item[1])
            db.session.add(s)
            db.session.commit()

        final_string = item[4]
        #add side to sides table
        sides = ["SS", "NS", "WS", "ES", "Both Sides"]
        for side in sides:
            if side in final_string:
                sd = Side.query.filter_by(side_name=item["blockside"]).first()  
                if sd is None:
                    sd = Side(side_name=item["blockside"])
                    db.session.add(side)
                    db.session.commit()
                side_id = sd.side_id

                to_from = item[2].split(" - ")
                from_address = to_from[0]
                to_address = to_from[1]
                

                #add location to locations table
                location=db.session.query(Location).filter(Location.street_id==s.street_id, Location.from_address==from_address,
                                        Location.to_address==to_address, Location.side_id==side_id).first()
                if location is None:
                    location = Location(street_id=s.street_id, from_address=from_address,
                                        to_address=to_address, side_id=side_id)
                    db.session.add(location)
                    db.session.commit()
                    

                days = find_days(final_string)

                if item["week1ofmon"] == "Y":
                    cleaning1 = Cleaning(day_id = day_id, start_time=item["fromhour"], end_time=item["tohour"], week_of_mon = 1, locations=location)
                    db.session.add(cleaning1)
                if item["week2ofmon"] == "Y":
                    cleaning2 = Cleaning(day_id = day_id, start_time=item["fromhour"], end_time=item["tohour"], week_of_mon = 2, locations=location)
                    db.session.add(cleaning2)
                if item["week3ofmon"] == "Y":
                    cleaning3 = Cleaning(day_id=day_id, start_time=item["fromhour"], end_time=item["tohour"], week_of_mon = 3, locations=location)
                    db.session.add(cleaning3)
                if item["week4ofmon"] == "Y":
                    cleaning4 = Cleaning(day_id=day_id, start_time=item["fromhour"], end_time=item["tohour"], week_of_mon = 4, locations=location)
                    db.session.add(cleaning4)
                if item["week5ofmon"] == "Y":
                    cleaning5 = Cleaning(day_id=day_id, start_time=item["fromhour"], end_time=item["tohour"], week_of_mon = 5, locations=location)
                    db.session.add(cleaning5)

    db.session.commit()



if __name__ == "__main__":
    #later can import app from server
    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()

    
    create_days()
    create_cleanings()


