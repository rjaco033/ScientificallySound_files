import random


class Room:

    def __init__(self, number, capacity):
        self.number = number
        self.capacity = capacity

    def clean(self):
        option = [True, False]
        random.shuffle(option)
        if self.capacity > 10:
            ans = option[0]
        else:
            ans = option[1]
        return ans


