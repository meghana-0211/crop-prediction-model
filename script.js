// Load Pyodide and set up the ML model
async function loadPyodideAndModel() {
    const pyodide = await loadPyodide();
    await pyodide.loadPackage(['pandas', 'scikit-learn']);
    
    // Load and execute ML model code from 'ML_model.py'
    const response = await fetch('ML_model.py');
    const code = await response.text();
    pyodide.runPython(code);

    return pyodide;
}

let pyodideInstance;
loadPyodideAndModel().then(instance => {
    pyodideInstance = instance;
});

document.getElementById('inputForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Retrieve user inputs
    const humidity = parseFloat(document.getElementById('humidity').value);
    const temperature = parseFloat(document.getElementById('temperature').value);
    const rainfall = parseFloat(document.getElementById('rainfall').value);
    const lightIntensity = parseFloat(document.getElementById('lightIntensity').value);

    if (pyodideInstance) {
        // Pass inputs to Python function and get prediction
        const pythonCode = `
            predict_crop(temp=${temperature}, humidity=${humidity}, rainfall=${rainfall}, light_intensity=${lightIntensity})
        `;
        
        // Get prediction result
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
