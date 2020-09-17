"""Retrieve Tweets, embeddings, and persist in the database"""
from os import getenv
import tweepy
import basilica
from .models import DB, Tweet, User

# twitter users we will populate
TWITTER_USERS = ['calebhicks', 'elonmusk', 'rrherr', 'SteveMartinToGo', 'alyankovic', 'nasa', 'sadserver', 'jkhowland', 'austen', 'common_squirrel', 'KenJennings', 'conanobrien', 'big_ben_clock', 'IAM_SHAKESPEARE']

# This gives us authorization through .env file
TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_API_KEY'), getenv('TWITTER_API_KEY_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)
BASILICA = basilica.Connection(getenv('BASILICA_KEY'))

# create user based on the username with associated tweets
def add_or_update_user(username):
  try:
    #grabbing twitter user
    twitter_user = TWITTER.get_user(username)
    # add or update user
    db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
    DB.session.add(db_user) 

    #grabbing tweet
    tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, 
        tweet_mode='extended', since_id=db_user.newest_tweet_id)

    # if we get a new tweet then change the newest_tweet_id associated with ther user
    if tweets:
      db_user.newest_tweet_id = tweets[0].id

    #loops for tweets 
    for tweet in tweets:
      embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
      db_tweet = Tweet(id=tweet.id, text=tweet.full_text, embedding=embedding)
      db_user.tweets.append(db_tweet)
      DB.session.add(db_tweet)

  except Exception as e: 
    print('ERROR PROCESSING {}: {}'.format(username, e))
    raise e

  else:
    DB.session.commit()


#populations using add_or_update user
def insert_example_users():
  DB.drop_all()
  DB.create_all()
  add_or_update_user('elonmusk')
  add_or_update_user('jackblack')



