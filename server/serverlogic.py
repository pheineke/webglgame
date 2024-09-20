import time

from resources.world import World
from resources.player import Player

class ServerLogic:
    def __init__(self):
        self.world = World()

        self.players: dict[Player] = {}

        self.instructionqueue = []

    def add_instruction(self, instruction):
        self.instructionqueue.append(instruction)
        

    def __add_player(self, sid):
        self.players[sid] = self.world.add_player(sid)

    def __remove_player(self, sid):
        self.world.remove_player(self.players[sid])
        del self.players[sid]

    def __move_player(self, sid, data):
        self.world.move_player(sid=sid, direction=data)


    
    def run(self):
        while True:
            if len(self.instructionqueue) > 0:
                instruction : dict = self.instructionqueue.pop(0)

                match instruction["type"]:

                    case "add_player":
                        self.__add_player(instruction["sid"])
                    
                    case "remove_player":
                        self.__remove_player(instruction["sid"])
                    
                    case "move_player":
                        self.__move_player(instruction["sid"], instruction["data"])
            
            # Server Tick Rate
            tick = 0.1
            time.sleep(tick)