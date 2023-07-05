#!/usr/bin/env python3 

# Imporitng the necessary modules 
import os 
import json 
import cv2 
import pickle 
from time import sleep 

# Get the current working directory 
base_dir = os.getcwd(); 

# Setting the path to the image directory 
imageDir = os.sep.join([base_dir, 'static'])
imageDir = os.sep.join([imageDir, 'Uploads'])

# Setting the path to the svm model directory 
svmModelPath = os.sep.join([base_dir, 'Dashboard'])
svmModelPath  = os.sep.join([svmModelPath, 'MachineLearningModel'])
svmModelPath  = os.sep.join([svmModelPath, 'finalized_model.sav'])

# Creating a class called Analyze 
class Analyze: 
    def __init__ (self, imageName):
        self.imageName = imageName
        self.model = None 

    # Creating a method for loading the svm model 
    def load_model(self): 
        # Getting the path to the machine learning model 
        svmModel = open(svmModelPath, 'rb')
        svmModel = pickle.load(svmModel)

        # Returning the model 
        return svmModel; 

    # Creating a method for performing predictions 
    def perform_analysis(self): 
        # Loading the model into memory 
        model = self.load_model(); 

        # Getting the full path to the image 
        image = os.sep.join([imageDir, self.imageName])

        # Loading the image using the python-opencv module
        image = cv2.imread(image) 
        image = cv2.resize(image, (250, 250))
        image = image.ravel() 
        image = image.reshape(1, -1); 

        # Getting the result 
        result = model.predict(image)
        result = result[0]; 

        # Return the result 
        return {
            "status": "success", 
            "ModelAccuracy": "99.87%", 
            "ThreadType": result, 
        }