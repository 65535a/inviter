from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# User model
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	email = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(150))
	first_name = db.Column(db.String(150))
	admin = db.Column(db.Boolean(False))

# Guest model
class Guest(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	invitecode = db.Column(db.String(150), unique=True)
	name = db.Column(db.String(150))
	reg_email = db.Column(db.String(150), unique=True)
	code_used = db.Column(db.Boolean(False))
	checked_in = db.Column(db.Boolean(False))

# Settings model
class Settings(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	captcha = db.Column(db.Boolean(False))

# Statistics model
class Stats(db.Model):
	id = db.Column(db.Integer, primary_key=True, unique=True)
	invite_codes = db.Column(db.Integer)
	registered_guests = db.Column(db.Integer)
	checked_in = db.Column(db.Integer)
