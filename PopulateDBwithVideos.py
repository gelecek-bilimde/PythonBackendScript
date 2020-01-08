import pyrebase
import requests
import json

config = {

}

####FIREBASE CONFIG
firebase = pyrebase.initialize_app(config)
db = firebase.database()

videos = []


class MyVideo(object):
    def __init__(self, videoID, videoTitle, videoDesc, videoDate, videoImageURL):
        self.videoID = videoID
        self.videoTitle = videoTitle
        self.videoDesc = videoDesc
        self.videoDate = videoDate
        self.videoImageURL = videoImageURL


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
    print("alooo")
    for channel in channels['items']:

        newVideo = MyVideo(channel['id'].get('videoId'), channel['snippet']['title'], channel['snippet']['description'],
                           channel['snippet']['publishedAt'], channel['snippet']['thumbnails']['high']['url'])

        s = json.dumps(newVideo.__dict__)
        s = json.loads(s)

        # realFuckingArticle = {article['id']: s, }
        db.child("Video").child(channel['id'].get('videoId')).set(s)

        videos.append(newVideo)

print(nextPageToken)
print(videos)
