class User:
    def __init__(self, json):
        self.username = json['username']
        self.dateOfBirth = json['dateOfBirth']