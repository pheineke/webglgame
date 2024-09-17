import random
import requests
from PIL import Image

class World:
    def __init__(self):
        self.WORLD_SIZE = 200
        self.MOVEMENT = 0.5
        
        self.textures = [
            "grass",
            "sand",
            "snow",
            "rock",
            "water",
            "lava"
        ]

        self.world_matrix = [
            ["grass" for _ in range(self.WORLD_SIZE * 2)] for _ in range(self.WORLD_SIZE * 2)
        ]

        self.world_data = {
            "name": "world",
            "type": "plane",
            "ground_texture": "grass",
            "world_size": {
                "x": self.WORLD_SIZE,
                "z": self.WORLD_SIZE,
            },
            "world_matrix": self.world_matrix,
            "trees": self.random_trees(),
            "rocks": self.random_rocks()
        }

        self.players = {
            0: {
                "name": "admin",
                "position": {
                    "x": 0,
                    "y": 0,
                    "z": 0
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
                "x": random.randint(0, self.WORLD_SIZE - 1),
                "y": 0,
                "z": random.randint(0, self.WORLD_SIZE - 1),
            },
            "velocity": self.MOVEMENT,
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
    
    def move_player(self, sid, direction: dict):
        players: dict = self.players

        player = players[sid]

        x = player["position"]["x"]
        z = player["position"]["z"]

        print(x, z, direction)

        if(direction['vectorZ'] > 0):
            z += self.MOVEMENT
        elif(direction['vectorZ'] < 0):
            z -= self.MOVEMENT

        if(direction['vectorX'] > 0):
            x += self.MOVEMENT
        elif(direction['vectorX'] < 0):
            x -= self.MOVEMENT

        player["position"]["x"] = x
        player["position"]["z"] = z

        if (x < 0):
            player["position"]["x"] = 0

        if (x > self.WORLD_SIZE):
            player["position"]["x"] = self.WORLD_SIZE

        if (z < 0):
            player["position"]["z"] = 0
        
        if (z > self.WORLD_SIZE):
            player["position"]["z"] = self.WORLD_SIZE

        players[sid] = player

        print(x, z)
        self.world_matrix[int(x)][int(z)] = "player"

    def random_trees(self):
        trees = []

        

        for i in range(70):
            height = random.randint(1, 5) if random.randint(1, 10) > 2 else random.randint(6, 10)
            x = random.randint(0, self.WORLD_SIZE -1)
            z = random.randint(0, self.WORLD_SIZE -1)

            tree = {
                "position": {
                    "x": x,
                    #calculate the lowest point of the tree based on the height so trees don't float
                    "y": height / 2,
                    "z": z
                },
                "type": random.choice(["oak", "pine", "birch", "maple"]),
                "height": height
            }
            trees.append(tree)
            self.world_matrix[z][x] = "tree"

        return trees
        
    def random_rocks(self):
        rocks = []

        for i in range(50):
            x = random.randint(0, self.WORLD_SIZE -1)
            z = random.randint(0, self.WORLD_SIZE -1)

            rock = {
                "position": {
                    "x": x,
                    "y": -1,
                    "z": z
                },
                "type": random.choice(["granite", "diorite", "andesite", "basalt"]),
            }
            rocks.append(rock)
            self.world_matrix[z][x] = "rock"

        return rocks
    
    def world_matrix_img(self):
        ## make image of world matrix png with pillow:
        img = Image.new('RGB', (self.WORLD_SIZE, self.WORLD_SIZE), color = 'white')
        ## fill tree with green, grass with white, rock with red, players with blue
        for z in range(self.WORLD_SIZE):
            for x in range(self.WORLD_SIZE):
                if self.world_matrix[z][x] == "tree":
                    img.putpixel((x, z), (0, 255, 0))
                elif self.world_matrix[z][x] == "rock":
                    img.putpixel((x, z), (255, 0, 0))
                elif self.world_matrix[z][x] == "grass":
                    img.putpixel((x, z), (255, 255, 255))
                else:
                    img.putpixel((x, z), (0, 0, 255))

        #player
        for player in self.players.values():
            print(player)
            x = int(player['position']['x']) % self.WORLD_SIZE
            z = int(player['position']['z']) % self.WORLD_SIZE

            print(x, z)
            img.putpixel((x, z), (0, 0, 255))
    
        img.save('world_matrix.png')

        return 'world_matrix.png'

        