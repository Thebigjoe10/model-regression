"""
Solar Fish Dryer ML Backend
Real machine learning models for predicting drying rates
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global variables to store trained models
models = {
    'svr': None,
    'decision_tree': None,
    'ann': None,
    'scaler': None
}

# Training status
training_status = {
    'trained': False,
    'metrics': {}
}

def generate_sample_data(n_samples=200):
    """
    Generate synthetic training data for solar fish dryer
    This simulates real-world measurements based on physics
    """
    np.random.seed(42)

    # Environmental parameters
    temperature = np.random.uniform(20, 45, n_samples)  # °C
    humidity = np.random.uniform(30, 90, n_samples)  # %
    solar_radiation = np.random.uniform(300, 1200, n_samples)  # W/m²
    wind_speed = np.random.uniform(0, 8, n_samples)  # m/s
    initial_moisture = np.random.uniform(65, 85, n_samples)  # %
    fish_thickness = np.random.uniform(1, 5, n_samples)  # cm

    # Calculate drying rate based on physics-based relationships
    # This formula simulates real drying behavior
    drying_rate = (
        0.12 * temperature +  # Temperature effect
        0.05 * (100 - humidity) +  # Humidity effect (inverted)
        0.003 * solar_radiation +  # Solar radiation effect
        0.25 * wind_speed +  # Wind speed effect
        0.02 * initial_moisture -  # Initial moisture effect
        0.35 * fish_thickness +  # Thickness penalty
        np.random.normal(0, 0.3, n_samples)  # Random noise
    )

    # Ensure drying rates are positive and realistic
    drying_rate = np.clip(drying_rate, 0.5, 8.0)

    # Create DataFrame
    df = pd.DataFrame({
        'temperature': temperature,
        'humidity': humidity,
        'solar_radiation': solar_radiation,
        'wind_speed': wind_speed,
        'initial_moisture': initial_moisture,
        'fish_thickness': fish_thickness,
        'drying_rate': drying_rate
    })

    return df

def train_models(data_path=None):
    """
    Train all three ML models: SVR, Decision Tree, and ANN
    """
    global models, training_status

    # Load or generate data
    if data_path and os.path.exists(data_path):
        print(f"Loading data from {data_path}...")
        df = pd.read_csv(data_path)
    else:
        print("Generating sample data for training...")
        df = generate_sample_data(200)
        df.to_csv('training_data.csv', index=False)

    # Prepare features and target
    X = df[['temperature', 'humidity', 'solar_radiation', 'wind_speed',
            'initial_moisture', 'fish_thickness']].values
    y = df['drying_rate'].values

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models['scaler'] = scaler

    # Train SVR Model
    print("Training SVR model...")
    svr = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
    svr.fit(X_train_scaled, y_train)
    svr_pred = svr.predict(X_test_scaled)
    svr_rmse = np.sqrt(mean_squared_error(y_test, svr_pred))
    svr_r2 = r2_score(y_test, svr_pred)
    models['svr'] = svr

    # Train Decision Tree Model
    print("Training Decision Tree model...")
    dt = DecisionTreeRegressor(max_depth=10, min_samples_split=5, random_state=42)
    dt.fit(X_train, y_train)
    dt_pred = dt.predict(X_test)
    dt_rmse = np.sqrt(mean_squared_error(y_test, dt_pred))
    dt_r2 = r2_score(y_test, dt_pred)
    models['decision_tree'] = dt

    # Train ANN Model
    print("Training ANN model...")
    ann = MLPRegressor(
        hidden_layer_sizes=(64, 32, 16),
        activation='relu',
        solver='adam',
        max_iter=1000,
        random_state=42,
        early_stopping=True
    )
    ann.fit(X_train_scaled, y_train)
    ann_pred = ann.predict(X_test_scaled)
    ann_rmse = np.sqrt(mean_squared_error(y_test, ann_pred))
    ann_r2 = r2_score(y_test, ann_pred)
    models['ann'] = ann

    # Store training metrics
    training_status['trained'] = True
    training_status['metrics'] = {
        'svr': {'rmse': float(svr_rmse), 'r2': float(svr_r2)},
        'decision_tree': {'rmse': float(dt_rmse), 'r2': float(dt_r2)},
        'ann': {'rmse': float(ann_rmse), 'r2': float(ann_r2)},
        'samples': len(df)
    }

    # Save models
    joblib.dump(models, 'trained_models.pkl')

    print("\n=== Training Complete ===")
    print(f"SVR - RMSE: {svr_rmse:.3f}, R²: {svr_r2:.3f}")
    print(f"Decision Tree - RMSE: {dt_rmse:.3f}, R²: {dt_r2:.3f}")
    print(f"ANN - RMSE: {ann_rmse:.3f}, R²: {ann_r2:.3f}")

    return training_status['metrics']

def load_models():
    """Load pre-trained models if available"""
    global models, training_status

    if os.path.exists('trained_models.pkl'):
        models = joblib.load('trained_models.pkl')
        training_status['trained'] = True
        print("Loaded pre-trained models")
        return True
    return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_trained': training_status['trained']
    })

@app.route('/api/train', methods=['POST'])
def train():
    """Train models endpoint"""
    try:
        data = request.json
        data_path = data.get('data_path', None) if data else None

        metrics = train_models(data_path)

        return jsonify({
            'success': True,
            'message': 'Models trained successfully',
            'metrics': metrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make predictions using trained models"""
    try:
        if not training_status['trained']:
            return jsonify({
                'success': False,
                'error': 'Models not trained yet. Please train models first.'
            }), 400

        data = request.json

        # Extract input features
        features = np.array([[
            data['temperature'],
            data['humidity'],
            data['solar_radiation'],
            data['wind_speed'],
            data['initial_moisture'],
            data['fish_thickness']
        ]])

        # Scale features for SVR and ANN
        features_scaled = models['scaler'].transform(features)

        # Make predictions
        svr_prediction = float(models['svr'].predict(features_scaled)[0])
        dt_prediction = float(models['decision_tree'].predict(features)[0])
        ann_prediction = float(models['ann'].predict(features_scaled)[0])

        # Ensemble prediction (average)
        ensemble_prediction = (svr_prediction + dt_prediction + ann_prediction) / 3

        # Calculate estimated drying time
        initial_moisture = data['initial_moisture']
        target_moisture = 15  # Target moisture content (%)
        moisture_to_remove = initial_moisture - target_moisture
        estimated_time = moisture_to_remove / ensemble_prediction if ensemble_prediction > 0 else 0

        # Generate time series data
        time_series = []
        for hour in range(9):
            time_series.append({
                'hour': hour,
                'svr': max(0, initial_moisture - (svr_prediction * hour)),
                'decision_tree': max(0, initial_moisture - (dt_prediction * hour)),
                'ann': max(0, initial_moisture - (ann_prediction * hour)),
                'ensemble': max(0, initial_moisture - (ensemble_prediction * hour))
            })

        return jsonify({
            'success': True,
            'predictions': {
                'svr': svr_prediction,
                'decision_tree': dt_prediction,
                'ann': ann_prediction,
                'ensemble': ensemble_prediction
            },
            'estimated_time': estimated_time,
            'time_series': time_series
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get training metrics"""
    return jsonify({
        'success': True,
        'trained': training_status['trained'],
        'metrics': training_status.get('metrics', {})
    })

@app.route('/api/upload-data', methods=['POST'])
def upload_data():
    """Upload custom training data"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        if file and file.filename.endswith('.csv'):
            filepath = 'uploaded_data.csv'
            file.save(filepath)

            # Validate data format
            df = pd.read_csv(filepath)
            required_columns = ['temperature', 'humidity', 'solar_radiation',
                              'wind_speed', 'initial_moisture', 'fish_thickness',
                              'drying_rate']

            if not all(col in df.columns for col in required_columns):
                return jsonify({
                    'success': False,
                    'error': f'CSV must contain columns: {", ".join(required_columns)}'
                }), 400

            return jsonify({
                'success': True,
                'message': f'Data uploaded successfully. {len(df)} samples loaded.',
                'filepath': filepath
            })
        else:
            return jsonify({
                'success': False,
                'error': 'File must be a CSV'
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Try to load existing models, otherwise train new ones
    if not load_models():
        print("No pre-trained models found. Training new models...")
        train_models()

    print("\n=== Solar Fish Dryer ML Backend ===")
    print("Server starting on http://localhost:5000")
    print("API Endpoints:")
    print("  - POST /api/predict - Make predictions")
    print("  - POST /api/train - Train models")
    print("  - GET /api/metrics - Get model metrics")
    print("  - POST /api/upload-data - Upload custom data")
    print("  - GET /api/health - Health check")

    app.run(debug=True, port=5000, host='0.0.0.0')
