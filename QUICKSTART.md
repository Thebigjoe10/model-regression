# Quick Start Guide - Solar Fish Dryer ML System

Get up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher installed
- Web browser (Chrome, Firefox, or Safari)
- Internet connection

## Step 1: Install Python Packages (1 minute)

Open your terminal and run:

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-3.0.0 flask-cors-4.0.0 numpy-1.24.3 pandas-2.0.3 scikit-learn-1.3.0 joblib-1.3.2
```

## Step 2: Verify Installation (30 seconds)

```bash
python test_installation.py
```

**Expected output:**
```
🔬 Solar Fish Dryer ML System - Installation Test
==================================================
🐍 Checking Python Version...
  ✅ Python version is compatible (3.8+)
...
🎉 SUCCESS! Your system is ready to use!
```

If you see any ❌ errors, run `pip install -r requirements.txt` again.

## Step 3: Start the Backend (30 seconds)

**Mac/Linux:**
```bash
./start_backend.sh
```

**Windows:**
```
start_backend.bat
```

**Or manually:**
```bash
python backend.py
```

**Expected output:**
```
Generating sample data for training...
Training SVR model...
Training Decision Tree model...
Training ANN model...

=== Training Complete ===
SVR - RMSE: 0.321, R²: 0.945
Decision Tree - RMSE: 0.298, R²: 0.952
ANN - RMSE: 0.287, R²: 0.958

=== Solar Fish Dryer ML Backend ===
Server starting on http://localhost:5000
```

**Keep this terminal open!** The backend needs to keep running.

## Step 4: Open the Frontend (1 minute)

1. Open a new browser tab
2. Go to Claude.ai
3. Start a new conversation
4. Paste the contents of `frontend.jsx`
5. Claude will render the interactive web interface

**Alternative:** If you have a React development environment, you can run the frontend there.

## Step 5: Make Your First Prediction (1 minute)

1. In the web interface, you should see:
   - "Backend Connected" (green)
   - "Models Trained" (blue)

2. Adjust the input parameters:
   - Temperature: 32°C
   - Humidity: 55%
   - Solar Radiation: 850 W/m²
   - Wind Speed: 3.2 m/s
   - Initial Moisture: 78%
   - Fish Thickness: 2.0 cm

3. Click **"Predict Drying Rate"**

4. See the results:
   - Individual model predictions
   - Ensemble prediction
   - Estimated drying time
   - Charts showing moisture over time

**Congratulations!** You've successfully made your first prediction!

## What Just Happened?

1. **Backend trained 3 ML models** on 200 synthetic samples
2. **Frontend connected** to the backend via HTTP
3. **Models made predictions** based on your inputs
4. **Results displayed** with visualizations

## Next Steps

### Try Different Scenarios

Experiment with different conditions:

**Hot, dry, sunny day:**
- Temperature: 38°C
- Humidity: 40%
- Solar Radiation: 1100 W/m²
- Wind Speed: 4.5 m/s
- Expected: Very fast drying (6-7 %/hour)

**Cool, humid, cloudy day:**
- Temperature: 24°C
- Humidity: 80%
- Solar Radiation: 400 W/m²
- Wind Speed: 1.0 m/s
- Expected: Slow drying (2-3 %/hour)

### Upload Your Own Data

1. Collect real measurements from your solar dryer
2. Format as CSV (see `sample_data_template.csv`)
3. Click "Upload Your Data (CSV)" in the web interface
4. Click "Train / Retrain Models"
5. Get predictions specific to YOUR dryer!

### Understand the Models

- **SVR:** Best for general predictions
- **Decision Tree:** Shows which factors matter most
- **ANN:** Highest accuracy with enough data
- **Ensemble:** Most reliable (recommended)

## Troubleshooting

### Backend shows "ModuleNotFoundError"

**Problem:** Missing Python packages

**Solution:**
```bash
pip install -r requirements.txt
```

### Frontend shows "Backend Disconnected"

**Problem:** Backend not running

**Solution:**
1. Check the terminal where you ran `python backend.py`
2. Look for errors
3. Ensure you see "Server starting on http://localhost:5000"

### Frontend shows "Models Not Trained"

**Problem:** Models haven't been trained yet

**Solution:**
1. Click "Train / Retrain Models" button
2. Wait 5-10 seconds for training to complete
3. You'll see "Models trained successfully!"

### Port 5000 already in use

**Problem:** Another app is using port 5000

**Solution A - Kill the other process:**
```bash
# Mac/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solution B - Use a different port:**

Edit `backend.py` line 365:
```python
app.run(debug=True, port=5001)  # Changed from 5000 to 5001
```

Then edit `frontend.jsx` line 25:
```javascript
const API_URL = 'http://localhost:5001/api';  // Changed from 5000 to 5001
```

### Predictions seem random

**Problem:** Models not properly trained

**Solution:**
1. Click "Train / Retrain Models"
2. Wait for "Models trained successfully!" message
3. Check metrics show good R² scores (>0.85)

## Quick Reference

### Starting the System

```bash
# 1. Install (once)
pip install -r requirements.txt

# 2. Start backend (every time)
python backend.py

# 3. Open frontend.jsx in browser
```

### Stopping the System

```bash
# Press Ctrl+C in the terminal running backend.py
```

### Retraining Models

1. Upload new CSV data (or keep using sample data)
2. Click "Train / Retrain Models"
3. Wait for success message
4. Make new predictions

### API Quick Test

Test the backend directly:

```bash
# Health check
curl http://localhost:5000/api/health

# Make a prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 32,
    "humidity": 55,
    "solar_radiation": 850,
    "wind_speed": 3.2,
    "initial_moisture": 78,
    "fish_thickness": 2.0
  }'
```

## Files Overview

| File | Purpose | When to Use |
|------|---------|-------------|
| `backend.py` | ML server | Run this first |
| `frontend.jsx` | Web interface | Open in browser |
| `requirements.txt` | Python packages | For installation |
| `test_installation.py` | Check setup | After installing |
| `start_backend.sh` | Auto-start (Unix) | Quick launch |
| `start_backend.bat` | Auto-start (Windows) | Quick launch |
| `sample_data_template.csv` | Data example | Format reference |

## Performance Expectations

With sample data (200 samples):
- Training time: 5-10 seconds
- Prediction time: <100ms
- Model accuracy: R² = 0.90-0.95
- RMSE: 0.25-0.35 %/hour

With real data (100+ samples):
- Training time: 5-15 seconds
- Prediction time: <100ms
- Model accuracy: R² = 0.85-0.98 (varies)
- RMSE: 0.20-0.50 %/hour (varies)

## Getting Help

1. **Installation issues?** → Run `python test_installation.py`
2. **Backend issues?** → Check terminal output for errors
3. **Frontend issues?** → Check browser console (F12)
4. **Data format issues?** → Compare with `sample_data_template.csv`
5. **Still stuck?** → Read the full `README.md`

## What's Next?

Once you have the system running:

1. **Read `DATA_COLLECTION_GUIDE.md`** to learn how to collect real data
2. **Experiment** with different parameters
3. **Collect data** from your actual solar dryer
4. **Upload and retrain** with real measurements
5. **Get accurate predictions** for your specific setup!

---

**Estimated total time: 5 minutes**

**You should now have a working ML system for solar fish dryer predictions!**

Need more details? Check the full documentation in `README.md`.
