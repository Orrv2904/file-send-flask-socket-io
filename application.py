import os
from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit
from dotenv import load_dotenv
from base64 import b64decode
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'
socketio = SocketIO(app)

ruta_absoluta = '/ruta/absoluta/al/directorio/static/images'
if not os.path.exists(ruta_absoluta):
    print(f"El directorio {ruta_absoluta} no existe.")

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


@socketio.on('image')
def handle_image(data):
    username = data['username']
    room = data['room']
    image_data = data['image']
    image_binary = b64decode(image_data.split(',')[1])
    try:
        with open('static/images/{room}_{username}_image.png', 'wb') as image_file:
            image_file.write(image_binary)

        emit('image', {'username': username, 'image': image_data}, room=room, broadcast=True)
    except Exception as e:
        print(f"Error al guardar la imagen: {str(e)}")


@socketio.on('file')
def handle_file(data):
    username = data['username']
    room = data['room']
    file_data = data['fileData']
    file_name = data['fileName']
    with open(f'static/files/{room}_{username}_{file_name}', 'wb') as file:
        file.write(file_data)

    emit('file', {'username': username, 'fileName': file_name}, room=room, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)