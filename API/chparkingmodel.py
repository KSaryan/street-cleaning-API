from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, timedelta, date
# import pytz
# import bcrypt
# from server import app

db = SQLAlchemy()



class Cleaning(db.Model):
    """Individual cleanings"""

    __tablename__ = "cleanings"

    cleaning_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    month_id = db.Column(db.Integer,  db.ForeignKey('months.month_id'))
    date = db.Column(db.Integer, nullable=False)
    ward = db.Column(db.Integer, nullable=False)

    months = db.relationship('Month', backref='cleanings')
    def __repr__ (self):
        """Displayed when called"""

        return "<loc-id: %s, starts: %s, ends:%s>"%(self.loc_id,
                                                    self.start_time,
                                                    self.end_time)


class Month(db.Model):
    """Days of week"""

    __tablename__ = "months"

    month_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    month_name = db.Column(db.String(9), nullable=False)

    def __repr__ (self):
        """Displayed when called"""

        return "<%s>"%(self.day_name)



def connect_to_db(app, db_uri = "postgres:///chicagoparking"):
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