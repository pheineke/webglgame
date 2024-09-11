import random
import requests

class World:
    def __init__(self):
        self.WORLD_SIZE = 100
        self.MOVEMENT = 0.5
        
        self.textures = [
            "grass",
            "sand",
            "snow",
            "rock",
            "water",
            "lava"
        ]

        self.world_data = {
            "name": "world",
            "type": "plane",
            "ground_texture": "grass",
            "world_size": {
                "x": self.WORLD_SIZE,
                "z": self.WORLD_SIZE,
            },
            "trees": self.random_trees(),
            "rocks": self.random_rocks()
        }

        self.players = {
            0: {
                "name": "admin",
                "position": {
                    "x": 0,
                    "y": 0
                },
                "inventory": []
            }
        }

    def add_player(self, sid):
        players: dict = self.players

        name = random.choice(['admin', 'user', 'player', 'guest', 'paul', 'john', 'jane', 'doe', 'joe', 'jim', 'bob', 'alice', 'eve', 'mallory', 'charlie', 'dave', 'rob', 'jill', 'jill', 'jack'])
        color = '#' +''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

        players[sid] = \
        {
            "id": sid,
            "name": name,
            "color": color,
            "position": {
                "x": random.randint(0, self.WORLD_SIZE),
                "y": 0,
                "z": random.randint(0, self.WORLD_SIZE),
            },
            "inventory": []
        }

    def remove_player(self, sid):
        players: dict = self.players

        del players[sid]
    
    def get_players(self) -> dict:
        return self.players
    
    def get_player(self, sid) -> dict:
        players: dict = self.players

        player = players[sid]
        return player
            
    def get_player_position(self, sid) -> dict:
        players: dict = self.players

        player = players[sid]
        return player["position"]
    
    def get_world(self) -> dict:
        return self.world_data
    
    def move_player(self, sid, direction: str):
        players: dict = self.players

        player = players[sid]

        x = player["position"]["x"]
        z = player["position"]["z"]

        if (direction == "forward"):
            player["position"]["z"] -= self.MOVEMENT
        elif (direction == "backward"):
            player["position"]["z"] += self.MOVEMENT
        elif (direction == "left"):
            player["position"]["x"] -= self.MOVEMENT
        elif (direction == "right"):
            player["position"]["x"] += self.MOVEMENT

        if (x > self.WORLD_SIZE):
            player["position"]["x"] = self.WORLD_SIZE
        
        if (z > self.WORLD_SIZE):
            player["position"]["z"] = self.WORLD_SIZE
        
        players[sid] = player
        

    def random_trees(self):
        trees = []

        for i in range(70):
            height = random.randint(1, 5) if random.randint(1, 10) > 2 else random.randint(6, 10)
            tree = {
                "position": {
                    "x": random.randint(0, self.WORLD_SIZE),
                    #calculate the lowest point of the tree based on the height so trees don't float
                    "y": height / 2,
                    "z": random.randint(0, self.WORLD_SIZE)
                },
                "type": random.choice(["oak", "pine", "birch", "maple"]),
                "height": height
            }
            trees.append(tree)

        return trees
        
    def random_rocks(self):
        rocks = []

        for i in range(50):
            rock = {
                "position": {
                    "x": random.randint(0, self.WORLD_SIZE),
                    "y": -1,
                    "z": random.randint(0, self.WORLD_SIZE)
                },
                "type": random.choice(["granite", "diorite", "andesite", "basalt"]),
            }
            rocks.append(rock)

        return rocks