# 🌾 Intelligent Crop Recommendation System

An advanced machine learning system that recommends suitable crops based on environmental conditions and soil composition. This project uses gradient boosting to achieve high accuracy (99.95%) in crop predictions.

## 📊 Overview

This system helps farmers make data-driven decisions about crop selection by analyzing:
- Environmental parameters (temperature, humidity, rainfall)
- Soil composition (N, P, K values, pH)
- Light intensity (optional)

## 🎯 Features

- **High Accuracy**: Achieves 99.95% accuracy using Gradient Boosting
- **Multiple Input Parameters**: Considers 7-8 different parameters for prediction
- **Flexible Light Intensity**: Works with or without light intensity measurements
- **Easy Integration**: Simple API for making predictions
- **Scalable**: Can be retrained with different datasets

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/crop-recommendation.git

# Navigate to project directory
cd crop-recommendation

# Install required packages
pip install -r requirements.txt
```

## 📋 Dependencies

```
pandas>=1.3.0
numpy>=1.19.5
scikit-learn>=0.24.2
```

## 💻 Usage

### Basic Usage

```python
# Import necessary modules
from crop_predictor import load_and_prepare_dataset, create_prediction_model, predict_crop

# Load dataset
df = load_and_prepare_dataset('Crop_recommendation.csv')

# Create and train model
model, scaler, base_features = create_prediction_model(df)

# Make prediction
prediction = predict_crop(
    df=df,
    model=model,
    scaler=scaler,
    base_features=base_features,
    temp=25,
    humidity=80,
    rainfall=100
)

print(f"Recommended crop: {prediction}")
```

### With Light Intensity

```python
prediction = predict_crop(
    df=df,
    model=model,
    scaler=scaler,
    base_features=base_features,
    temp=25,
    humidity=80,
    rainfall=100,
    light_intensity=750
)
```

## 📊 Dataset Format

Your dataset should be a CSV file with the following columns:

| Column      | Description                        | Unit                |
|-------------|------------------------------------|---------------------|
| N           | Ratio of Nitrogen                  | mg/kg              |
| P           | Ratio of Phosphorous               | mg/kg              |
| K           | Ratio of Potassium                 | mg/kg              |
| temperature | Temperature                        | °C                 |
| humidity    | Relative Humidity                  | %                  |
| ph          | pH value of soil                   | pH                 |
| rainfall    | Amount of rainfall                 | mm                 |
| label       | Name of crop                       | text               |

## 🧪 Model Performance

The model has been tested extensively with the following results:

- Accuracy: 99.95%
- Method: Gradient Boosting Classifier
- Cross-validation: Performed with 4-fold validation

## 🔄 Model Pipeline

1. Data Loading and Validation
2. Feature Scaling using MinMaxScaler
3. Synthetic Light Intensity Calculation (if not provided)
4. Gradient Boosting Classification
5. Label Mapping and Prediction

## 📈 Future Improvements

- [ ] Add support for seasonal predictions
- [ ] Incorporate weather forecast data
- [ ] Add soil type classification
- [ ] Develop web interface
- [ ] Add crop yield predictions
- [ ] Include economic factors in recommendations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

- Dataset source: [Kaggle Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
- Original research papers and methodologies
- Contributing developers and data scientists

---
⭐️ Star this repo if you find it helpful!
