from .person import Person

class Student(Person):
    def __init__(self, first_name, last_name, username, nationality=None, predicted_grade=None):
        super().__init__(first_name, last_name)
        self.username = username
        self.nationality = nationality
        self.predicted_grade = predicted_grade

    def __str__(self):
        return self.username
