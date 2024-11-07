import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import os

class CropModelTrainer:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = None
        self.scaler = None
        self.label_mapping = None
        
    def load_data(self):
        df = pd.read_csv(self.data_path)
        df['target'] = df.label.astype('category').cat.codes
        self.label_mapping = dict(enumerate(df.label.astype('category').cat.categories))
        return df
        
    def prepare_features(self, df):
        df['light_intensity'] = (df['temperature'] * 0.7 + (100 - df['humidity']) * 0.3)
        base_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'light_intensity']
        return df[base_features], df['target']
        
    def train_model(self):
        df = self.load_data()
        X, y = self.prepare_features(df)
        
        self.scaler = MinMaxScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        self.model = GradientBoostingClassifier(random_state=42)
        self.model.fit(X_scaled, y)
        
    def save_model(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        joblib.dump(self.model, os.path.join(output_dir, 'model.joblib'))
        joblib.dump(self.scaler, os.path.join(output_dir, 'scaler.joblib'))
        joblib.dump(self.label_mapping, os.path.join(output_dir, 'label_mapping.joblib'))
