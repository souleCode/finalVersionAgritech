from flask import Flask, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)


# Load the scaler
feature_scaler = joblib.load("../Models/feature_scaler.pkl")

# Load all the model

model_recommand = joblib.load("../Models/naive_bayes.pkl")

# Define a route for predicting crop type


@app.route('/recommand', methods=['POST'])
def predict():
    # Get JSON data from the request
    data = request.json
    # Extract features from the JSON data
    try:
        n = data['N']
        p = data['P']
        k = data['K']
        temperature = data['temperature']
        humidity = data['humidity']
        ph = data['ph']
        rainfall = data['rainfall']
    except KeyError as e:
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400

    # Create a feature vector
    features = np.array([[n, p, k, temperature, humidity, ph, rainfall]])

    # Scale the input features
    features_scaled = feature_scaler.transform(features)

    # Predict with each model

    prediction = model_recommand.predict(features_scaled)[0]

    # Return the predictions as a JSON response
    return jsonify({
        "recommandation": prediction
    })


if __name__ == '__main__':
    app.run(debug=True, port=5002)
