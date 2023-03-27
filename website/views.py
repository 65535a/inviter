from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, logout_user, current_user
from . import db, is_valid_email, is_valid_string
from .models import Guest, Stats, Settings

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
	
	if request.args.get('code') !=None and request.args.get('email') !=None and request.args.get('name') !=None:
		input_code = request.args.get('code')
		input_email = request.args.get('email')
		input_name = request.args.get('name')

		if is_valid_email(input_email) and is_valid_string(input_name):
			guest = Guest.query.filter_by(reg_email=input_email).first()
			if guest != None:
				flash("Email already registered", category='error')
				return render_template("register.html", user=current_user, code=input_code)
			else:	
				guest = Guest.query.filter_by(invitecode=input_code+"\n").first()
				if guest and guest.code_used == False:
					stats = Stats.query.first()
					stats.registered_guests += 1
					guest.reg_email = input_email
					guest.name = input_name
					guest.code_used = True
					db.session.commit()
					return("Guest registered!")					
				else:
					flash("Invalid or already registered code", category='error')
					return render_template("home.html", user=current_user)
						
		else:
			flash("Invalid email address or name.", category='error')
			return render_template("register.html", user=current_user, code=input_code)

	elif request.args.get('code') !=None:
		input_code = request.args.get('code').upper()
		if is_valid_string(input_code):
			guest = Guest.query.filter_by(invitecode=input_code+"\n").first()
		else:
			flash("Invalid code.", category='error')
			return render_template("home.html", user=current_user) 
		if guest:
			if guest.code_used == False:
				flash("Code correct!", category='success')
				return render_template("register.html", user=current_user, code=guest.invitecode)
			else:
				flash("Code already registered!", category='error') 
				return redirect(url_for('views.home'))
		else:
			flash("Invalid code.", category='error')
			return render_template("home.html", user=current_user)
	else:
		settings = Settings.query.first()
		if settings.captcha == True:
			# Put captcha here
			pass
		return render_template("home.html", user=current_user)


@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
	settings = Settings.query.first()
	if request.args.get('captcha') == "enable":		
		settings.captcha = True
		db.session.commit()
	else: 
		settings.captcha = False
		db.session.commit()
	return render_template("admin.html", user=current_user, settings=settings)


@views.route('/guestlist', methods=['GET'])
@login_required
def guestlist():
	rows = request.args.get('rows', 10, type=int)
	page = request.args.get('page', 1, type=int)
	 
	if request.args.get('search') != None:
		search = request.args.get('search')
		if search == "":
			guestlist = Guest.query.filter_by(code_used=True).order_by(Guest.name).paginate(page=page, per_page=rows)
		elif is_valid_string(search):		
			guestlist = Guest.query.filter_by(invitecode=search+"\n").order_by(Guest.name).paginate(page=page, per_page=rows)
			if not guestlist.items:
				search = "%{}%".format(search)
				guestlist = Guest.query.filter(Guest.name.like(search)).order_by(Guest.name).paginate(page=page, per_page=rows)
			if not guestlist.items:
				guestlist = Guest.query.filter(Guest.name.like(search)).order_by(Guest.name).paginate(page=page, per_page=rows)		
		else:
			guestlist = Guest.query.filter(Guest.name.like(search)).order_by(Guest.name).paginate(page=page, per_page=rows)
	else:
		guestlist = Guest.query.filter_by(code_used=True).order_by(Guest.name).paginate(page=page, per_page=rows)
		
	return render_template("guestlist.html", guestlist=guestlist, user=current_user)


@views.route('/checkin/<code>', methods=['GET'])
@login_required
def checkin(code):
	guest = Guest.query.filter_by(invitecode=code+"\n").first()
	stats = Stats.query.first()
	stats.checked_in += 1
	guest.checked_in = True
	db.session.commit()
	return redirect('/guestlist')

@views.route('/stats', methods=['GET'])
@login_required
def stats():
	stats = Stats.query.first()
	return render_template("stats.html", user=current_user, stats=stats)

