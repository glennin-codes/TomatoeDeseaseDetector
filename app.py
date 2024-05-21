from flask import Flask, request, jsonify
from keras.preprocessing import image
import numpy as np
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.preprocessing.image import ImageDataGenerator
import os
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS
# import aiohttp
# import asyncio
from agrovets_location import find_nearest_agrovets,generate_google_maps_link,get_place_details,generate_photo_url
from googleSearch import search_and_extract
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route('/') 
def index():
    return 'Api Working Succesful! hello world '

@app.route('/location', methods=['GET'])
def  location():
    # Replace with your actual API key
    api_key = os.getenv('api_key')


    # Latitude and Longitude of Nairobi (center)
    nairobi_location = "-1.286389,36.817223"
    
  # Search for agrovets
    agrovets = find_nearest_agrovets(api_key, nairobi_location)
    result = []
    
    if agrovets:
        for agrovet in agrovets:
            place_id = agrovet.get("place_id")
            details = get_place_details(api_key, place_id)
            photos = agrovet.get("photos", [])
            photo_url = generate_photo_url(photos[0]["photo_reference"], api_key) if photos else None
            if details:
                name = details.get("name")
                address = details.get("vicinity")
                phone_number = details.get("formatted_phone_number")
                maps_link = generate_google_maps_link(place_id)
                print(f"Name: {name}\nAddress: {address}\nPhone Number: {phone_number}\nGoogle Maps Link: {maps_link}\nphoto:{photo_url}\n")
                
                result.append({
                    "Name": name,
                    "Address": address,
                    "Phone Number": phone_number,
                    "Google Maps Link": maps_link,
                    "Photo": photo_url
                })
        return jsonify(result)
    else:
        print("No agrovets found.") 
        return jsonify({'error': 'No agrovets found.'}), 404



   
 

# Load the model architecture
model = Sequential()
model.add(Convolution2D(32, 3, 3, input_shape=(128, 128, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Convolution2D(16, 3, 3, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(units=128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dropout(rate=0.5))
model.add(Dense(units=10, activation='softmax'))

# Load the trained weights
model.load_weights('keras_potato_trained_model_weights.h5')

# Get the class indices mapping from the training code
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Create the generator
training_set = train_datagen.flow_from_directory(
    'train',  # Update with the actual path
    target_size=(128, 128),
    batch_size=64,
    class_mode='categorical'
)


# Obtain class indices
label_map = training_set.class_indices


# Define an endpoint for predicting the disease class
@app.route('/api/predict', methods=['POST'])
async def predict():
    if request.method == 'POST':
        # Get the file from the request
        file = request.files['file']
        id = request.args.get('id')
        
        # Extract the original filename and extension
        original_filename, extension = os.path.splitext(file.filename)

        # Save the file temporarily with its original name and extension
        file_path = f'temp{extension}'
        file.save(file_path)

        # Load the image and make predictions
        img = image.load_img(file_path, target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize the image

        # Make predictions using the model with loaded weights
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions)

        # Get the class label from the label map
        predicted_class_name = [k for k, v in label_map.items() if v == predicted_class][0]
        # query=f"{predicted_class_name} treatement"
        # search_results = search_and_extract(query, num_results=2)
        # Return the prediction and disease information as JSON
        result = {'prediction': predicted_class_name, "message":"saved to db succesfuly"}
          # Make a PUT request to  Node.js server
        if result:
            node_api_url = f'http://localhost:8080/api/predict/{id}'
            print(id)
            data = { 'diseaseName': predicted_class_name}
            response = requests.patch(node_api_url, json=data)
            if response.ok:
               return jsonify(result),200
            else:
                return jsonify({'error': f'Failed to update user data in Node.js API: {response.text}'}), 500


        return jsonify({'error': 'Prediction failed'}), 400
          
        

if __name__ == '__main__':
    app.run(debug=True)
