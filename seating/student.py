class Student:
    def __init__(self, name, username, gender, nationality, group, disability=None, wildCard1=None, wildCard2=None):
        self.name = name
        self.username = username
        self.gender = gender
        self.nationality = nationality
        self.gender = gender
        self.group = group
        self.disability = disability
        self.wildCard1 = wildCard1
        self.wildCard2 = wildCard2

    def to_json(self):
        return self.__dict__

    def get_username(self):
        return self.username

    def get_wild1(self):
        return self.wildCard1

    def get_name(self):
        return self.name

    def get_wild2(self):
        return self.wildCard2

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

    def set_wild1(self, wild1):
        self.wildCard1 = wild1

    def set_wild2(self, wild2):
        self.wildCard2 = wild2

    def is_male(self):
        return self.gender == 'Male'

    def __lt__(self, student):
        return self.username < student.username