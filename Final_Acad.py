import tweepy
from twitter_authentication import bearer_token
import time
import pandas as pd

client = tweepy.Client(bearer_token, wait_on_rate_limit=True)

account_tweets = []
for response in tweepy.Paginator(client.search_all_tweets, 
                                 query = ["IT professionals" and 'depression' or 'anxiety' or 'mental health' or 'mental' or 'health'],
                                 user_fields = ['id','username', 'name','created_at','public_metrics', 'description', 'location','verified','protected','pinned_tweet_id'],
                                 tweet_fields = ['author_id','id','conversation_id','created_at','text','edit_controls','geo','in_reply_to_user_id','lang','possibly_sensitive','public_metrics','referenced_tweets','reply_settings','source'],
                                 expansions = ['author_id', 'in_reply_to_user_id','referenced_tweets.id','geo.place_id'],
                                 start_time = '2018-10-01T00:00:00Z',
                                 end_time = '2020-10-31T00:00:00Z',
                            max_results= 500):
    time.sleep(4)
    account_tweets.append(response)



result = []
user_dict = {}
# Loop through each response object
for response in account_tweets:
    # Take all of the users, and put them into a dictionary of dictionaries with the info we want to keep
    for user in response.includes['users']:
        user_dict[user.id] = {'id':user.id,
                              'username': user.username, 
                              'name': user.name,
                              'account created': user.created_at,
                              'followers': user.public_metrics['followers_count'],
                              'tweets': user.public_metrics['tweet_count'],
                              'pinned_tweet':user.pinned_tweet_id,
                              'description': user.description,
                              'location': user.location,
                              'protected': user.protected,
                              'verified': user.verified
                             }
    for tweet in response.data:
        # For each tweet, find the author's information
        author_info = user_dict[tweet.author_id]
        # Put all of the information we want to keep in a single dictionary for each tweet
        result.append({#'author_id': tweet.author_id, 
                       'username': author_info['username'],
                       'id':tweet.id,
                       'author_followers': author_info['followers'],
                       'author_tweets': author_info['tweets'],
                       'author_description': author_info['description'],
                       'author_location': author_info['location'],
                       'text': tweet.text,
                       'edit_countrols':tweet.edit_controls,
                       'created_at': tweet.created_at,
                       'replies':tweet.in_reply_to_user_id,
                       'language': tweet.lang,
                       'referenced_tweets': tweet.referenced_tweets,
                       'reply_settings': tweet.reply_settings,
                       'possibly_sensitive': tweet.possibly_sensitive,
                       'retweet_count': tweet.public_metrics['retweet_count'],
                       'reply_count': tweet.public_metrics['reply_count'],
                       'like_count': tweet.public_metrics['like_count'],
                       'quote_count': tweet.public_metrics['quote_count'],
                       'source': tweet.source

                      })

# Change this list of dictionaries into a dataframe
df = pd.DataFrame(result)
df.to_csv('TwitterDataCollection.csv')
