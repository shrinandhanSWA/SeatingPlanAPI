from .person import Person

class Student(Person):
    def __init__(self, first_name, last_name, username):
        super().__init__(first_name, last_name)
        self.username = username

    def __str__(self):
        return self.username
