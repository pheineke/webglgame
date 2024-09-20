import threading

from flask import *
from flask_socketio import *

from server.serverlogic import ServerLogic

class ConnectionHandler:
    def __init__(self, socketio):
        self.socketio = socketio

        self.serverlogic = ServerLogic()
        
        self.serverlogic = threading.Thread(target=self.serverlogic, daemon=True)

    def init(self):
        socketio = self.socketio

        @socketio.on('connect')
        def connect():
            sid = request.sid

            self.serverlogic.add_instruction({
                "type": "add_player",
                "sid": sid
            })

            print('Client connected')

        @socketio.on('disconnect')
        def disconnect():
            sid = request.sid

            self.serverlogic.add_instruction({
                "type": "remove_player",
                "sid": sid
            })

            print('Client disconnected')

        @socketio.on('move_player')
        def move(data):
            sid = request.sid

            self.serverlogic.add_instruction({
                "type": "move_player",
                "sid": sid,
                "data": data
            })



    def run(self):
        self.serverlogic.start()