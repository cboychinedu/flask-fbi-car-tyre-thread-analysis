#!/usr/bin/env python3

# Importing the necessary modules
import os
import logging
from flask import Flask, session
from flask import render_template, url_for
from flask_cors import CORS
from datetime import timedelta
from dotenv import load_dotenv

# Loading the environment variables
load_dotenv();

# Importing the views
from Home.routes import home
from Register.routes import register
from Dashboard.routes import dashboard

# Creating the flask application
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = os.getenv('SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=24)

# Setting cors configurations
CORS(app)

# Register the views using the "app.register" function
app.register_blueprint(home, url_prefix="/")
app.register_blueprint(register, url_prefix="/register")
app.register_blueprint(dashboard, url_prefix='/dashboard')

# # Logging the configurations to a file on disk
# logging.basicConfig(filename="requests.log", level=logging.DEBUG,
#                     format="%(asctime)s %(message)s %(filename)s %(module)s %(pathname)s",
#                     datefmt="%m/%d/%Y %I:%M:%S %p")


@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

# Adding the session configurations
@app.before_request
def make_session_permanent():
    # Setting the server message
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=45)


# Handling custom error pages
@app.errorhandler(404)
def page_not_found(e):
    # Execute this route if the user navigates to a route that does
    # not exist
    return render_template('page_not_found.html'), 404;

# Handling the error request 500
@app.errorhandler(500)
def internal_server_error(e):
    # Execute this route if the request generated gives an internal server error
    return render_template('bad_request.html'), 500;

# Creating a function called dated url for tracking the changes made
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# Adding functions for updating the web application on reload
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for) 

# Running the server
if __name__ == "__main__":
    # app.run(port=5000, host='localhost', debug=True)
    app.run(port=5000, host="192.168.43.95", debug=True)
