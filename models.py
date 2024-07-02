from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), unique=True, nullable=False)
    lname = db.Column(db.String(50), unique=True, nullable=False)
    profile = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hskill = db.Column(db.String(200), unique=True, nullable=False)
    sskill = db.Column(db.String(500), unique=True, nullable=False)
    experience = db.Column(db.String(500), unique=True, nullable=True)
    education = db.Column(db.String(500), unique=True, nullable=False)
    projects = db.Column(db.String(500), unique=True, nullable=False)
    certifications = db.Column(db.String(200), unique=True, nullable=False)