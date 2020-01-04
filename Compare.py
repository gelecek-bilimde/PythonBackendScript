from CommunicateAPI import CommunicateAPI
class Compare:
    def __init__(self, oldTitles, newTitles):
        self.oldArray = oldTitles
        self.newArray = newTitles
        
    def ReturnWillAdds(self):
        oldArray = [1, 8119, 8085, 8039, 8001, 7953, 7905, 7879, 7866]
        newArray = CommunicateAPI.ReturningNewIds("a")
        add = set(newArray) - set(oldArray)
        return add
    def ReturnWillDeletes(self):    
        oldArray = [1, 8119, 8085, 8039, 8001, 7953, 7905, 7879, 7866]
        newArray = CommunicateAPI.ReturningNewIds("a")
        delete = set(oldArray) - set(newArray)
        return delete

    print("Eklenecek ",ReturnWillAdds(""))
    print("Silinecek ",ReturnWillDeletes(""))

