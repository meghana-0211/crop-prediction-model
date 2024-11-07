import joblib
import pandas as pd
import numpy as np

class CropPredictor:
    def __init__(self, model_dir):
        self.model = joblib.load(f"{model_dir}/model.joblib")
        self.scaler = joblib.load(f"{model_dir}/scaler.joblib")
        self.label_mapping = joblib.load(f"{model_dir}/label_mapping.joblib")
        
    def predict(self, features):
        input_data = pd.DataFrame([features])
        input_scaled = self.scaler.transform(input_data)
        prediction = self.model.predict(input_scaled)[0]
        return self.label_mapping[prediction]

# api/app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from model.predictor import CropPredictor

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Initialize the predictor
predictor = CropPredictor('model/saved_models')

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Prepare features in the correct order
        features = {
            'N': 50,  # default value
            'P': 50,  # default value
            'K': 50,  # default value
            'temperature': float(data['temperature']),
            'humidity': float(data['humidity']),
            'ph': 6.5,  # default value
            'rainfall': float(data['rainfall']),
            'light_intensity': float(data['light_intensity'])
        }
        
        prediction = predictor.predict(features)
        return jsonify({'crop': prediction})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500