import feedparser as fp
import datetime as dt
import re
from datetime import date, timedelta
from pymongo import MongoClient

aws = fp.parse('https://aws.amazon.com/ko/about-aws/whats-new/recent/feed/')
azure = fp.parse('https://azurecomcdn.azureedge.net/ko-kr/updates/feed/')
aws_img = "https://a0.awsstatic.com/main/images/logos/aws_logo_smile_179x109.png"
CURRENT_TIME = dt.datetime.today()
MONGO_URI = ""

def delete_html_tags(body):
    regx = re.compile('<.*?>')
    pure_text = re.sub(regx,'',body)
    return pure_text

def mongo_connection():
    aws_articles_last_week = []
    client = MongoClient(MONGO_URI)
    db = client.news_data
    mongo_conn = db.articles
    query_result = mongo_conn.find({"insertion_date":{"$gt":CURRENT_TIME-timedelta(days=2)}})
    for article in query_result:
        aws_articles_last_week.append(article)

    categories = []
    db_categories = db.categories.find()
    for category in db_categories:
        categories.append(category['category'])

    return mongo_conn, aws_articles_last_week,categories


temp_list = []
for cur in aws.entries:
    article = {}
    client = MongoClient(MONGO_URI)
    db = client.news_data
    mongo_conn = db.articles
    article['article_title'] = cur.title
    article['article_image'] = aws_img
    article['category'] = "AWS"
    article['article_href'] = cur.link
    article['article_date'] = cur.published
    article['article_body'] = delete_html_tags(cur.description)
    article['insertion_date'] = CURRENT_TIME
    article['article_source'] = "AWS 최근 공지사항"
    article['article_tag'] = "AWS_UPDATE"
    temp_list.append(article)

print(temp_list[0]['article_date'])
# for i in range(len(temp_list)):
#     cur = temp_list.pop()
#     inserted_id = mongo_conn.insert_one(cur).inserted_id
#     print(inserted_id)





# for item in aws.items():
#     print(item)