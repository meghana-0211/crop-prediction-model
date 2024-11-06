import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingClassifier

def load_data(csv_data):
    """
    Loads the CSV data from a string.
    """
    from io import StringIO
    df = pd.read_csv(StringIO(csv_data))
    return df

def create_prediction_model(df, include_light=True):
    """
    Creates and trains the prediction model with the option to include light intensity
    """
    # Prepare data
    df['target'] = df.label.astype('category').cat.codes
    base_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

    # Add synthetic light intensity feature if requested
    if include_light:
        # Create synthetic light intensity based on temperature and humidity
        # This is a simplified approximation for demonstration
        df['light_intensity'] = (df['temperature'] * 0.7 + (100 - df['humidity']) * 0.3)
        base_features.append('light_intensity')

    X = df[base_features]
    y = df.target

    # Initialize and fit scaler and model
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    model = GradientBoostingClassifier()
    model.fit(X_scaled, y)

    return model, scaler, base_features

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
'''
# Initialize the model and scaler with the dataset
model, scaler, base_features = create_prediction_model(df)

# Example usage:
print("Predicted Crop (without explicit light intensity):",
    predict_crop(temp=60, humidity=40, rainfall=150))

print("Predicted Crop (with explicit light intensity):",
    predict_crop(temp=45, humidity=15, rainfall=50, light_intensity=260))
    '''