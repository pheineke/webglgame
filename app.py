import threading
from flask import *
from flask_socketio import *
import requests
import random

from server.connectionhandler import ConnectionHandler

app = Flask(__name__)
app.secret_key = '1234'
socketio = SocketIO(app)

PORT = 5000

### FLASK

@app.route('/', methods=['GET', 'POST'])
def game():
    return render_template('game.html')

if __name__ == '__main__':
    connectionhandler = ConnectionHandler(socketio)

    connectionhandler_thread = threading.Thread(target=connectionhandler.init, daemon=True)
    connectionhandler_thread.start()
    
    app.config.update(
        DEBUG=True,
        TEMPLATES_AUTO_RELOAD=True
    )
    
    app.run(host='0.0.0.0', port=PORT, debug=True)