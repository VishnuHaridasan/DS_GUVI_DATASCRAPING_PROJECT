import pymongo
import pandas as pd
# import pymongo
import snscrape.modules.twitter as sntwitter
import time
# from snscrape.modules import snscrape_twitter as sntwitter
# def scrape_tweets(keyword, start_date, end_date, limit):
#     # create empty list to store scraped data
#     tweets_list = []
#     # iterate over each tweet using snscrape
#     for i, tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' since:' + start_date + ' until:' + end_date).get_items()):
#         if i >= limit:
#             break
#         # create a dictionary to store required fields
#         tweet_dict = {'date': tweet.date.strftime('%Y-%m-%d %H:%M:%S'),
#                       'id': tweet.id,
#                       'url': tweet.url,
#                       'content': tweet.content,
#                       'user': tweet.user.username,
#                       'reply_count': tweet.replyCount,
#                       'retweet_count': tweet.retweetCount,
#                       'language': tweet.lang,
#                       'source': tweet.sourceLabel,
#                       'like_count': tweet.likeCount}
#         # append the dictionary to the list
#         tweets_list.append(tweet_dict)
#     # return the list of dictionaries
#     return tweets_list


def scrape_tweets(keyword, start_date, end_date, limit):
    # create empty list to store scraped data
    tweets_list = []
    # iterate over each tweet using snscrape
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' since:' + start_date + ' until:' + end_date).get_items()):
        if i >= limit:
            break
        # create a dictionary to store required fields
        tweet_dict = {'date': tweet.date.strftime('%Y-%m-%d %H:%M:%S'),
                      'id': tweet.id,
                      'url': tweet.url,
                      'content': tweet.content,
                      'user': tweet.user.username,
                      'reply_count': tweet.replyCount,
                      'retweet_count': tweet.retweetCount,
                      'language': tweet.lang,
                      'source': tweet.sourceLabel,
                      'like_count': tweet.likeCount}
        # append the dictionary to the list
        tweets_list.append(tweet_dict)
         # add a sleep timer between requests
        time.sleep(5)
    # return the list of dictionaries
    return tweets_list


# # connect to MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# # create a database
# db = client["twitter_data"]
# # create a collection
# collection = db["scraped_data"]

from pymongo import MongoClient

#Creating a pymongo client
client = MongoClient('localhost', 27017)

#Getting the database instance

# db = client['twitter_data']
db = client['twitter_collection']

#Creating a collection
collection = db['scraped_data']
print("Collection created........")


def store_data_in_mongodb(scraped_data, keyword, start_date, end_date):
    # create a dictionary to store scraped data and search keyword
    data_dict = {'keyword': keyword,
                 'start_date': start_date,
                 'end_date': end_date,
                 'data': scraped_data}
    # insert the dictionary into MongoDB collection
    collection.insert_one(data_dict)




import streamlit as st

# set page title
st.set_page_config(page_title='Twitter Data Scraper', layout='wide')
pd.set_option('display.max_colwidth', None)

# create sidebar with input fields
with st.sidebar:
    st.title('Twitter Data Scraper')
    keyword = st.text_input('Enter hashtag or keyword')
    start_date = st.date_input('Start date')
    end_date = st.date_input('End date')
    limit = st.number_input('Limit')

# create button to scrape data
if st.button('Scrape Data'):
    # scrape data using snscrape function
    scraped_data = scrape_tweets(keyword, str(start_date), str(end_date), limit)
    # store data in MongoDB using pymongo function
    store_data_in_mongodb(scraped_data,keyword, str(start_date), str(end_date))