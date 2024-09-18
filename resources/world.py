import random
import requests
from PIL import Image

from resources.player import Player

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

        self.players = {}

    def add_player(self, sid):
        players: dict = self.players

        name = random.choice(['admin', 'user', 'player', 'guest', 'paul', 'john', 'jane', 'doe', 'joe', 'jim', 'bob', 'alice', 'eve', 'mallory', 'charlie', 'dave', 'rob', 'jill', 'jill', 'jack'])
        color = '#' +''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

        player = Player(sid)

        player.set_color(color)
        player.set_name(name)
        player.set_position(
            x=random.randint(0, self.WORLD_SIZE - 1),
            y=0,
            z=random.randint(0, self.WORLD_SIZE - 1)
        )
        player.set_velocity(self.MOVEMENT)
        player.set_inventory([])

        players[sid] = player

    def remove_player(self, sid):
        players: dict = self.players

        del players[sid]
    
    def get_players(self) -> dict:
        players: dict = self.players

        # convert players with __str__ and make dict with ids as keys and string as values
        players__str__ = {sid: player.to_json() for sid, player in players.items()}

        return players__str__
    
    
    def get_player(self, sid) -> Player:
        players: dict = self.players

        player = players[sid]
        return player
            
    def get_player_position(self, sid) -> dict:
        players: dict = self.players

        player = players[sid]
        return player["position"]
    
    def get_player_surroundings(self, sid) -> dict:
        players : dict = self.players

        player : Player = players[sid]

        return player.get_surroundings()
    
    def set_player_surroundings(self, sid) -> dict:
        players : dict = self.players
        player : Player = players[sid]

        radius = 5

        # Get player's position and ensure it's an integer for indexing
        x = int(player.get_position()["x"])
        z = int(player.get_position()["z"])

        # Ensure x and z remain within bounds
        x = max(radius, min(x, self.WORLD_SIZE - radius - 1))
        z = max(radius, min(z, self.WORLD_SIZE - radius - 1))

        player_surroundings_matrix = [
            [self.world_matrix[z + i][x + j] for j in range(-radius, radius + 1)] for i in range(-radius, radius + 1)
        ]

        player_surroundings = {
            "name": "surroundings",
            "world_matrix": player_surroundings_matrix
        }

        player.set_surroundings(player_surroundings)

        players[sid] = player

        # Properly return surroundings
        return player_surroundings


    def get_world(self) -> dict:
        return self.world_data
    
    def move_is_valid(self, sid, direction: dict, new_x: int, new_y: int) -> bool:
        players: dict = self.players
        player = players[sid]

        # If surroundings are None, consider the move invalid
        player_surroundings = player.get_surroundings()
        if player_surroundings is None:
            return False

        # check if player is moving out of bounds
        if new_x < 0 or new_x >= self.WORLD_SIZE or new_y < 0 or new_y >= self.WORLD_SIZE:
            return False

        # use player surroundings to check if the player is moving into a tree or rock
        if direction['z'] != 0:
            for i in range(1, 5):
                if player_surroundings["world_matrix"][i][0] == "tree" or player_surroundings["world_matrix"][i][0] == "rock":
                    return False

        if direction['x'] != 0:
            for i in range(1, 5):
                if player_surroundings["world_matrix"][0][i] == "tree" or player_surroundings["world_matrix"][0][i] == "rock":
                    return False

        return True

    
    def move_player(self, sid, direction: dict):
        players: dict = self.players
        player: Player = players[sid]

        # Ensure surroundings are set properly
        self.set_player_surroundings(sid)

        x = player.get_position()["x"]
        z = player.get_position()["z"]

        if direction['z'] != 0:
            z += direction['z'] * player.get_velocity()
        if direction['x'] != 0:
            x += direction['x'] * player.get_velocity()

        x = max(0, min(x, self.WORLD_SIZE))
        z = max(0, min(z, self.WORLD_SIZE))

        if self.move_is_valid(sid, direction, x, z):
            player.set_position(x=x, z=z)
            players[sid] = player

        # Update world matrix to reflect player position
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

            x = int(player.get_position()['x']) % self.WORLD_SIZE
            z = int(player.get_position()['z']) % self.WORLD_SIZE

            print(x, z)
            img.putpixel((x, z), (0, 0, 255))
    
        img.save('world_matrix.png')

        return 'world_matrix.png'

        