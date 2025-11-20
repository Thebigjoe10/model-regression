# Solar Fish Dryer ML System

A complete machine learning system for predicting drying rates in solar fish dryers. Uses real ML models (Support Vector Regression, Decision Trees, and Artificial Neural Networks) to provide accurate predictions based on environmental conditions.

## Features

- **Real Machine Learning Models**
  - Support Vector Regression (SVR)
  - Decision Tree Regressor
  - Artificial Neural Network (ANN)
  - Ensemble predictions combining all models

- **Full-Stack Application**
  - Python Flask backend with REST API
  - React frontend with interactive visualizations
  - Real-time predictions and model training
  - Data upload and management

- **Professional ML Features**
  - Model performance metrics (RMSE, R²)
  - Time-series forecasting
  - Interactive parameter controls
  - Beautiful charts and visualizations

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Backend

**Option A: Automatic (Recommended)**

Mac/Linux:
```bash
./start_backend.sh
```

Windows:
```
start_backend.bat
```

**Option B: Manual**

```bash
python backend.py
```

### 3. Open Frontend

Open `frontend.jsx` in a new Claude.ai conversation or paste it into a React environment.

The frontend will automatically connect to the backend at `http://localhost:5000`.

## System Architecture

```
┌─────────────────┐         HTTP/JSON         ┌─────────────────┐
│                 │ ◄─────────────────────────► │                 │
│  React Frontend │                             │  Flask Backend  │
│  (frontend.jsx) │                             │  (backend.py)   │
│                 │                             │                 │
└─────────────────┘                             └────────┬────────┘
                                                         │
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │   ML Models     │
                                                │  - SVR          │
                                                │  - Decision Tree│
                                                │  - ANN          │
                                                └─────────────────┘
```

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "models_trained": true
}
```

#### 2. Train Models
```http
POST /api/train
```

**Request Body (Optional):**
```json
{
  "data_path": "path/to/custom_data.csv"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Models trained successfully",
  "metrics": {
    "svr": {"rmse": 0.321, "r2": 0.945},
    "decision_tree": {"rmse": 0.298, "r2": 0.952},
    "ann": {"rmse": 0.287, "r2": 0.958},
    "samples": 200
  }
}
```

#### 3. Make Prediction
```http
POST /api/predict
```

**Request Body:**
```json
{
  "temperature": 32.5,
  "humidity": 55,
  "solar_radiation": 850,
  "wind_speed": 3.2,
  "initial_moisture": 78,
  "fish_thickness": 2.0
}
```

**Response:**
```json
{
  "success": true,
  "predictions": {
    "svr": 5.24,
    "decision_tree": 5.18,
    "ann": 5.31,
    "ensemble": 5.24
  },
  "estimated_time": 12.0,
  "time_series": [
    {"hour": 0, "svr": 78, "decision_tree": 78, "ann": 78, "ensemble": 78},
    {"hour": 1, "svr": 72.76, ...},
    ...
  ]
}
```

#### 4. Get Model Metrics
```http
GET /api/metrics
```

**Response:**
```json
{
  "success": true,
  "trained": true,
  "metrics": {
    "svr": {"rmse": 0.321, "r2": 0.945},
    "decision_tree": {"rmse": 0.298, "r2": 0.952},
    "ann": {"rmse": 0.287, "r2": 0.958},
    "samples": 200
  }
}
```

#### 5. Upload Data
```http
POST /api/upload-data
```

**Content-Type:** `multipart/form-data`

**Form Data:**
- `file`: CSV file with training data

**Response:**
```json
{
  "success": true,
  "message": "Data uploaded successfully. 150 samples loaded.",
  "filepath": "uploaded_data.csv"
}
```

## Data Format

### CSV Structure

Your training data CSV must include these columns:

```csv
temperature,humidity,solar_radiation,wind_speed,initial_moisture,fish_thickness,drying_rate
32.5,55,850,3.2,78,2.0,5.2
28.3,68,720,2.1,75,2.5,3.8
...
```

### Column Descriptions

| Column | Unit | Range | Description |
|--------|------|-------|-------------|
| temperature | °C | 20-45 | Ambient temperature |
| humidity | % | 30-90 | Relative humidity |
| solar_radiation | W/m² | 300-1200 | Solar irradiance |
| wind_speed | m/s | 0-8 | Wind speed |
| initial_moisture | % | 60-85 | Initial moisture content of fish |
| fish_thickness | cm | 1-5 | Average thickness of fish pieces |
| drying_rate | %/hour | 0.5-8 | Measured drying rate |

See `sample_data_template.csv` for an example.

## Machine Learning Models

### Support Vector Regression (SVR)
- **Kernel:** RBF (Radial Basis Function)
- **Parameters:** C=100, gamma=0.1, epsilon=0.1
- **Best for:** General-purpose predictions with non-linear relationships
- **Pros:** Robust to outliers, handles high-dimensional data well
- **Cons:** Computationally intensive for large datasets

### Decision Tree Regressor
- **Parameters:** max_depth=10, min_samples_split=5
- **Best for:** Understanding feature importance
- **Pros:** Easy to interpret, fast predictions
- **Cons:** Can overfit without proper tuning

### Artificial Neural Network (ANN)
- **Architecture:** 64→32→16 neurons (3 hidden layers)
- **Activation:** ReLU
- **Optimizer:** Adam
- **Best for:** Maximum accuracy with complex patterns
- **Pros:** Learns complex non-linear relationships
- **Cons:** Requires more training data, less interpretable

### Ensemble Prediction
The final prediction averages all three models, providing:
- Better accuracy than individual models
- Reduced variance and overfitting
- More robust predictions

## Collecting Real Data

The system starts with 200 synthetic samples for testing. For accurate predictions specific to your solar dryer:

1. **Setup sensors** to measure:
   - Temperature (DHT22 sensor ~$5)
   - Humidity (DHT22 sensor ~$5)
   - Solar radiation (Pyranometer ~$50-200)
   - Wind speed (Anemometer ~$20-50)

2. **Measure drying rates**:
   - Weigh fish samples before drying
   - Weigh every hour during drying
   - Calculate moisture loss rate

3. **Collect 20+ drying sessions** under different conditions

4. **Upload your data** via the web interface

5. **Retrain models** with your real data

See `DATA_COLLECTION_GUIDE.md` for detailed instructions.

## Testing the Installation

Run the test script to verify everything is installed correctly:

```bash
python test_installation.py
```

This checks:
- Python version (3.8+)
- All required packages
- ML model functionality
- Flask configuration
- Data processing capabilities

## Troubleshooting

### Backend won't start

**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Frontend can't connect

**Problem:** "Backend not connected"

**Solution:**
1. Ensure backend is running: `python backend.py`
2. Check the console for errors
3. Verify port 5000 is not in use by another application

### Models not training

**Problem:** Training fails or gets stuck

**Solution:**
1. Check you have enough RAM (4GB minimum)
2. Verify Python version is 3.8+
3. Try with smaller dataset first
4. Check error messages in backend console

### Port already in use

**Problem:** `OSError: [Errno 48] Address already in use`

**Solution:**
```bash
# Find and kill the process using port 5000
lsof -ti:5000 | xargs kill -9

# Or change the port in backend.py:
app.run(debug=True, port=5001)  # Use different port
```

### Predictions seem inaccurate

**Problem:** Unrealistic prediction values

**Solution:**
1. Ensure you've trained the models (click "Train Models")
2. Check input parameters are in valid ranges
3. If using custom data, verify CSV format is correct
4. Ensure you have enough training samples (100+ recommended)

## Development

### Project Structure

```
.
├── backend.py                 # Flask backend with ML models
├── frontend.jsx               # React frontend application
├── requirements.txt           # Python dependencies
├── start_backend.sh          # Unix startup script
├── start_backend.bat         # Windows startup script
├── test_installation.py      # Installation verification
├── sample_data_template.csv  # Example data format
├── README.md                 # This file
├── QUICKSTART.md            # Quick setup guide
└── DATA_COLLECTION_GUIDE.md # Data collection instructions
```

### Running in Production

For production deployment:

1. **Use a production WSGI server** (not Flask's built-in server):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 backend:app
   ```

2. **Enable HTTPS** for security

3. **Use environment variables** for configuration

4. **Set up proper logging** and monitoring

5. **Deploy frontend** to a static hosting service

## Requirements

### System Requirements
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- Modern web browser (Chrome, Firefox, Safari)

### Python Packages
- Flask 3.0.0
- flask-cors 4.0.0
- numpy 1.24.3
- pandas 2.0.3
- scikit-learn 1.3.0
- joblib 1.3.2

### For Data Collection (Optional)
- Temperature/humidity sensor ($5-15)
- Solar radiation sensor ($50-200)
- Wind speed sensor ($20-50)
- Digital scale ($15-30)

## Contributing

To improve this system:

1. Collect more real-world data
2. Experiment with different ML models
3. Add new features (wind direction, fish species, etc.)
4. Improve the UI/UX
5. Add more validation and error handling

## License

MIT License - Feel free to use and modify for your research and projects.

## Acknowledgments

Built with:
- scikit-learn for machine learning
- Flask for the backend API
- React for the frontend interface
- Recharts for data visualization

## Support

For questions or issues:
1. Check the troubleshooting section above
2. Review `QUICKSTART.md` for setup help
3. See `DATA_COLLECTION_GUIDE.md` for data collection
4. Check that all tests pass: `python test_installation.py`

## Citation

If you use this system in your research, please cite:

```
Solar Fish Dryer ML System
A machine learning approach to predicting drying rates in solar fish dryers
2024
```

---

**Good luck with your solar fish drying project! 🐟☀️**
