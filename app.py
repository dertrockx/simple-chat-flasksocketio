from flask import Flask, render_template, g, jsonify, request, session, redirect, url_for, flash
from flask_socketio import SocketIO

from flask_wtf import CSRFProtect
from forms import SignupForm, LoginForm
from models import Users as User, Messages as Message, SessionIDs as SessionID, db


import os, json
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{}/database.db'.format(BASE_DIR)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'secret_fucking_key'

csrf = CSRFProtect(app)

# Init database
db.init_app(app)

socketio = SocketIO(app)


from functools import wraps

def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		try:
			if session['logged_in']:
				redirect(url_for('chat_room'))
				return f(*args, **kwargs)
		except KeyError: # Meaning, token is not set yet...
			flash('Ooops, you\'re not logged in yet.', 'error')			
			return redirect(url_for('login'))
	return wrap


''' NOTES
	connect, disconnect, message and json are events that are not to be used
	because they are used by the socket library
'''


@app.route('/')
def sessions():
	return render_template('session.html')


'''
# A method that serves as a callback
def messsageReceived(methods=['GET', 'POST']):
	print('message was received')

			# this is a custom event
			#
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
	# the 'json' parameter is the message
	print('received my event: ' + str(json))
	socketio.emit('my response', json, callback=messsageReceived)

def signupSuccess():
	print("Signup sucessful")
'''
#@socketio.on('signup')



@app.route('/signup/', methods=['GET', 'POST'])
def signup(): 
	form = SignupForm(request.form)
	if request.method == 'POST':
		if form.validate():
			username = request.form['username']
			password = request.form['password']
			users = User.query.filter_by(username=username).all()
			if len(users):
				flash("Username is already taken, consider using a different one", "error")
				return render_template('signup.html', form=form)			
			user = User(username=username)
			user.set_password(password)
			db.session.add(user)
			db.session.commit()
			if user is not None:
				session['logged_in'] = True
				if session:
					flash("Signup successful", "success")
					return redirect(url_for('chat_room'))
			flash('Something went wrong', "error")
		flash(form.errors, "error")
	return render_template('signup.html', form=form)
	
@app.route('/login/', methods=['GET', "POST"])
def login():
	form = LoginForm(request.form)
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username).first()
		if user:
			if user.check_password(password):
				session['logged_in'] = True
				flash("Log in successful", "success")
				return redirect(url_for('chat_room'))
			flash("Passwords do not match!", "error")
			return redirect(url_for('login'))
		flash("Username not found, consider registering?", "error")
		return redirect(url_for('login'))
	return render_template('login.html')
@app.route('/chat_room/')
@is_logged_in
def chat_room():
	return render_template("chatroom.html")

@app.route('/logout/')
@is_logged_in
def logout():
	session.pop('logged_in')
	flash("Thank you for your time!", "success")
	return redirect(url_for('login'))

# SocketIO channels
@socketio.on('connect')
def on_user_connect():
	print("connected!")
	print(request.sid)

@socketio.on('disconnect')
def on_user_disconnect():
	print("Disconnect")
	print(request.sid)

@socketio.on("list_all_users")
def list_all_users():
	users = [user.username for user in User.query.all()]
	socketio.emit('return_all_users', users)

if __name__ == '__main__':
	#socketio.run(app, debug=True)
	#print(app.config['SQLALCHEMY_DATABASE_URI'])
	app.run(debug=True)
