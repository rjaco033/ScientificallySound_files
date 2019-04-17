from .room import Room


class Office(Room):

    def __init__(self,  number, capacity, person):
        Room.__init__(self, number, capacity)
        self.person = person

    def notice(self):
        print(f"This is office {self.number}, it belongs to {self.person}.")
