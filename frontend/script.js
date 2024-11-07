document.getElementById('cropForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const loader = document.getElementById('loader');
    const outputContainer = document.getElementById('outputContainer');
    const errorMessage = document.getElementById('errorMessage');
    
    loader.style.display = 'block';
    outputContainer.style.display = 'none';
    errorMessage.style.display = 'none';

    const formData = {
        temperature: parseFloat(document.getElementById('temperature').value),
        humidity: parseFloat(document.getElementById('humidity').value),
        rainfall: parseFloat(document.getElementById('rainfall').value),
        light_intensity: parseFloat(document.getElementById('light_intensity').value)
    };

    try {
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Prediction failed');
        }

        document.getElementById('result').textContent = data.crop;
        outputContainer.style.display = 'block';
    } catch (error) {
        errorMessage.textContent = error.message || 'An error occurred while making the prediction. Please try again.';
        errorMessage.style.display = 'block';
    } finally {
        loader.style.display = 'none';
    }
});