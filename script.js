async function loadPyodideAndModel() {
    const pyodide = await loadPyodide();
    await pyodide.loadPackage(['pandas', 'scikit-learn']);

    const response = await fetch('ML_model.py');
    const code = await response.text();
    await pyodide.runPython(code);

    // Fetch CSV data
    const csvResponse = await fetch('C:\Users\Megha\OneDrive\Desktop\crop prediction\crop-prediction-model\Crop_recommendation.csv');
    const csvData = await csvResponse.text();

    // Load CSV data in Pyodide
    pyodide.runPython(`
        from ML_model import load_data, create_prediction_model
        df = load_data("""${csvData}""")
        model, scaler, base_features = create_prediction_model(df)
    `);

    return pyodide;
}

document.getElementById('inputForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const humidity = parseFloat(document.getElementById('humidity').value);
    const temperature = parseFloat(document.getElementById('temperature').value);
    const rainfall = parseFloat(document.getElementById('rainfall').value);
    const lightIntensity = parseFloat(document.getElementById('lightIntensity').value);

    if (pyodideInstance) {
        const pythonCode = `
            from ML_model import predict_crop
            predict_crop(model, scaler, base_features, temp=${temperature}, humidity=${humidity}, rainfall=${rainfall}, light_intensity=${lightIntensity})
        `;

        try {
            const cropRecommendation = pyodideInstance.runPython(pythonCode);
            document.getElementById('predictionResult').innerText = `Recommended Crop: ${cropRecommendation}`;
            document.getElementById('outputContainer').style.display = 'block';
        } catch (error) {
            console.error("Prediction error:", error);
            document.getElementById('predictionResult').innerText = "An error occurred while predicting the crop.";
            document.getElementById('outputContainer').style.display = 'block';
        }
    } else {
        document.getElementById('predictionResult').innerText = "Loading model. Please try again shortly.";
        document.getElementById('outputContainer').style.display = 'block';
    }
});
