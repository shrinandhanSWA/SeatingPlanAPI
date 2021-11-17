class Student:
    def __init__(self, first_name, last_name, username, nationality=None, predicted_grade=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.nationality = nationality
        self.predicted_grade = predicted_grade

    def __str__(self):
        return self.username

    def to_json(self):
        return self.__dict__
        
    def get_username(self):
        return self.username

    def get_predicted_grade(self):
        return self.predicted_grade

    def get_nationality(self):
        return self.nationality

    def set_nationality(self, nationality):
        self.nationality = nationality

    def set_predicted_grade(self, grade):
        self.predicted_grade = grade