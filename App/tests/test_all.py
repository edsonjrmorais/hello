from models.user import User

class TestClass:

    def test_User(self):

        data = {"username": "Edinho", "dateOfBirth": "2022-06-28"}
        user = User(data)
        
        assert user.username == "Edinho"