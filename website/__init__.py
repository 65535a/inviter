from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import re

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'jasdhajkdshajkdhkjad'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	db.init_app(app)

	from .views import views
	from .auth import auth

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	from .models import User, Guest, Settings, Stats

	create_database(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	with app.app_context():

		invite_codes = Guest.query.count()
		setting_exist = Settings.query.count()
		stats_exist = Stats.query.count()
		print("Codes in the database: "+ str(invite_codes))
		print("Settings objects: "+ str(setting_exist))
		print("Stats objects: "+ str(stats_exist))
		settings = Settings(captcha = True)
		stats = Stats(invite_codes = 0, registered_guests = 0, checked_in = 0)
		if invite_codes <= 0:
			print("Copying invite codes to db.")
			codes = open("./codes.txt","r")
			for item in codes:
				code = Guest(invitecode=item, reg_email=None, code_used=False, checked_in=False)
				stats.invite_codes += 1
				db.session.add(code)
				db.session.commit()

		admin_email = "admin@foo.bar"
		admin_name = "admin"
		admin_pass = "changeme!"

		user = User.query.filter_by(email=admin_email).first()
	
		if user:
			return app
		else:
			new_user = User(email=admin_email, first_name=admin_name, password=generate_password_hash(admin_pass, method='sha256'), admin=True)
			db.session.add(new_user)
		
		db.session.add(settings)
		db.session.add(stats)
		db.session.commit()
	
	return app

def create_database(app):
	if not path.exists('website/' + DB_NAME):
		with app.app_context():
			db.create_all()
		print('Database created!')

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
    #return match is not None

def is_valid_string(inputString):
    pattern = r'^[a-zA-Z0-9öä]'
    return re.match(pattern, inputString) is not None

'''
def is_valid_string(inputString):
	pattern = re.compile('[^a-zA-Z0-9 ]+')
	return pattern.search(inputString) is None
'''
	