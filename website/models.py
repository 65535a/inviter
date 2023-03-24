from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(150), unique=True)
	password = db.Column(db.String(150))
	first_name = db.Column(db.String(150))
	admin = db.Column(db.Boolean(False))

class Guest(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	invitecode = db.Column(db.String(150), unique=True)
	name = db.Column(db.String(150))
	reg_email = db.Column(db.String(150), unique=True)
	code_used = db.Column(db.Boolean(False))
