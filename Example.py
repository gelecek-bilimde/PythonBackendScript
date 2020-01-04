import requests
import json
from Firebase import Firebase

db = Firebase.Configuration.db

db.child("users").push({"name": "1"})
