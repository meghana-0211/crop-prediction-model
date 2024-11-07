import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Loader2 } from 'lucide-react';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';

const CropRecommender = () => {
  const [formData, setFormData] = useState({
    temperature: '',
    humidity: '',
    rainfall: '',
    light_intensity: ''
  });
  
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          temperature: parseFloat(formData.temperature),
          humidity: parseFloat(formData.humidity),
          rainfall: parseFloat(formData.rainfall),
          light_intensity: parseFloat(formData.light_intensity)
        }),
      });

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      setPrediction(data.crop);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">Crop Recommendation System</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Temperature (°C)</label>
                <Input
                  type="number"
                  name="temperature"
                  value={formData.temperature}
                  onChange={handleInputChange}
                  placeholder="Enter temperature"
                  required
                  step="0.1"
                  className="w-full"
                />
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium">Humidity (%)</label>
                <Input
                  type="number"
                  name="humidity"
                  value={formData.humidity}
                  onChange={handleInputChange}
                  placeholder="Enter humidity"
                  required
                  min="0"
                  max="100"
                  className="w-full"
                />
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium">Rainfall (mm)</label>
                <Input
                  type="number"
                  name="rainfall"
                  value={formData.rainfall}
                  onChange={handleInputChange}
                  placeholder="Enter rainfall"
                  required
                  min="0"
                  className="w-full"
                />
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium">Light Intensity</label>
                <Input
                  type="number"
                  name="light_intensity"
                  value={formData.light_intensity}
                  onChange={handleInputChange}
                  placeholder="Enter light intensity"
                  required
                  className="w-full"
                />
              </div>
            </div>

            <Button 
              type="submit" 
              className="w-full"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Predicting...
                </>
              ) : (
                'Get Crop Recommendation'
              )}
            </Button>
          </form>

          {prediction && (
            <Alert className="mt-4 bg-green-50">
              <AlertTitle>Recommended Crop</AlertTitle>
              <AlertDescription className="text-lg font-semibold">
                {prediction}
              </AlertDescription>
            </Alert>
          )}

          {error && (
            <Alert className="mt-4 bg-red-50" variant="destructive">
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default CropRecommender;