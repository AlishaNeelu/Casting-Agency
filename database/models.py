# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

# ---------------------------------------------------------
# App Config.
# ---------------------------------------------------------

database_path = os.environ.get('SQLALCHEMY_DATABASE_URI')
if not database_path:
    database_name = "castingagency"
    #database_path = "postgresql://postgres:password@localhost:5432/castingagency"
    database_path = "postgres://yksarikszedlzu:e73cc9f76bc8f01f1a595a1ac06e14693e3a08d53c5daae29b342de83bacbe1d@ec2-23-23-151-191.compute-1.amazonaws.com:5432/d6rtvq6gd4b9gf"

db = SQLAlchemy()
moment = Moment()

def setup_db(app, database_path=database_path):
    app.config.from_pyfile('config.py', silent=False)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    moment.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


class Actor(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Actor id='{self.id}' name='{self.name}'>"

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

class Movie(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True,  nullable=True)
    title = db.Column(db.String, nullable=False)
    release = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Movie id='{self.id}' title='{self.title}'>"

    def __init__(self, title, release):
        self.title = title
        self.release = release

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release': self.release,
        }