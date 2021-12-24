class Student:
    def __init__(self, name, username, gender, nationality, group,
                 disability=False, wild=False, real=True):
        self.name = name
        self.username = username
        self.gender = gender
        self.nationality = nationality
        self.gender = gender
        self.group = group
        self.disability = disability
        self.wild = wild
        self.real = real

    def to_json(self):
        return self.__dict__

    def get_wild(self):
        return self.wild

    def is_wildcard(self):
        return self.wild

    def get_username(self):
        return self.username

    def get_name(self):
        return self.name

    def get_nationality(self):
        return self.nationality

    def get_disability(self):
        return self.disability

    def get_group(self):
        return self.group

    def get_gender(self):
        return self.gender

    def set_disability(self, disability):
        self.disability = disability

    def set_wild(self, wild):
        self.wild = wild

    def is_male(self):
        return self.gender == 'Male'

    def get_real(self):
        return self.real

    def __lt__(self, student):
        return self.username < student.username

    def __repr__(self):
        return self.username + "*" if self.wild else ""

    def __str__(self):
        return self.__repr__()


def dummy_student():
    return Student("fh5", "fh5", "fh5", "fh5", "fh5", real=False)
