import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Sun, Droplets, Wind, Thermometer, Activity, Database, TrendingUp, Upload, RefreshCw, CheckCircle, AlertCircle } from 'lucide-react';

const SolarFishDryerPredictor = () => {
  const [inputData, setInputData] = useState({
    temperature: 30,
    humidity: 60,
    solar_radiation: 800,
    wind_speed: 2.5,
    initial_moisture: 75,
    fish_thickness: 2.5,
    fish_type: 'tilapia'
  });

  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState({
    connected: false,
    trained: false
  });
  const [modelMetrics, setModelMetrics] = useState(null);
  const [training, setTraining] = useState(false);

  const API_URL = 'http://localhost:5000/api';
  const fishTypes = ['tilapia', 'catfish', 'mackerel', 'sardine', 'salmon'];

  // Check backend health on component mount
  useEffect(() => {
    checkBackendHealth();
    fetchModelMetrics();
  }, []);

  const checkBackendHealth = async () => {
    try {
      const response = await fetch(`${API_URL}/health`);
      const data = await response.json();
      setBackendStatus({
        connected: true,
        trained: data.models_trained
      });
    } catch (error) {
      console.error('Backend not connected:', error);
      setBackendStatus({
        connected: false,
        trained: false
      });
    }
  };

  const fetchModelMetrics = async () => {
    try {
      const response = await fetch(`${API_URL}/metrics`);
      const data = await response.json();
      if (data.success && data.trained) {
        setModelMetrics(data.metrics);
      }
    } catch (error) {
      console.error('Error fetching metrics:', error);
    }
  };

  const trainModels = async () => {
    setTraining(true);
    try {
      const response = await fetch(`${API_URL}/train`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
      });

      const data = await response.json();

      if (data.success) {
        setModelMetrics(data.metrics);
        setBackendStatus(prev => ({ ...prev, trained: true }));
        alert('Models trained successfully!');
      } else {
        alert('Training failed: ' + data.error);
      }
    } catch (error) {
      console.error('Training error:', error);
      alert('Failed to train models. Make sure the backend is running.');
    } finally {
      setTraining(false);
    }
  };

  const predictDryingRate = async () => {
    if (!backendStatus.connected) {
      alert('Backend is not connected. Please start the Python backend server.');
      return;
    }

    if (!backendStatus.trained) {
      alert('Models are not trained yet. Please train the models first.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputData)
      });

      const data = await response.json();

      if (data.success) {
        setPredictions({
          svr: data.predictions.svr,
          decisionTree: data.predictions.decision_tree,
          ann: data.predictions.ann,
          ensemble: data.predictions.ensemble,
          timeSeries: data.time_series,
          estimatedTime: data.estimated_time.toFixed(1)
        });
      } else {
        alert('Prediction failed: ' + data.error);
      }
    } catch (error) {
      console.error('Prediction error:', error);
      alert('Failed to get predictions. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setInputData(prev => ({
      ...prev,
      [field]: parseFloat(value) || value
    }));
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/upload-data`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (data.success) {
        alert(data.message);
      } else {
        alert('Upload failed: ' + data.error);
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Failed to upload data.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <Sun className="w-10 h-10 text-orange-500" />
                <h1 className="text-3xl font-bold text-gray-800">Solar Fish Dryer ML System</h1>
              </div>
              <p className="text-gray-600">Real Machine Learning with SVR, Decision Trees & Neural Networks</p>
            </div>

            {/* Backend Status */}
            <div className="flex gap-4">
              <div className={`flex items-center gap-2 px-4 py-2 rounded-lg ${backendStatus.connected ? 'bg-green-100' : 'bg-red-100'}`}>
                {backendStatus.connected ? (
                  <CheckCircle className="w-5 h-5 text-green-600" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-red-600" />
                )}
                <span className={`font-medium ${backendStatus.connected ? 'text-green-800' : 'text-red-800'}`}>
                  Backend {backendStatus.connected ? 'Connected' : 'Disconnected'}
                </span>
              </div>

              <div className={`flex items-center gap-2 px-4 py-2 rounded-lg ${backendStatus.trained ? 'bg-blue-100' : 'bg-yellow-100'}`}>
                {backendStatus.trained ? (
                  <CheckCircle className="w-5 h-5 text-blue-600" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-yellow-600" />
                )}
                <span className={`font-medium ${backendStatus.trained ? 'text-blue-800' : 'text-yellow-800'}`}>
                  Models {backendStatus.trained ? 'Trained' : 'Not Trained'}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Model Training Section */}
        {backendStatus.connected && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Model Training & Data</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <button
                  onClick={trainModels}
                  disabled={training}
                  className="w-full bg-blue-500 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {training ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                      Training Models...
                    </>
                  ) : (
                    <>
                      <RefreshCw className="w-5 h-5" />
                      Train / Retrain Models
                    </>
                  )}
                </button>
                <p className="text-sm text-gray-600 mt-2">Train models using sample data or uploaded data</p>
              </div>

              <div>
                <label className="w-full bg-green-500 text-white font-bold py-3 px-4 rounded-lg hover:bg-green-600 transition-all flex items-center justify-center gap-2 cursor-pointer">
                  <Upload className="w-5 h-5" />
                  Upload Your Data (CSV)
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                </label>
                <p className="text-sm text-gray-600 mt-2">Upload CSV with your collected data</p>
              </div>
            </div>

            {/* Model Metrics */}
            {modelMetrics && (
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold text-gray-800 mb-3">Model Performance Metrics</h3>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <div className="text-sm text-gray-600">SVR</div>
                    <div className="font-mono text-sm">RMSE: {modelMetrics.svr.rmse.toFixed(3)}</div>
                    <div className="font-mono text-sm">R²: {modelMetrics.svr.r2.toFixed(3)}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">Decision Tree</div>
                    <div className="font-mono text-sm">RMSE: {modelMetrics.decision_tree.rmse.toFixed(3)}</div>
                    <div className="font-mono text-sm">R²: {modelMetrics.decision_tree.r2.toFixed(3)}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">ANN</div>
                    <div className="font-mono text-sm">RMSE: {modelMetrics.ann.rmse.toFixed(3)}</div>
                    <div className="font-mono text-sm">R²: {modelMetrics.ann.r2.toFixed(3)}</div>
                  </div>
                </div>
                <div className="mt-2 text-sm text-gray-600">
                  Trained on {modelMetrics.samples} samples
                </div>
              </div>
            )}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Input Panel */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Database className="w-5 h-5" />
                Input Parameters
              </h2>

              <div className="space-y-4">
                {/* Temperature */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                    <Thermometer className="w-4 h-4 text-red-500" />
                    Temperature (°C)
                  </label>
                  <input
                    type="range"
                    min="20"
                    max="45"
                    step="0.5"
                    value={inputData.temperature}
                    onChange={(e) => handleInputChange('temperature', e.target.value)}
                    className="w-full"
                  />
                  <div className="text-right text-sm font-semibold text-gray-600">{inputData.temperature}°C</div>
                </div>

                {/* Humidity */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                    <Droplets className="w-4 h-4 text-blue-500" />
                    Relative Humidity (%)
                  </label>
                  <input
                    type="range"
                    min="30"
                    max="90"
                    step="1"
                    value={inputData.humidity}
                    onChange={(e) => handleInputChange('humidity', e.target.value)}
                    className="w-full"
                  />
                  <div className="text-right text-sm font-semibold text-gray-600">{inputData.humidity}%</div>
                </div>

                {/* Solar Radiation */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                    <Sun className="w-4 h-4 text-yellow-500" />
                    Solar Radiation (W/m²)
                  </label>
                  <input
                    type="range"
                    min="300"
                    max="1200"
                    step="50"
                    value={inputData.solar_radiation}
                    onChange={(e) => handleInputChange('solar_radiation', e.target.value)}
                    className="w-full"
                  />
                  <div className="text-right text-sm font-semibold text-gray-600">{inputData.solar_radiation} W/m²</div>
                </div>

                {/* Wind Speed */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                    <Wind className="w-4 h-4 text-cyan-500" />
                    Wind Speed (m/s)
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="8"
                    step="0.5"
                    value={inputData.wind_speed}
                    onChange={(e) => handleInputChange('wind_speed', e.target.value)}
                    className="w-full"
                  />
                  <div className="text-right text-sm font-semibold text-gray-600">{inputData.wind_speed} m/s</div>
                </div>

                {/* Initial Moisture */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                    <Activity className="w-4 h-4 text-green-500" />
                    Initial Moisture Content (%)
                  </label>
                  <input
                    type="range"
                    min="60"
                    max="85"
                    step="1"
                    value={inputData.initial_moisture}
                    onChange={(e) => handleInputChange('initial_moisture', e.target.value)}
                    className="w-full"
                  />
                  <div className="text-right text-sm font-semibold text-gray-600">{inputData.initial_moisture}%</div>
                </div>

                {/* Fish Thickness */}
                <div>
                  <label className="text-sm font-medium text-gray-700 mb-2 block">
                    Fish Thickness (cm)
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="5"
                    step="0.5"
                    value={inputData.fish_thickness}
                    onChange={(e) => handleInputChange('fish_thickness', e.target.value)}
                    className="w-full"
                  />
                  <div className="text-right text-sm font-semibold text-gray-600">{inputData.fish_thickness} cm</div>
                </div>

                {/* Fish Type */}
                <div>
                  <label className="text-sm font-medium text-gray-700 mb-2 block">
                    Fish Type
                  </label>
                  <select
                    value={inputData.fish_type}
                    onChange={(e) => handleInputChange('fish_type', e.target.value)}
                    className="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-blue-500"
                  >
                    {fishTypes.map(type => (
                      <option key={type} value={type}>
                        {type.charAt(0).toUpperCase() + type.slice(1)}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Predict Button */}
                <button
                  onClick={predictDryingRate}
                  disabled={loading || !backendStatus.trained}
                  className="w-full bg-gradient-to-r from-blue-500 to-orange-500 text-white font-bold py-3 px-4 rounded-lg hover:from-blue-600 hover:to-orange-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                      Predicting...
                    </>
                  ) : (
                    <>
                      <TrendingUp className="w-5 h-5" />
                      Predict Drying Rate
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2 space-y-6">
            {predictions ? (
              <>
                {/* Model Predictions */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h2 className="text-xl font-bold text-gray-800 mb-4">Real ML Model Predictions</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">SVR Model</div>
                      <div className="text-2xl font-bold text-purple-700">{predictions.svr.toFixed(2)}</div>
                      <div className="text-xs text-gray-500">%/hour</div>
                    </div>
                    <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">Decision Tree</div>
                      <div className="text-2xl font-bold text-green-700">{predictions.decisionTree.toFixed(2)}</div>
                      <div className="text-xs text-gray-500">%/hour</div>
                    </div>
                    <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">ANN Model</div>
                      <div className="text-2xl font-bold text-blue-700">{predictions.ann.toFixed(2)}</div>
                      <div className="text-xs text-gray-500">%/hour</div>
                    </div>
                    <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-4 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">Ensemble</div>
                      <div className="text-2xl font-bold text-orange-700">{predictions.ensemble.toFixed(2)}</div>
                      <div className="text-xs text-gray-500">%/hour</div>
                    </div>
                  </div>

                  <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">Estimated Drying Time (to 15% moisture)</div>
                    <div className="text-3xl font-bold text-blue-700">{predictions.estimatedTime} hours</div>
                  </div>
                </div>

                {/* Model Comparison Chart */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h2 className="text-xl font-bold text-gray-800 mb-4">Model Comparison</h2>
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={[
                      { name: 'SVR', rate: predictions.svr },
                      { name: 'Decision Tree', rate: predictions.decisionTree },
                      { name: 'ANN', rate: predictions.ann },
                      { name: 'Ensemble', rate: predictions.ensemble }
                    ]}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis label={{ value: 'Drying Rate (%/hour)', angle: -90, position: 'insideLeft' }} />
                      <Tooltip />
                      <Bar dataKey="rate" fill="#3b82f6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* Time Series Prediction */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h2 className="text-xl font-bold text-gray-800 mb-4">Moisture Content Over Time</h2>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={predictions.timeSeries}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis
                        dataKey="hour"
                        label={{ value: 'Time (hours)', position: 'insideBottom', offset: -5 }}
                      />
                      <YAxis
                        label={{ value: 'Moisture Content (%)', angle: -90, position: 'insideLeft' }}
                      />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="svr" stroke="#9333ea" name="SVR" strokeWidth={2} />
                      <Line type="monotone" dataKey="decision_tree" stroke="#22c55e" name="Decision Tree" strokeWidth={2} />
                      <Line type="monotone" dataKey="ann" stroke="#3b82f6" name="ANN" strokeWidth={2} />
                      <Line type="monotone" dataKey="ensemble" stroke="#f97316" name="Ensemble" strokeWidth={3} strokeDasharray="5 5" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>

                {/* Recommendations */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h2 className="text-xl font-bold text-gray-800 mb-4">Recommendations</h2>
                  <div className="space-y-3">
                    {predictions.ensemble > 5 && (
                      <div className="p-3 bg-green-50 border-l-4 border-green-500 text-green-800">
                        <strong>Excellent Conditions:</strong> High drying rate expected. Monitor regularly to prevent over-drying.
                      </div>
                    )}
                    {predictions.ensemble >= 3 && predictions.ensemble <= 5 && (
                      <div className="p-3 bg-blue-50 border-l-4 border-blue-500 text-blue-800">
                        <strong>Good Conditions:</strong> Moderate drying rate. Continue monitoring environmental parameters.
                      </div>
                    )}
                    {predictions.ensemble < 3 && (
                      <div className="p-3 bg-yellow-50 border-l-4 border-yellow-500 text-yellow-800">
                        <strong>Suboptimal Conditions:</strong> Low drying rate. Consider improving ventilation or waiting for better weather.
                      </div>
                    )}
                  </div>
                </div>
              </>
            ) : (
              <div className="bg-white rounded-lg shadow-lg p-12 text-center">
                <TrendingUp className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-600 mb-2">No Predictions Yet</h3>
                <p className="text-gray-500">
                  {!backendStatus.connected
                    ? 'Start the Python backend server first'
                    : !backendStatus.trained
                    ? 'Train the models first, then enter parameters and predict'
                    : 'Enter your environmental parameters and click "Predict Drying Rate"'
                  }
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 bg-white rounded-lg shadow-lg p-4 text-center text-sm text-gray-600">
          <p>Solar Fish Dryer ML System | Real ML Models: Support Vector Regression, Decision Trees, Artificial Neural Networks</p>
        </div>
      </div>
    </div>
  );
};

export default SolarFishDryerPredictor;
