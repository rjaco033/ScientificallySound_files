from .person import Person


class Student(Person):

    def __init__(self, age, name, student_id):
        Person.__init__(self, age, name)
        self.student_id = student_id

    def repeat_id(self):
        print(f"My student number is {self.student_id}.")
        print(f"I repeat, my student number is {self.student_id}.")