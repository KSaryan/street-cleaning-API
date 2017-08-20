from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
import pytz
import bcrypt
# from server import app

db = SQLAlchemy()

class Street(db.Model):
    """Streets in SF"""

    __tablename__ = "streets"

    street_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    street_name = db.Column(db.String(20), nullable=False)

    def __repr__ (self):
        """Displayed when called"""

        return "<%s>"%(self.street_name)


class Side(db.Model):
    """Street Sides"""

    __tablename__ = "sides"

    side_id = db.Column(db.String(2), primary_key=True)
    side_name = db.Column(db.String(10), nullable=False)

    def __repr__ (self):
        """Displayed when called"""

        return "<%s>"%(self.side_name)


class Location(db.Model):
    """Specific address."""

    __tablename__ = "locations"

    loc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    street_id = db.Column(db.Integer, db.ForeignKey('streets.street_id'))
    from_address = db.Column(db.Integer, nullable=False)
    to_address = db.Column(db.Integer, nullable=False)
    side_id = db.Column(db.Integer, db.ForeignKey('sides.side_id'))
    
    sides = db.relationship('Side', backref='locations')
    streets = db.relationship('Street', backref='locations')

    def __repr__ (self):
        """Displayed when called"""

        return "<rt: %s-%s, lt: %s-%s for loc: %s>"%(self.rt_from_address,
                                                        self.rt_to_address,
                                                        self.lt_from_address,
                                                        self.lt_to_address,
                                                        self.loc_id)


class Cleaning(db.Model):
    """Individdual cleanings"""

    __tablename__ = "cleanings"

    cleaning_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    loc_id = db.Column(db.Integer, db.ForeignKey('locations.loc_id'))
    start_time = db.Column(db.String(5), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    day_id = db.Column(db.String(4), db.ForeignKey('days.day_id'))
    week_of_mon = db.Column(db.Integer, nullable=False)
    months = db.Column(db.ARRAY(db.Numeric, dimensions=1), nullable=False)

    locations = db.relationship('Location', backref='cleanings')
    days = db.relationship('Day', backref='cleanings')

    def __repr__ (self):
        """Displayed when called"""

        return "<loc-id: %s, starts: %s, ends:%s>"%(self.loc_id,
                                                    self.start_time,
                                                    self.end_time)


class Day (db.Model):
    """Days of week"""

    __tablename__ = "days"

    day_id = db.Column(db.String(4), primary_key=True)
    day_name = db.Column(db.String(9), nullable=False)

    def __repr__ (self):
        """Displayed when called"""

        return "<%s>"%(self.day_name)



def connect_to_db(app, db_uri = "postgres:///parking"):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    #can import app from server later
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."