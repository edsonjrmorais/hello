# import re
# import json
# from flask import Flask, request, jsonify
# from models.user import User
# from endpoints.hello import Hello
# from clients.firebase import FirebaseClient

# databaseURL = "https://hellopyapi-default-rtdb.firebaseio.com/"
# credentialPath = "./App/hellopyapi-firebase-adminsdk-h5up0-edb1d5449c.json"
# dataBaseClient = FirebaseClient(databaseURL, credentialPath)
# tableRef = dataBaseClient.set_data_table("/Users")

# client = Hello()
# #result = print(client.get("edinho",tableRef))

# data = {"username": "EdinhoOO", "dateOfBirth": "2022-06-28"}
# user = User(data)
# result = print(client.put(user,tableRef))

# pip install firebase_admin

import re
import json
from flask import Flask, request
from models.user import User
from endpoints.hello import Hello
from clients.firebase import FirebaseClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["DEBUG"] = True

databaseURL = os.getenv('DATABASE_URL')
credentialPath = os.getenv('CREDENTIAL_PATH')

dataBaseClient = FirebaseClient(databaseURL, credentialPath)

if __name__ == '__main__':

   @app.errorhandler(404)
   def page_not_found(e):
      return "<h1>404</h1><p>The resource could not be found.</p>", 404   

   @app.route('/', methods=['GET'])
   def home():
      return "Is good be at home :)"

   @app.route('/hello/<string:username>', methods=['GET'])
   def get_hello(username):

      # Home Task - 1 - Note: <username> must contain only letters
      if username.isalpha():
            
         tableRef = dataBaseClient.set_data_table("/Users")
         helloEndpoint = Hello()

         result = helloEndpoint.get(username.lower(),tableRef)

         return result,200
      
      else:
         return { "message": "Argument <username> must contain only letters" }

   @app.route('/hello', methods=['PUT'])
   def put_hello():

      user = User(json.loads(request.data))

      if re.match('([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))', user.dateOfBirth):      
         
         tableRef = dataBaseClient.set_data_table("/Users")
         helloEndpoint = Hello()

         result = helloEndpoint.put(user,tableRef)

         return result,204

      else:
         
         return { "message": "Argument <dateOfBirth”:> must be in format YYYY-MM-DD" },400

   app.run(host="0.0.0.0", port=int("8181"), debug=True)