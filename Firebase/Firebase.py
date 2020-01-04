import pyrebase
import Compare

class Configuration:
  
  config = {
    "apiKey": "*",
    "authDomain": "*-*-***.*",
    "databaseURL": "*",
    "projectId": "t*",
    "storageBucket": "*",
    "messagingSenderId": "*"
  }
  firebase = pyrebase.initialize_app(config)
  db = firebase.database()