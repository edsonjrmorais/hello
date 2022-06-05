import datetime
from models.user import User
from os.path import exists as file_exists

class Hello:

    def __init__(self):

        self.date_format = "%Y-%m-%d"
        
        pass

    def calc_birthday(self, user: User):

            birth = datetime.datetime.strptime(user.dateOfBirth, self.date_format)

            today = datetime.date.today()

            # Home Task - 1 - Response Examples - A. If username’s birthday is in N days
            if(birth.date() == today):

                result = "Hello, {}! Happy birthday!".format(user.username)

                return { "message": result }

            # Home Task - 1 - Response Examples - B. If username’s birthday is today
            elif(
                today.month == birth.month
                and today.day >= birth.day
                or today.month > birth.month
            ):

                nextBirthdayYear = today.year + 1

            else:

                nextBirthdayYear = today.year

            nextBirthday = datetime.date(

                nextBirthdayYear, birth.month, birth.day

            )

            diff = nextBirthday - today

            result = "Hello, {}! Your birthday is in {} day(s)".format(user.username,diff.days)

            return { "message": result }

    def get(self, username: str, tableRef):

        table_users = tableRef.order_by_child("username").equal_to(username).get()

        if len(table_users) == 1:

            for key, value in table_users.items():

                if(value["username"].lower() == username):

                    d_users_db_table = {"username": value["username"].lower(), "dateOfBirth": value["dateOfBirth"]}

                    user = User(d_users_db_table)

                    result = self.calc_birthday(user)

                    return str(result)
        
        else:

            return {"message": "Username not found."}

    def put(self, user: User, tableRef):

        table_users = tableRef.order_by_child("username").equal_to(user.username.lower()).get()

        put_user = {"username": user.username.lower(), "dateOfBirth": user.dateOfBirth}

        # Home Task - 1 - Updates the given user’s name and date of birth in the database
        if len(table_users) == 1:

            for key, value in table_users.items():

                if(value["username"].lower() == user.username.lower()):

                    tableRef.child(key).update(put_user)

                    return {"message": "User updated."}
        
        # Home Task - 1 - Saves the given user’s name and date of birth in the database
        elif len(table_users) == 0:

            tableRef.push().set(put_user)

            return {"message": "User inserted."}