from flask import *
from flask_socketio import *
import requests
import random

from world import World

app = Flask(__name__)
app.secret_key = '1234'
socketio = SocketIO(app)


### FLASK-SOCKETIO

WORLD = World()


@socketio.on('connect')
def connect():
    

    sid = request.sid

    WORLD.add_player(sid=sid)

    emit('adamah', WORLD.get_world())
    emit('adameva', WORLD.get_player(sid))

    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    WORLD.remove_player(request.sid)
    print('Client disconnected')

@socketio.on('move')
def move(data):
    sid = request.sid
    WORLD.move_player(sid, data['direction'])

    emit('player_update', WORLD.get_player(sid))
    emit('other_player_update', WORLD.get_players(), broadcast=True)

### FLASK

@app.route('/', methods=['GET', 'POST'])
def game():
    return render_template('game.html')


if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
        TEMPLATES_AUTO_RELOAD=True
    )
    app.run(host='0.0.0.0', port=8000, debug=True)