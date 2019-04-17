from .person import Person


class Scientist(Person):

    def __init__(self, name, age, discipline):
        Person.__init__(self, name, age)
        self.discipline = discipline

    def value_self(self):
        print(f"The smartest scientists study {self.discipline}")
