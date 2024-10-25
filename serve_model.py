# from flask import Flask, request, jsonify
# import pickle
# import numpy as np
# import logging

# # Load the trained model (replace 'model.pkl' with your actual model file)
# with open('./Notebooks/RandomForestClassifier_2024-10-23-13-48-20.pkl', 'rb') as f:
#     model = pickle.load(f)

# # Initialize Flask application
# app = Flask(__name__)

# # Set up logging
# logging.basicConfig(filename='fraud_detection.log', level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(message)s')

# @app.route('/')
# def home():
#     return "Fraud Detection Model API"

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.json  # Get data from the POST request
        
#         # Assuming the incoming data is in the form of a list of features
#         features = np.array(data['features']).reshape(1, -1)

#         # Make prediction
#         prediction = model.predict(features)[0]
#         result = {'fraud': bool(prediction)}

#         # Log request and result
#         logging.info(f"Request Data: {data} - Prediction: {result}")

#         return jsonify(result)

#     except Exception as e:
#         logging.error(f"Error occurred: {str(e)}")
#         return jsonify({'error': 'Invalid data or server error'}), 400

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import pickle
import numpy as np
import logging

# Load the trained model
with open('./Notebooks/RandomForestClassifier_2024-10-23-13-48-20.pkl', 'rb') as f:
    model = pickle.load(f)

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
        data = request.json  # Get data from the POST request
        
        # Assuming the incoming data is in the form of a list of features
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

# New GET route to display model-related data
@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Example data: Feature importance (for tree-based models like RandomForest)
        if hasattr(model, 'feature_importances_'):
            feature_importance = model.feature_importances_.tolist()
        else:
            feature_importance = "Feature importance is not available for this model."

        # Sample input for prediction (replace with real sample data or use random data)
        sample_input = np.random.rand(1, model.n_features_in_)  # Random sample with the same number of features
        sample_prediction = model.predict(sample_input)[0]

        # Data to display in the browser
        data = {
            'message': 'Model-related information from the fraud detection model',
            'feature_importance': feature_importance,
            'sample_input': sample_input.tolist(),
            'sample_prediction': bool(sample_prediction)
        }

        # Log the request
        logging.info("GET request received at /data - Returning model information.")

        return jsonify(data)

    except Exception as e:
        logging.error(f"Error occurred in /data endpoint: {str(e)}")
        return jsonify({'error': 'Could not retrieve model data'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
