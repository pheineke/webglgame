import time

from flask import *
from flask_socketio import *

from resources.world import World
from resources.player import Player

class ServerLogic:
    def __init__(self, connectionhandler_instructionqueue):
        self.world = World()

        self.players: dict[Player] = {}

        self.instructionqueue = []
        self.connectionhandler_instructionqueue = connectionhandler_instructionqueue

    def add_instruction(self, instruction):
        self.instructionqueue.append(instruction)
        

    def __add_player(self, sid):
        self.players[sid] = self.world.add_player(sid)

    def __remove_player(self, sid):
        self.world.remove_player(self.players[sid])
        del self.players[sid]

    def __move_player(self, sid, data):
        self.world.move_player(sid=sid, direction=data)


    def __send_to_client(self, sid, header, data, broadcast=False):
        self.connectionhandler_instructionqueue.append({
            "sid": sid,
            "header": header,
            "data": data
        }, broadcast)
    
    def run(self):
        while True:
            if len(self.instructionqueue) > 0:
                instruction : dict = self.instructionqueue.pop(0)

                print(f"Got instruction: {instruction}")

                match instruction["type"]:

                    case "add_player":
                        self.__add_player(instruction["sid"])

                        print("Added player")

                        self.__send_to_client(instruction["sid"], "init_world", {"world": self.world.get_world()})

                        print("Sent init_world")
                        
                    
                    case "remove_player":
                        self.__remove_player(instruction["sid"])
                    
                    case "move_player":
                        self.__move_player(instruction["sid"], instruction["data"])
            
            # Server Tick Rate
            tick = 0.1
            time.sleep(tick)