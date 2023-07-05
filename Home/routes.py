#!/usr/bin/env python3 

# Importing the necessary modules 
import os 
import json 
import bcrypt 
from base64 import b64encode 
from flask import request 
from flask import Blueprint 
from datetime import datetime 
from flask import session, flash, redirect
from mongo import MongoDB
from flask import render_template, url_for

# Creating the blueprint object 
home = Blueprint('home', __name__, template_folder='templates', static_folder='static'); 

# Creating an instance of the database 
db = MongoDB(); 

# Creating the home page 
@home.route('/', methods=['GET', 'POST'])
def HomePage(): 
    # Checking if the user is logged in 
    if 'email' in session: 
        email = session['email']

        # Render the dashboard page 
        return render_template('Dashboard.html')
    
    # Checking if the request was a POST request 
    if request.method == 'POST': 
        # Getting the email, and password data from the 
        # request data available in the submitted html form 
        request_data = request.get_json()
        email = request_data['email']
        password = request_data['password']

        # Getting the user's data by connecting to the Mongodb database server 
        db.connect('mongodb://localhost:27017/', 'car_tyre_analysis')
        database_data = db.retrieve_data('users', email=email)

        # If the database value returns a None type, execute the 
        # block of code below. 
        if database_data == None: 
            return { "message": "User not found on the database", "status": "error"}, 500; 

        # Converting the json string, into a json object using the json module 
        database_data = json.loads(database_data.json);


        # If the user is found on the database with the specificed email address, execute 
        # the block of code below 
        if database_data: 
            # Validate the user's password to see if it is correct 
            passwordCondition = bcrypt.checkpw(password.encode('utf-8'), database_data['password'].encode('utf-8'))

            # Checking if the password condition returned a True, or False value 
            if (passwordCondition == True): 
                # Give the user a session value, and redirect the user to the 
                # Dashboard page 
                session['email'] = email 

                # Creating the success message 
                successMessage = {
                    "status": "success", 
                    "message": "User logged in", 
                    "statusCode": 200, 
                }

                # Sending the error message 
                return successMessage; 


            # If the password condition returned a False value, exeucte the 
            # block of code below 
            elif (passwordCondition == False): 

                # Creating the error message 
                errorMessage = {
                    "status": "error", 
                    "message": "Invalid username, or password", 
                    "statusCode": 500, 
                }

                # Sending back the error message 
                return errorMessage; 
            
            # 
            return {"message": "User found", "PasswordValidation": passwordCondition}; 

        # Else 
        else: 
            # Creating an error message 
            errorMessage = {
                "status": "error", 
                "message": "User not found on the database", 
                "statusCode": 501, 
            }
        
            # Returning the database data 
            return errorMessage; 


    else: 
        # Rendering the home page 
        return render_template('Home.html')
    

# Creating the sign out route 
@home.route("/logout", methods=["GET"])
def Logout():
    # Removing the email from the session storage 
    session.pop("email", None); 

    # Redirecting the user back to the home page 
    return redirect(url_for("home.HomePage"))