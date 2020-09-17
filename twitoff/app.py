"""Main app/routing file for TwitOff!"""

#importing flask and data models
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import  insert_example_users, add_or_update_user
from os import getenv
from .predict import predict_user


#function to create our app
def create_app():
    #initializing our flask app
    app = Flask(__name__)

    #for storing information in our database
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #initilizes database within our app
    DB.init_app(app)

    #listens for path '/' and executes function when heard
    @app.route('/')
    def root():
        return render_template('base.html', title="Home", users=User.query.all())

    @app.route('/compare', methods=['POST']) # POST = changing something
    def compare():

        #using request to access user input and assigning which user was picked to user0 and user1
        user0, user1 = sorted([request.values['user0'], request.values['user1']])

        #if user0 == user1 return message explanation
        if user0 == user1:
            message = 'Cannot compare a user to themselves'
        else: #no error
            #run model and return model with who is more likely on prediction.html
            prediction = predict_user(user0, user1, request.values['tweet_text'])
            message = "{} is more likely to be said by {} than {}".format(
                request.values['tweet_text'], user1 if prediction else user0, user0 if prediction else user1
            )
        # render prediction.html and passes title and message
        return render_template('prediction.html', title='Prediction', message=message)

    # two decorators/routes depending upon actions in user.html (reference user.html)
    @app.route('/user', methods=['POST'])  # POST = changing something
    @app.route('/user/<name>', methods=['GET']) # POST = getting something
    def user(name=None, message=''):
        #grabs or creates user
        name = name or request.values['user_name']
        try:
            #If most request i.e. form submitted than update or add user to DB and assign message
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} succesfully added!".format(name)

            # initialize tweets variable with users tweets
            tweets = User.query.filter(User.name == name).one().tweets

        # if error presented change message
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            #assign empty list for tweets and display nothing since iterated through in user.html
            tweets = []

        #renders user.html passing title, tweets, and message to be accessed
        return render_template('user.html', title=name, tweets=tweets, message=message)



    #associated with update button
    @app.route('/update')
    def update():
        return render_template('base.html', title="users updated!", users=User.query.all())

    #associated with reset button
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title="Reset Database")

    #returns that app with everything we are trying to render
    return app
