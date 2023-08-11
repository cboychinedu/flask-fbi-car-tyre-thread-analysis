#!/usr/bin/env python3 

# Importing the necessary modules 
import os 
import json 
from flask import request 
from flask import Blueprint 
from datetime import datetime
from flask import session, redirect 
from mongo import MongoDB 
from flask import render_template, url_for 
from Dashboard.MachineLearningModel.main import Analyze

# Creating the blueprint object 
dashboard = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static'); 

# Creating an instance of the database 
db = MongoDB(); 

# Creating a route for performing the car-tyre thread analysis 
@dashboard.route('/perform-analysis', methods=['POST'])
def performAnalysis(): 
    # Getting the image url information 
    imageMetadata = request.get_json(); 

    # Geting the image name 
    imageName = imageMetadata['imageName']

    # Creating an instance of the Analyze class 
    analyze = Analyze(imageName=imageName)

    # Performing the analysis 
    result = analyze.perform_analysis(); 

    # returning the results 
    return result; 

# Creating a route for uploading the image 
@dashboard.route('/upload', methods=['POST'])
def upload(): 
    # 
    image = request.files['image']

    # 
    if image: 
        # Getting the image filename 
        filename = image.filename 

        # Getting the image extension 
        imgExt = filename.split(".")[1]

        # Getting the date timestamp value for the image uploaded 
        timestampValue = datetime.now().isoformat(timespec='seconds')
        filename = timestampValue + '.' + imgExt;         

        # Setting the full path for the image upload directory 
        imageUploadDir = os.path.sep.join(['static', 'Uploads'])
        imageUploadDir = os.path.sep.join([imageUploadDir, filename])

        # Creating the image url 
        imageUrl = f"/{imageUploadDir}"; 

        # Saving the image to disk 
        image.save(imageUploadDir)

        # Creating a response message for the uploaded image 
        data = {
            "imageUrl": imageUrl, 
            "imageName": filename, 
            "status": "success", 
            "message": "Image successfully uploaded", 
            "statusCode": 200, 
        }

        # Sending back the image data to the client 
        return data; 
    
    # Else if the image wasn't saved, execute the block 
    # of code below 
    else: 
        # Creating a response message for the uploaded image 
        data = {
            "imageUrl": imageUrl, 
            "imageName": filename, 
            "status": "error", 
            "message": "Image not uploaded on the server", 
            "statusCode": 500, 
        }
 
        # Sending back the data to the client 
        return data; 

# Creating a route for getting the logged in user's details 
@dashboard.route('/get-users-details', methods=['POST', 'GET'])
def GetUsers(): 
    # Checking if the users are logged in 
    if 'email' in session: 
        email = session.get('email')

        # Getting the user's full details 
        # Connecting into the database 
        db.connect('mongodb://localhost:27017/', 'car_tyre_analysis') 
        database_data = db.user_infomation('users', email=email)

        # Converting the json string, into a json object using the json 
        # module 
        database_data = json.loads(database_data.json); 

        # If the database value returns a None type, execute the block 
        # of code below 
        if database_data == None: 
            return { "status": "error", "message": "Error retriving the user's information."}
        
        # Return the data 
        return database_data; 

    # If the user is not logged in, execute the 
    # block of code below 
    else: 
        # Create an error message, and send it back to the 
        # client 
        errMessage = { 'status': 'error', 'message': 'User not logged in'}; 
        return errMessage;  


# Creating the dashboard home page 
@dashboard.route('/', methods=['GET'])
def Dashboard(): 
    # Checking if the user is logged in 
    if 'email' in session: 
        email = session["email"]

        # Render the dashboard page 
        return render_template('Dashboard.html')
    
    # If the user email wasn't found in the session localstorage 
    # execute the block of code below 
    else: 
        # Redirecting the user back to the home page 
        return redirect(url_for('home.HomePage')); 