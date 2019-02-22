from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime

db = SQLAlchemy()
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		hasher = hashlib.sha256()
		hasher.update(str(password))
		self.password = hasher.hexdigest()
		return self.password

	def check_password(self, password):
		hasher = hashlib.sha256()
		hasher.update(str(password))
		return hasher.hexdigest() == self.password

class Messages(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	message = db.Column(db.Text, nullable=False)
	'''
	user_id_from = db.Column(db.Integer, db.ForeignKey('users.id'))
	user_from = db.relationship('Users', backref=db.backref('sent_messages'), lazy=True)

	user_id_to = db.Column(db.Integer, db.ForeignKey('users.id'))
	user_to = db.relationship('Users', backref=db.backref('received_messages'), lazy=True)
	'''
	def __repr__(self):
		return '<Message {}>'.format(self.message)

class SessionIDs(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sid = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

	def __repr__(self):
		return "<User {}'s session ID: {}".format(self.user_id, self.sid)

class ActiveAccounts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	session_id = db.Column(db.String(32), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

	def __repr__(self):
		return "<Active: {}>".format(self.user_id)