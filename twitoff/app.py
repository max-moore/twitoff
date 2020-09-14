"""Main app/routing file for TwitOff!"""

#importing flask and data models
from flask import Flask, render_template
from .models import DB, User, insert_example_users

#function to create our app
def create_app():
  #initializing our flask app
  app = Flask(__name__)

  #for storing information in our database
  app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///db.sqlite3'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  #initilizes database within our app
  DB.init_app(app)

  #listens for path '/' and executes function when heard
  @app.route('/')
  def root():
    #re creates our database to avoid errors and duplicates
    DB.drop_all()
    DB.create_all()
    #calls our function within the models.py file to insert users
    insert_example_users()

    # a select * query using SQLAlchemy
    users = User.query.all()
    #rendering template that we created passing Home and query to template
    return render_template('base.html', title="Home", users=User.query.all())

  #returns that app with everything we are trying to render
  return app
