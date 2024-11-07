async function predictCrop() {
    // Clear previous results and errors
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    resultDiv.style.display = 'none';
    errorDiv.style.display = 'none';
    resultDiv.className = 'result-container';

    try {
        // Get input values
        const temperature = parseFloat(document.getElementById('temperature').value);
        const humidity = parseFloat(document.getElementById('humidity').value);
        const rainfall = parseFloat(document.getElementById('rainfall').value);
        const light_intensity = parseFloat(document.getElementById('light_intensity').value);

        // Validate inputs
        if (isNaN(temperature) || isNaN(humidity) || isNaN(rainfall) || isNaN(light_intensity)) {
            throw new Error('Please fill in all fields with valid numbers');
        }

        if (humidity < 0 || humidity > 100) {
            throw new Error('Humidity must be between 0 and 100');
        }

        // Prepare the request data
        const data = {
            temperature,
            humidity,
            rainfall,
            light_intensity
        };

        // Make the prediction request
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.error) {
            throw new Error(result.error);
        }

        // Display the result
        resultDiv.textContent = `Recommended Crop: ${result.crop}`;
        resultDiv.style.display = 'block';
        resultDiv.classList.add('success');
    } catch (error) {
        // Display error message
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    }
}