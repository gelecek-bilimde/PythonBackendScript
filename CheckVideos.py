import pyrebase
import requests
import json

config = {

}

####FETCH FROM FIREBASE
firebase = pyrebase.initialize_app(config)
db = firebase.database()
firebaseResult = db.child("/Videos").get()

##### INSERT FIREBASE ARTICLE'S IDS
firebaseIds = []
for videoId in firebaseResult.val():
    firebaseIds.append(int(videoId))

###### FETCH FROM WORDPRESS AND IDS
videos = {}
youtubeIds = []
nextPageToken = ""
while True:
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UC03cpKIZShIWoSBhfVE5bog&maxResults=50&order=date&key=AIzaSyBIIj6VEdAbHGxJdfOGz2viRdmusZwsZUI&pageToken" + str(
            nextPageToken))
    text = json.dumps(response.json(), sort_keys=True, indent=4)
    channels = json.loads(text)
    if response.status_code == 400 | response.status_code == 403:
        print("Status 400")
        break
    nextPageToken = channels['nextPageToken']

    for channel in channels:
        videos[channel['id'].get('videoId')] = channel
        youtubeIds.append(channel['id'].get('videoId'))

# FIND DIFFERENCES
for firebaseId in firebaseIds[:]:
    for youtubeId in youtubeIds:
        if int(firebaseId) == int(youtubeId):
            firebaseIds.remove(firebaseId)
            youtubeIds.remove(youtubeId)

#### REMOVE
for silinecek in firebaseIds:
    res = db.child("/Videos").child(silinecek).remove()
    print(res)


class MyVideo(object):
    def __init__(self, videoID, videoTitle, videoDesc, videoDate, videoImageURL):
        self.videoID = videoID
        self.videoTitle = videoTitle
        self.videoDesc = videoDesc
        self.videoDate = videoDate
        self.videoImageURL = videoImageURL


for eklenecekId in youtubeIds:
    ekle = videos[eklenecekId]

    new = MyVideo(ekle['id'].get('videoId'), ekle['snippet']['title'], ekle['snippet']['description'],
                  ekle['snippet']['publishedAt'], ekle['snippet']['thumbnails']['high']['url'])
    s = json.dumps(new.__dict__)
    s = json.loads(s)

    # realFuckingArticle = {article['id']: s, }
    db.child("Videos").child(ekle['id']).set(s)

print(type(videos))
print(videos)

print(firebaseIds)  # silinecek
print(youtubeIds)  # eklenecek
