#!/usr/bin/env python3

# Importing the necessary modules
import json
import bcrypt
from mongo import MongoDB
from flask import request, jsonify, session
from flask import request, Blueprint, render_template

# Creating the blueprint object
register = Blueprint('register', __name__, template_folder='templates', static_folder='static');

# Creating an instance of the databae
db = MongoDB();

# Creating the register route home age
@register.route('/', methods=['GET', 'POST'])
def RegisterHome():
    # Checking if the user is logged in
    if 'email' in session:
        email = session['email']
    
        # Render the dashboard page
        return render_template('Dashboard.html')


    # Checking if the request made was a POST request
    if request.method == 'POST':
        # Getting the firstname, lastname, email, and password data
        # from the request body
        request_data = request.get_json()
        firstname = request_data['firstname'];
        lastname = request_data['lastname'];
        email = request_data['email'];
        password = request_data['password'];

        # Connecting to the Mongodb database, and save the users data
        db.connect('mongodb://localhost:27017/', 'car_tyre_analysis')

        """
         Here, we need to verify if the user's data are already registered
         on the mongodb database before saving the new data to the server.
         And if the user exists, redirect the user to the login page.
        """
        database_data = db.retrieve_data('users', email=email)

        # Hashing the password
        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14));
        hash_password = hash_password.decode('utf-8');

        # Rebuilding the request_data
        request_data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": hash_password,
        }

        # Checking the returned type if None, execute the block of code
        # below
        if database_data == None:
            # Save the new user on the database
            result = db.save_data('users', request_data)

            # Checking if the results returned a value of True
            if (result):
                #
                return jsonify({'status': 'success', 'message': 'User\'s data saved on the database'}), 200

            else:
                return jsonify({'status': 'error', 'message': 'Unable to save the user\'s data on the database'}), 500

        #
        else:
            #
            return jsonify({'status': 'error', 'message': 'The user already exists on the database.'}), 501


    # Else if the request was a get request
    else:
        return render_template('Register.html')
