import requests
import json
import time

class CommunicateAPI:
    
    ### Run Start from here ###
    start_time = time.time()
    
    def ReturningNewIds(self):
        ids =[]
        i=1
        while True:
            response = requests.get(
            "https://www.bilimtreni.com/wp-json/wp/v2/posts?page=" + str(i))
            text = json.dumps(response.json(), sort_keys=True, indent=4)
            channels = json.loads(text)
            if response.status_code == 400:
                print("Status 400")
                break
            for channel in channels:
                # print(channel)   # prints the entire channel
                #print(channel['id'])  # prints name  #prints the id's
                ids.append(channel['id'])
            
            print("---------------------------------------")
            print(i)
            i += 1
        return ids

    ### End Run Time ###
    print("Run Time --- %s seconds ---" % (time.time() - start_time))
    
