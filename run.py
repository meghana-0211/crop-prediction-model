from model.train import CropModelTrainer
from api.app import app

def train_and_save_model():
    trainer = CropModelTrainer('Crop_recommendation.csv')
    trainer.train_model()
    trainer.save_model('model/saved_models')

if __name__ == '__main__':

    
    # Run the Flask app
    app.run(debug=True)