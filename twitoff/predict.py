"""Prediction of User based on tweet embeddings."""

#importing
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import BASILICA

def predict_user(user0_name, user1_name, tweet_text): # tweet text is a hypothetical tweet that the user passes in
    """
  Determine and return which user is more likely to say a given Tweet.

  Example run: predict_user('jackblack', 'elonmusk', 'Tesla, woohoo!')
  Returns 0 (user0_name) or 1 (user1_name)
  """

    # querying our database for user0
    user0 = User.query.filter(User.name == user0_name).one()
    # querying our database for user1
    user1 = User.query.filter(User.name == user1_name).one()

    #grabbing embeddings from our tweet database (reference models.py) to run LR on
    user0_embeddings = np.array([tweet.embedding for tweet in user0.tweets])
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])

    #stacking vertically to create one embeddings matrix (tweets by features)
    embeddings = np.vstack([user0_embeddings, user1_embeddings])
    #creating labels associated with the embeddings that correspond to either user0 (0) or user1 (1)
    labels = np.concatenate([np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    #creating and training LR model based off labels and embeddings
    log_reg = LogisticRegression().fit(embeddings, labels)

    #grabbing embeddings from BASILICA for our hypothetical tweet_text paramater passed in
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')

    #returns a prediction for the hypothetical tweet, returning either 0 or 1
    return log_reg.predict(np.array(tweet_embedding).reshape(1,-1))
