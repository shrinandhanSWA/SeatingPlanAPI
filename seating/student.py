class Student:
    def __init__(self, first_name, last_name, username, gender=None,
                 nationality=None, predicted_grade=2, disability_exception=False,
                 wildcard_accountant=False, wildcard_python=False, group_name=None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.gender = gender
        self.nationality = nationality
        self.predicted_grade = predicted_grade
        self.disability_exception = disability_exception
        self.wildcard_accountant = wildcard_accountant
        self.wildcard_python = wildcard_python
        self.group_name = group_name

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

    def is_disabled(self):
        return self.disability_exception

    def is_male(self):
        return self.gender == 'Male'

    def get_group_name(self):
        return self.group_name

    def __lt__(self, student):
        return self.username < student.username

    def __repr__(self):
        return self.gender
