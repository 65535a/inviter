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

	from .models import User, Registrant

	create_database(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	with app.app_context():

		db_check = Registrant.query.count()
		print("Codes in the database: "+ str(db_check))
		if db_check <= 0:
			print("Copying invite codes to db.")
			codes = open("./codes.txt","r")
			for item in codes:
				code = Registrant(invitecode=item, reg_email=None, used=False)
				db.session.add(code)
				db.session.commit()

		admin_email = "admin@foo.bar"
		admin_name = "admin"
		admin_pass = "changeme!"

		user = User.query.filter_by(email=admin_email).first()
	
		if user:
			return app
		else:
			new_user = User(email=admin_email, first_name=admin_name, password=generate_password_hash(admin_pass, method='sha256'))
			db.session.add(new_user)
			db.session.commit()

	return app

def create_database(app):
	if not path.exists('website/' + DB_NAME):
		with app.app_context():
			db.create_all()
		print('Database created!')

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    match = re.match(pattern, email)
    return match is not None

def is_valid_string(s):
	for c in s:
		if not c.isalnum():
			return False
	return True