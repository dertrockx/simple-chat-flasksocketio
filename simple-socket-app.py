from flask import Flask, render_template
from flask_socketio import SocketIO
import os, sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'randomtext'
socketio = SocketIO(app)


''' NOTES
	connect, disconnect, message and json are events that are not to be used
	because they are used by the socket library
'''

@app.route('/')
def sessions():
	return render_template('session.html')


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



if __name__ == '__main__':
	socketio.run(app, debug=True)