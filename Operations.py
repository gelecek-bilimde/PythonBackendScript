import requests
import json
from Firebase import Firebase
from CommunicateAPI import CommunicateAPI

db = Firebase.Configuration.db

array = CommunicateAPI.ReturningNewIds("a")
willPushArray = []

def AddToNewPost():

    for x in array: 
        willPushArray.append(x)
    print(willPushArray)


    #db.child('Post').push({
    #    "id": "1",
    #    "name":"post.name"
    #}) 
AddToNewPost()