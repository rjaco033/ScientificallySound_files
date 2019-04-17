class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def interact(self, other_person):
        print(f"Hi {other_person}, my name is {self.name}.")