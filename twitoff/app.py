"""Main app/routing file for TwitOff!"""

#importing flask and data models
from flask import Flask, render_template
from .models import DB, User
from .twitter import  insert_example_users

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
    return render_template('base.html', title="Home", users=User.query.all())

  #associated with update button
  @app.route('/update')
  def update():
    insert_example_users()
    return render_template('base.html', title="Updated Users", users=User.query.all())

  #associated with reset button
  @app.route('/reset')
  def reset():
    DB.drop_all()
    DB.create_all()
    return render_template('base.html', title="DATABASE RESET")
  
  #returns that app with everything we are trying to render
  return app
