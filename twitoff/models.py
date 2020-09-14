"""SQLAlchemy models and utility functions for TwitOff!"""

from flask_sqlalchemy import SQLAlchemy

#creating database
DB = SQLAlchemy()

#creating classes that act as 'tables' within our DB
class User(DB.Model):

  #creating columns using SQLAlchemy methods
  id = DB.Column(DB.BigInteger, primary_key=True) #primary key id
  name = DB.Column(DB.String, nullable=False) #string column that can not be null

  #for readability when trying to access info
  def __repr__(self):
    return '-User {}-'.format(self.name)


#creating a tweet class that will connect to our User table
class Tweet(DB.Model):
  
  #similar to our User class/table
  id = DB.Column(DB.BigInteger, primary_key=True)
  text = DB.Column(DB.Unicode(300)) #so we can grab everything that someone might tweet, links and all

  #Creating a user id that is the same as the one we created in User class, relates the database
  user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
  #back referencing that acts as a join and allows us to know name associated with tweet
  user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

  #for readability
  def __repr__(self):
    return '-Tweet {}-'.format(self.text)

#populates database when called (called in app.py)
def insert_example_users():
  # IF we run multiple times then we will get error because users exist, which is why we drop in app.py
  nick = User(id=1, name='nick')
  elon = User(id=2, name='elonmusk')
  #have to add our users and then commit using SQLAlchemy
  DB.session.add(nick)
  DB.session.add(elon)
  DB.session.commit()