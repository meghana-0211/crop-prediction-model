from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingClassifier
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

# Load and prepare the model (using your existing code)
try:
    df = pd.read_csv("Crop_recommendation.csv")
except Exception as e:
    print(f"Error loading CSV file: {str(e)}")
    df = None

def create_prediction_model(df, include_light=True):
    try:
        df['target'] = df.label.astype('category').cat.codes
        base_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

        if include_light:
            df['light_intensity'] = (df['temperature'] * 0.7 + (100 - df['humidity']) * 0.3)
            base_features.append('light_intensity')

        X = df[base_features]
        y = df.target

        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        model = GradientBoostingClassifier(random_state=42)
        model.fit(X_scaled, y)

        return model, scaler, base_features
    except Exception as e:
        print(f"Error in create_prediction_model: {str(e)}")
        return None, None, None

# Initialize the model
if df is not None:
    model, scaler, base_features = create_prediction_model(df)
else:
    model, scaler, base_features = None, None, None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None or scaler is None or base_features is None:
            return jsonify({'error': 'Model not properly initialized'}), 500

        # Get the data from the request
        data = request.get_json()
        print(f"Received data: {data}")  # Debug print

        # Create input dataframe
        input_data = pd.DataFrame([[
            df['N'].mean(),  # N
            df['P'].mean(),  # P
            df['K'].mean(),  # K
            float(data['temperature']),  # temperature
            float(data['humidity']),     # humidity
            df['ph'].mean(),  # ph
            float(data['rainfall']),     # rainfall
            float(data['light_intensity'])  # light_intensity
        ]], columns=base_features)

        print(f"Input data shape: {input_data.shape}")  # Debug print
        print(f"Input data columns: {input_data.columns}")  # Debug print

        # Scale the input data
        input_scaled = scaler.transform(input_data)
        print(f"Scaled input shape: {input_scaled.shape}")  # Debug print

        # Predict crop label
        predicted_label = model.predict(input_scaled)[0]
        print(f"Predicted label: {predicted_label}")  # Debug print

        # Map the label number to crop name
        crop_name = df[df['target'] == predicted_label]['label'].iloc[0]
        print(f"Crop name: {crop_name}")  # Debug print

        return jsonify({'crop': crop_name})

    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        print(traceback.format_exc())  # Print the full traceback
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
'''
def predict_crop(temp, humidity, rainfall, light_intensity=None):
    """
    Predicts crop based on given environmental parameters

    Parameters:
    temp (float): Temperature in Celsius
    humidity (float): Humidity percentage
    rainfall (float): Rainfall in mm
    light_intensity (float, optional): Light intensity value

    Returns:
    str: Predicted crop name
    """
    # Create input dataframe
    input_data = pd.DataFrame([[temp, humidity, rainfall]],
                            columns=['temperature', 'humidity', 'rainfall'])

    # Add default values for N, P, K, ph using dataset means
    input_data['N'] = df['N'].mean()
    input_data['P'] = df['P'].mean()
    input_data['K'] = df['K'].mean()
    input_data['ph'] = df['ph'].mean()

    # Add light intensity if provided, otherwise calculate it
    if light_intensity is not None:
        input_data['light_intensity'] = light_intensity
    else:
        # Calculate synthetic light intensity if not provided
        input_data['light_intensity'] = (temp * 0.7 + (100 - humidity) * 0.3)

    # Ensure columns are in the same order as training data
    input_data = input_data[base_features]

    # Scale the input data
    input_scaled = scaler.transform(input_data)

    # Predict crop label
    predicted_label = model.predict(input_scaled)[0]

    # Map the label number to crop name
    crop_name = df[df['target'] == predicted_label]['label'].iloc[0]

    return crop_name

# Initialize the model and scaler with the dataset
model, scaler, base_features = create_prediction_model(df)

# Example usage:
print("Predicted Crop (without explicit light intensity):",
    predict_crop(temp=60, humidity=40, rainfall=150))

print("Predicted Crop (with explicit light intensity):",
    predict_crop(temp=45, humidity=15, rainfall=50, light_intensity=260))'''