from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('joined', f'{username} ha entrado a la sala {room}', room=room)

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('left', f'{username} ha salido de la sala {room}', room=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    room = data['room']
    message = data['message']
    emit('message', {'username': username, 'message': message}, room=room, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
