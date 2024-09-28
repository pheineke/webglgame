import threading
from queue import Queue

from flask import *
from flask_socketio import *

from server.serverlogic import ServerLogic

class ConnectionHandler:
    def __init__(self, socketio):
        self.socketio : SocketIO = socketio

        self.instruction_queue = Queue()

        self.serverlogic = ServerLogic(self.instruction_queue)
        
        self.serverlogic_thread = threading.Thread(target=self.serverlogic.run, daemon=True)

    def get_instruction_queue(self):
        return self.instruction_queue

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


    def __send_to_client(self, sid, header, data, broadcast):
        if broadcast:
            self.socketio.emit(header, data, broadcast=True)
        else:
            self.socketio.emit(header, data, to=sid)

        print(f"Sent to {sid}: {header} {data}")


    def run(self):
        self.serverlogic_thread.start()

        while True:
            if not self.instruction_queue.empty():
                instruction = self.instruction_queue.get()

                sid = instruction["sid"]
                header = instruction["header"]
                data = instruction["data"]
                broadcast = instruction["broadcast"]

                self.__send_to_client(sid, header, data, broadcast)
                