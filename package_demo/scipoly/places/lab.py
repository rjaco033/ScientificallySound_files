from .room import Room
import random


class Lab(Room):

    def __init__(self,  number, capacity, equipment):
        Room.__init__(self, number, capacity)
        self.equipment = equipment

    def accident(self):
        broken = random.choice(self.equipment)
        print(f"Unfortunately, your graduate student just broke your {broken}.")
