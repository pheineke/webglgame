class Player:
    global WORLD_SIZE
    
    def __init__(self, sid):
        self.sid = sid
        self.name = "Player"
        self.color = "#000000"

        self.position = {
            "x": 0,
            "y": 0,
            "z": 0
        }

        self.player_surroundings = {
            "name": "surroundings",
            "world_matrix": []
        }

        self.velocityVector = {
            "x": 0,
            "y": 0,
            "z": 0
        }
        self.velocity = 0.5
        self.inventory = []

    def get_name(self) -> str:
        return self.name
    
    def get_color(self) -> str:
        return self.color

    def get_position(self) -> dict:
        return self.position
    
    def get_surroundings(self) -> dict:
        return self.player_surroundings
    
    def get_velocity(self) -> int:
        return self.velocity
    
    def get_velocityVector(self) -> dict:
        return self.velocityVector
    
    def get_inventory(self) -> list:
        return self.inventory
    
    def set_name(self, name: str):
        self.name = name

    def set_color(self, color: str):
        self.color = color
    
    def set_position(self, x: int = None, y: int = None, z: int = None):
        if (x):
            self.position["x"] = x

        if (y):
            self.position["y"] = y

        if (z):
            self.position["z"] = z

    def set_surroundings(self, surroundings: dict):
        self.player_surroundings = surroundings

    def set_velocity(self, velocity: int):
        self.velocity = velocity

    def set_inventory(self, inventory: list):
        self.inventory = inventory

    def to_json(self) -> dict:
        player : dict = {
            "id": self.sid,
            "name": self.name,
            "color": self.color,
            "position": {
                "x": self.position["x"],
                "y": self.position["y"],
                "z": self.position["z"],
            },
            "velocityVector": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "velocity": self.velocity,
            "inventory": []
        }

        return player