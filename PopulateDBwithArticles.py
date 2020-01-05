import json
import requests
import pyrebase

config = {
   ...
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
print("nasıl bastık")
articles = []
i = 1
while True:
    response = requests.get(
        "https://www.bilimtreni.com/wp-json/wp/v2/posts?page=" + str(i))
    text = json.dumps(response.json(), sort_keys=True, indent=4)
    channels = json.loads(text)
    if response.status_code == 400:
        print("Status 400")
        break
    for channel in channels:
        articles.append(channel)
    print(i)
    i += 1


class MyArticle(object):
    def __init__(self, articleId, articleTitle, articleDesc, articleBody, articleAuthor, articleDate, articleImageURL):
        self.articleId = articleId
        self.articleTitle = articleTitle
        self.articleDesc = articleDesc
        self.articleBody = articleBody
        self.articleAuthor = articleAuthor
        self.articleDate = articleDate
        self.articleImageURL = articleImageURL


for article in articles:
    print(type(article))
    print(article)
    # image start
    if 'wp:featuredmedia' in list(article['_links'].keys()):
        url = article['_links']['wp:featuredmedia'][0]['href']
        response = requests.get(url)
        imageJson = json.loads(json.dumps(response.json(), sort_keys=True, indent=4))
        imageURL = imageJson['source_url']
        print(imageURL)

    else:
        imageURL = "null"

    # image end

    # author name start
    url = article['_links']['author'][0]['href']
    response = requests.get(url)
    authorJson = json.loads(json.dumps(response.json(), sort_keys=True, indent=4))
    # author name end

    new = MyArticle(article['id'], article['title']['rendered'], article['excerpt']['rendered'],
                    article['content']['rendered'], authorJson['name'], article['date'], imageURL)
    s = json.dumps(new.__dict__)
    s = json.loads(s)

    #realFuckingArticle = {article['id']: s, }
    db.child("Articles").child(article['id']).set(s)

print("nasıl bastık")
