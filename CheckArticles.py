import pyrebase
import requests
import json

config = {
    ...
}

####FETCH FROM FIREBASE
firebase = pyrebase.initialize_app(config)
db = firebase.database()
firebaseResult = db.child("/Articles").get()

##### INSERT FIREBASE ARTICLE'S IDS
firebaseIds = []
for articleId in firebaseResult.val():
    firebaseIds.append(int(articleId))

###### FETCH FROM WORDPRESS AND IDS
articles = {}
wordpressIds = []
i = 1
while True:
    response = requests.get("https://www.bilimtreni.com/wp-json/wp/v2/posts?page=" + str(i))
    text = json.dumps(response.json(), sort_keys=True, indent=4)
    channels = json.loads(text)
    if response.status_code == 400:
        print("Status 400")
        break
    for channel in channels:
        articles[channel['id']] = channel
        wordpressIds.append(channel['id'])
    i += 1

#FIND DIFFERENCES
for firebaseId in firebaseIds[:]:
    for wordpressId in wordpressIds:
        if int(firebaseId) == int(wordpressId):
            firebaseIds.remove(firebaseId)
            wordpressIds.remove(wordpressId)

#### REMOVE
for silinecek in firebaseIds:
    res = db.child("/Articles").child(silinecek).remove()
    print(res)

class MyArticle(object):
    def __init__(self, articleId, articleTitle, articleDesc, articleBody, articleAuthor, articleDate, articleImageURL):
        self.articleId = articleId
        self.articleTitle = articleTitle
        self.articleDesc = articleDesc
        self.articleBody = articleBody
        self.articleAuthor = articleAuthor
        self.articleDate = articleDate
        self.articleImageURL = articleImageURL


for eklenecek in wordpressIds:
    ekle = articles[eklenecek]
    # image start
    if 'wp:featuredmedia' in list(ekle['_links'].keys()):
        url = ekle['_links']['wp:featuredmedia'][0]['href']
        response = requests.get(url)
        imageJson = json.loads(json.dumps(response.json(), sort_keys=True, indent=4))
        imageURL = imageJson['source_url']
        print(imageURL)

    else:
        imageURL = "null"

    # image end

    # author name start
    url = ekle['_links']['author'][0]['href']
    response = requests.get(url)
    authorJson = json.loads(json.dumps(response.json(), sort_keys=True, indent=4))
    # author name end

    new = MyArticle(ekle['id'], ekle['title']['rendered'], ekle['excerpt']['rendered'],
                    ekle['content']['rendered'], authorJson['name'], ekle['date'], imageURL)
    s = json.dumps(new.__dict__)
    s = json.loads(s)

    # realFuckingArticle = {article['id']: s, }
    db.child("Articles").child(ekle['id']).set(s)

print(type(articles))
print(articles)

print(firebaseIds)  # silinecek
print(wordpressIds)  # eklenecek
