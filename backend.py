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
import pickle
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables for models and scaler
models = {
    'svr': None,
    'decision_tree': None,
    'ann': None
}
scaler = StandardScaler()
feature_columns = ['temperature', 'humidity', 'solar_radiation', 'wind_speed', 
                   'initial_moisture', 'fish_thickness', 'fish_type_encoded']
model_metrics = {}
trained = False

# Fish type encoding
fish_type_mapping = {
    'tilapia': 0,
    'catfish': 1,
    'mackerel': 2,
    'sardine': 3,
    'salmon': 4
}

def generate_sample_data(n_samples=200):
    """Generate realistic sample data for training"""
    np.random.seed(42)
    
    data = {
        'temperature': np.random.uniform(20, 45, n_samples),
        'humidity': np.random.uniform(30, 90, n_samples),
        'solar_radiation': np.random.uniform(300, 1200, n_samples),
        'wind_speed': np.random.uniform(0, 8, n_samples),
        'initial_moisture': np.random.uniform(60, 85, n_samples),
        'fish_thickness': np.random.uniform(1, 5, n_samples),
        'fish_type_encoded': np.random.randint(0, 5, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Generate realistic drying rate based on physics-informed formula
    df['drying_rate'] = (
        0.08 * df['temperature'] +
        -0.03 * df['humidity'] +
        0.002 * df['solar_radiation'] +
        0.3 * df['wind_speed'] +
        -0.05 * df['initial_moisture'] +
        -0.4 * df['fish_thickness'] +
        0.2 * df['fish_type_encoded'] +
        np.random.normal(0, 0.3, n_samples)  # Add some noise
    )
    
    # Ensure drying rate is positive
    df['drying_rate'] = df['drying_rate'].clip(lower=0.5)
    
    return df

def train_models_func(data=None):
    """Train all ML models"""
    global models, scaler, model_metrics, trained
    
    if data is None:
        print("Generating sample data for training...")
        data = generate_sample_data()
    
    X = data[feature_columns]
    y = data['drying_rate']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train SVR
    print("Training SVR model...")
    models['svr'] = SVR(kernel='rbf', C=100, gamma='scale', epsilon=0.1)
    models['svr'].fit(X_train_scaled, y_train)
    svr_pred = models['svr'].predict(X_test_scaled)
    
    # Train Decision Tree
    print("Training Decision Tree model...")
    models['decision_tree'] = DecisionTreeRegressor(max_depth=10, min_samples_split=5, random_state=42)
    models['decision_tree'].fit(X_train_scaled, y_train)
    dt_pred = models['decision_tree'].predict(X_test_scaled)
    
    # Train ANN
    print("Training ANN model...")
    models['ann'] = MLPRegressor(
        hidden_layer_sizes=(64, 32, 16),
        activation='relu',
        solver='adam',
        max_iter=1000,
        random_state=42,
        early_stopping=True
    )
    models['ann'].fit(X_train_scaled, y_train)
    ann_pred = models['ann'].predict(X_test_scaled)
    
    # Calculate metrics
    model_metrics = {
        'svr': {
            'rmse': float(np.sqrt(mean_squared_error(y_test, svr_pred))),
            'r2': float(r2_score(y_test, svr_pred))
        },
        'decision_tree': {
            'rmse': float(np.sqrt(mean_squared_error(y_test, dt_pred))),
            'r2': float(r2_score(y_test, dt_pred))
        },
        'ann': {
            'rmse': float(np.sqrt(mean_squared_error(y_test, ann_pred))),
            'r2': float(r2_score(y_test, ann_pred))
        },
        'samples': len(data)
    }
    
    trained = True
    
    # Save models
    save_models()
    
    print("\n=== Training Complete ===")
    print(f"SVR - RMSE: {model_metrics['svr']['rmse']:.3f}, R²: {model_metrics['svr']['r2']:.3f}")
    print(f"Decision Tree - RMSE: {model_metrics['decision_tree']['rmse']:.3f}, R²: {model_metrics['decision_tree']['r2']:.3f}")
    print(f"ANN - RMSE: {model_metrics['ann']['rmse']:.3f}, R²: {model_metrics['ann']['r2']:.3f}")
    
    return model_metrics

def save_models():
    """Save trained models to disk"""
    os.makedirs('trained_models', exist_ok=True)
    
    with open('trained_models/svr_model.pkl', 'wb') as f:
        pickle.dump(models['svr'], f)
    with open('trained_models/dt_model.pkl', 'wb') as f:
        pickle.dump(models['decision_tree'], f)
    with open('trained_models/ann_model.pkl', 'wb') as f:
        pickle.dump(models['ann'], f)
    with open('trained_models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    with open('trained_models/metrics.pkl', 'wb') as f:
        pickle.dump(model_metrics, f)

def load_models():
    """Load pre-trained models from disk"""
    global models, scaler, model_metrics, trained
    
    try:
        with open('trained_models/svr_model.pkl', 'rb') as f:
            models['svr'] = pickle.load(f)
        with open('trained_models/dt_model.pkl', 'rb') as f:
            models['decision_tree'] = pickle.load(f)
        with open('trained_models/ann_model.pkl', 'rb') as f:
            models['ann'] = pickle.load(f)
        with open('trained_models/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('trained_models/metrics.pkl', 'rb') as f:
            model_metrics = pickle.load(f)
        
        trained = True
        print("Loaded pre-trained models")
        return True
    except FileNotFoundError:
        print("No pre-trained models found. Training new models...")
        return False

def predict_time_series(initial_data, drying_rate):
    """Generate time series prediction of moisture content"""
    time_series = []
    current_moisture = initial_data['initial_moisture']
    hour = 0
    
    while current_moisture > 15 and hour < 50:  # Stop at 15% moisture or 50 hours
        time_series.append({
            'hour': hour,
            'moisture': current_moisture
        })
        current_moisture -= drying_rate
        hour += 1
    
    # Add final point at 15%
    time_series.append({
        'hour': hour,
        'moisture': max(current_moisture, 15)
    })
    
    return time_series

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_trained': trained
    })

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get model performance metrics"""
    if not trained:
        return jsonify({
            'success': False,
            'trained': False,
            'message': 'Models not trained yet'
        })
    
    return jsonify({
        'success': True,
        'trained': True,
        'metrics': model_metrics
    })

@app.route('/api/train', methods=['POST'])
def train_models_endpoint():
    """Train or retrain models"""
    try:
        metrics = train_models_func()
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
    if not trained:
        return jsonify({
            'success': False,
            'error': 'Models not trained yet. Please train models first.'
        }), 400
    
    try:
        data = request.json
        
        # Encode fish type
        fish_type_encoded = fish_type_mapping.get(data['fish_type'], 0)
        
        # Prepare input features
        input_features = np.array([[
            data['temperature'],
            data['humidity'],
            data['solar_radiation'],
            data['wind_speed'],
            data['initial_moisture'],
            data['fish_thickness'],
            fish_type_encoded
        ]])
        
        # Scale features
        input_scaled = scaler.transform(input_features)
        
        # Make predictions with each model
        svr_pred = float(models['svr'].predict(input_scaled)[0])
        dt_pred = float(models['decision_tree'].predict(input_scaled)[0])
        ann_pred = float(models['ann'].predict(input_scaled)[0])
        
        # Ensemble prediction (weighted average)
        ensemble_pred = (0.5 * svr_pred + 0.3 * dt_pred + 0.2 * ann_pred)
        
        # Generate time series for each model
        svr_series = predict_time_series(data, svr_pred)
        dt_series = predict_time_series(data, dt_pred)
        ann_series = predict_time_series(data, ann_pred)
        ensemble_series = predict_time_series(data, ensemble_pred)
        
        # Combine time series
        time_series = []
        max_length = max(len(svr_series), len(dt_series), len(ann_series), len(ensemble_series))
        
        for i in range(max_length):
            point = {'hour': i}
            
            if i < len(svr_series):
                point['svr'] = svr_series[i]['moisture']
            if i < len(dt_series):
                point['decision_tree'] = dt_series[i]['moisture']
            if i < len(ann_series):
                point['ann'] = ann_series[i]['moisture']
            if i < len(ensemble_series):
                point['ensemble'] = ensemble_series[i]['moisture']
            
            time_series.append(point)
        
        # Calculate estimated time to reach 15% moisture
        estimated_time = (data['initial_moisture'] - 15) / ensemble_pred if ensemble_pred > 0 else 999
        
        return jsonify({
            'success': True,
            'predictions': {
                'svr': svr_pred,
                'decision_tree': dt_pred,
                'ann': ann_pred,
                'ensemble': ensemble_pred
            },
            'time_series': time_series,
            'estimated_time': estimated_time
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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
        
        # Read CSV
        df = pd.read_csv(file)
        
        # Validate required columns
        required_cols = feature_columns + ['drying_rate']
        if not all(col in df.columns for col in required_cols):
            return jsonify({
                'success': False,
                'error': f'CSV must contain columns: {", ".join(required_cols)}'
            }), 400
        
        # Save the uploaded data
        os.makedirs('uploaded_data', exist_ok=True)
        df.to_csv('uploaded_data/custom_data.csv', index=False)
        
        return jsonify({
            'success': True,
            'message': f'Successfully uploaded {len(df)} samples. You can now retrain the models.'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Initialize models on startup (for production deployment)
if not load_models():
    print("No pre-trained models found. Training new models...")
    train_models_func()

if __name__ == '__main__':
    # Get port from environment variable (for production) or use 5000 (for local)
    port = int(os.environ.get('PORT', 5000))

    # Determine if running in production
    is_production = os.environ.get('FLASK_ENV') == 'production'

    print("\n=== Solar Fish Dryer ML Backend ===")
    print(f"Environment: {'Production' if is_production else 'Development'}")
    print(f"Server starting on port {port}")
    print("API Endpoints:")
    print("  - POST /api/predict - Make predictions")
    print("  - POST /api/train - Train models")
    print("  - GET /api/metrics - Get model metrics")
    print("  - POST /api/upload-data - Upload custom data")
    print("  - GET /api/health - Health check")

    app.run(debug=not is_production, port=port, host='0.0.0.0')
