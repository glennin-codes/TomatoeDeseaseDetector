from flask import Flask, request, jsonify
from keras.preprocessing import image
import numpy as np
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.preprocessing.image import ImageDataGenerator
import os
from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio

app = Flask(__name__)

@app.route('/') 
def index():
    return 'Api Working Succesful!'

 
 

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
@app.route('/predict', methods=['POST'])
async def predict():
    if request.method == 'POST':
        # Get the file from the request
        file = request.files['file']

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
        disease_info = await get_disease_information(predicted_class_name)
        # Return the prediction and disease information as JSON
        result = {'prediction': predicted_class_name, 'disease_info': disease_info}
        return jsonify(result)
async def get_disease_information(disease_name):
    search_url = f'https://www.bing.com/search?q={disease_name} disease treatment'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as response:
            print(response)
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')

                # Check if the element with class 'b_caption' is found
                result_div = soup.find('div', {'class': 'b_caption'})
                if result_div:
                    # Extract relevant information from the search results
                    # You may need to inspect the HTML structure of the search results and adjust this part accordingly
                    information = result_div.text.strip()
                    return information
                else:
                    return 'No information found'
            else:
                return 'Failed to retrieve information'

if __name__ == '__main__':
    app.run(debug=True)
