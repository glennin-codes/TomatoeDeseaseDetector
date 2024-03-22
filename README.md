# Tomato Disease Prediction API
## Overview
- This API predicts tomato diseases using a Convolutional Neural Network (CNN) model trained on tomato disease images. It serves as a backend service for predicting the disease based on images provided by the user.

### Features
Image Upload: Accepts an image file via HTTP POST request.
Prediction: Utilizes a pre-trained CNN model to predict the disease from the uploaded image.
Treatment Information: Retrieves treatment information for the predicted disease through web scraping.
#### Usage
- Send Image for Prediction:

Endpoint: /predict
Method: POST
Parameters: Id ``get id after you create an acount here ``,
Body: Image file ``should be of either jpg,png and webp only``
Response: JSON object containing the predicted disease and treatment information.

Response Format:

```json 

{
    "prediction": "Disease Name",
    "message": "saved successfuly to db",
    "result": [
        {
            "url": "Treatment URL",
            "title": "Treatment Title",
            "content": "Treatment Content (TEXT)"
        },
    
    ]
}
```
status code ``200``

#### Setup
- Clone the repository.
- Install the required Python dependencies listed in requirements.txt.
- Start the Flask server using python app.py.

### Dataset
- The model was trained on a dataset containing images of various tomato diseases. The dataset used for training is not included in this repository.cuase its big over 7gb .it contains over 10000 images

### Model
- The CNN model architecture used for prediction is defined in app.py. - - - - Trained weights are loaded from keras_potato_trained_model_weights.h5.
- The model has about 25768 paramters
- The model has an acuracy of 86.6% on the validation set.

#### Dependencies
- Keras
- GoogleSearch Python Library
- Beautiful Soup
- Requests
- License

This project is licensed under the MIT License - see the [LICENSE](#LICENSE) file for details.