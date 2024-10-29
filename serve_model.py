from flask import Flask, request, jsonify
import pickle
import numpy as np
import logging

import joblib
model = joblib.load('./Notebooks/Random Forest.pkl')


# Initialize Flask application
app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='fraud_detection.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# Home route
@app.route('/')
def home():
    return "Fraud Detection Model API"

# Predict route (POST)
@app.route('/predict', methods=['POST'])

def predict():
    try:
        # Ensure content type is JSON
        data = request.json  # Get data from the POST request

        #The incoming data is in the form of a list of features
        features = np.array(data['features']).reshape(1, -1)

        # Make prediction
        prediction = model.predict(features)[0]
        result = {'fraud': bool(prediction)}

        # Log request and result
        logging.info(f"Request Data: {data} - Prediction: {result}")

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': 'Invalid data or server error'}), 400


if __name__ == '__main__':
    app.run(debug=True)
