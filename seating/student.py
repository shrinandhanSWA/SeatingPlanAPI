class Student:
    def __init__(self, name, username, gender, nationality, group, disability=None, wild1=None, wild2=None):
        self.name = name
        self.username = username
        self.nationality = nationality
        self.gender = gender
        self.group = group
        self.disability = disability
        self.wild1 = wild1
        self.wild2 = wild2

    def __str__(self):
        return self.username

    def to_json(self):
        return self.__dict__
        
    def get_username(self):
        return self.username

    def get_wild1(self):
        return self.wild1

    def get_wild2(self):
        return self.wild2

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
        self.wild1 = wild1

    def set_wild2(self, wild2):
        self.wild1 = wild2