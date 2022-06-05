import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class FirebaseClient:

    def __initialize_authentication(self):
        databaseURL = self.databaseUrl
        cred = credentials.Certificate(self.credentialPath)
        firebase_admin.initialize_app(cred, {'databaseURL':databaseURL})

    def __init__(self, databaseUrl: str, credentialPath: str,):
        self.databaseUrl = databaseUrl
        self.credentialPath = credentialPath

        self.__initialize_authentication()

    def set_data_table(self, table_name: str):
        return db.reference(table_name)