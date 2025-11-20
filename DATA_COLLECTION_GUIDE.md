# Data Collection Guide - Solar Fish Dryer

This guide explains how to collect real data from your solar fish dryer to train accurate ML models.

## Why Collect Real Data?

The system starts with **synthetic data** (computer-generated samples that simulate realistic behavior). This works great for testing, but for **accurate predictions specific to YOUR solar dryer**, you need real measurements.

**Benefits of using your own data:**
- Predictions accurate to within 0.2-0.4 %/hour
- Accounts for your specific dryer design
- Adapts to your local climate
- Optimizes for your fish processing methods

## Overview: What You Need

### 1. Equipment (~$50-$300 total)
- Temperature/humidity sensor
- Solar radiation meter
- Wind speed sensor
- Digital scale
- Optional: Data logger

### 2. Time Commitment
- Setup: 2-4 hours (one-time)
- Data collection: 3-4 weeks
- Measurement frequency: Every hour during drying
- Minimum sessions: 20 drying sessions

### 3. Data Requirements
- **Minimum:** 50 data points (adequate)
- **Recommended:** 100-150 data points (good)
- **Optimal:** 200+ data points (excellent)

## Step-by-Step Guide

### Phase 1: Equipment Setup

#### Required Sensors

**1. Temperature & Humidity Sensor (~$5-$15)**

Recommended: DHT22 or AM2302 sensor

```
Where to buy:
- Amazon, eBay, AliExpress
- Electronics stores
- Arduino/Raspberry Pi suppliers

Specifications:
- Temperature range: -40°C to 80°C
- Humidity range: 0-100%
- Accuracy: ±0.5°C, ±2% RH
```

**Installation:**
- Mount near the fish (but not touching)
- Shield from direct sunlight
- Ensure good air circulation
- Height: Mid-level of dryer

**2. Solar Radiation Sensor (~$50-$200)**

Option A: Professional Pyranometer ($150-$200)
- Most accurate
- Research-grade data
- Worth it for serious projects

Option B: Budget Light Sensor ($5-$20)
- TSL2591 or BH1750 sensor
- Less accurate but usable
- Calibrate against known values

Option C: Use weather data
- Free weather API (OpenWeatherMap)
- Less accurate for specific location
- Better than nothing

**Installation:**
- Mount horizontally (parallel to ground)
- Full sky view (no shadows)
- Same angle as dryer surface
- Clean regularly

**3. Wind Speed Sensor (~$20-$50)**

Recommended: Cup anemometer or hot-wire anemometer

```
Where to buy:
- Weather equipment suppliers
- Amazon
- DIY electronics stores

Specifications:
- Range: 0-10 m/s minimum
- Accuracy: ±0.5 m/s
```

**Installation:**
- Mount above dryer (1-2 meters)
- Clear of obstacles
- Secure to prevent damage
- Regular calibration

**4. Digital Scale (~$15-$30)**

For measuring fish weight and moisture

```
Specifications:
- Capacity: 5-10 kg
- Precision: ±1 gram
- Tare function
```

#### Optional Equipment

**5. Data Logger (~$20-$100)**

Options:
- Arduino Uno + SD card module (~$25)
- Raspberry Pi Zero (~$15)
- Commercial data logger ($50-$100)

**Benefits:**
- Automatic data recording
- No manual reading needed
- Better time accuracy
- Less human error

### Phase 2: Data Collection Protocol

#### Before Each Drying Session

1. **Prepare fish samples**
   - Select representative pieces
   - Measure thickness (average 5 pieces)
   - Weigh initial batch (at least 500g)
   - Record fish type

2. **Calculate initial moisture**
   ```
   Initial moisture (%) = ((Wet weight - Dry weight) / Wet weight) × 100

   For fish, typically:
   - Fresh fish: 75-85%
   - Estimate: 78% for most species
   ```

3. **Set up sensors**
   - Verify all sensors working
   - Synchronize time
   - Position correctly
   - Test readings

#### During Drying Session

**Hourly measurements (every 60 minutes):**

1. **Record sensor readings:**
   - Temperature (°C)
   - Humidity (%)
   - Solar radiation (W/m²)
   - Wind speed (m/s)

2. **Weigh fish sample:**
   - Remove from dryer
   - Weigh quickly (minimize cooling)
   - Return to dryer
   - Calculate current moisture

3. **Calculate drying rate:**
   ```
   Drying rate (%/hour) = (Previous moisture % - Current moisture %) / Time elapsed (hours)
   ```

#### Example Data Recording Sheet

```
Session: 2024-01-15
Fish type: Tilapia
Initial weight: 1000g
Initial moisture: 78%
Thickness: 2.5cm

Hour | Time  | Temp | RH  | Solar | Wind | Weight | Moisture | Drying Rate
-----|-------|------|-----|-------|------|--------|----------|------------
0    | 08:00 | 28°C | 65% | 450   | 2.1  | 1000g  | 78.0%    | -
1    | 09:00 | 30°C | 60% | 680   | 2.8  | 960g   | 74.8%    | 3.2%/hr
2    | 10:00 | 32°C | 58% | 820   | 3.2  | 918g   | 71.4%    | 3.4%/hr
3    | 11:00 | 34°C | 55% | 920   | 3.5  | 880g   | 68.2%    | 3.2%/hr
...
```

### Phase 3: Data Collection Strategy

#### Vary Conditions

To build a robust model, collect data across different conditions:

**Temperature variation:**
- Cool days (20-25°C): 5+ sessions
- Moderate days (25-35°C): 10+ sessions
- Hot days (35-45°C): 5+ sessions

**Humidity variation:**
- Dry (<50%): 7+ sessions
- Moderate (50-70%): 7+ sessions
- Humid (>70%): 6+ sessions

**Weather variation:**
- Clear sunny days: 8+ sessions
- Partly cloudy: 7+ sessions
- Overcast: 5+ sessions

**Fish variation:**
- Thin pieces (1-2cm): 7+ sessions
- Medium pieces (2-3cm): 7+ sessions
- Thick pieces (3-5cm): 6+ sessions

#### Timing Recommendations

**Week 1-2: Peak season**
- Collect during best drying conditions
- Establish baseline performance
- 10-12 sessions

**Week 3-4: Varied conditions**
- Deliberately choose different weather
- Test edge cases
- 8-10 sessions

**Total:** 20 sessions minimum

### Phase 4: Data Formatting

#### CSV File Format

Save your data as a CSV file with these exact column names:

```csv
temperature,humidity,solar_radiation,wind_speed,initial_moisture,fish_thickness,drying_rate
32.5,55,850,3.2,78,2.0,5.2
30.0,60,680,2.8,78,2.0,3.2
34.0,55,920,3.5,74.8,2.0,3.4
...
```

#### Column Specifications

| Column | Unit | Valid Range | Notes |
|--------|------|-------------|-------|
| temperature | °C | 15-50 | Ambient air temperature |
| humidity | % | 20-95 | Relative humidity |
| solar_radiation | W/m² | 0-1400 | Solar irradiance |
| wind_speed | m/s | 0-15 | Wind speed at dryer height |
| initial_moisture | % | 60-90 | Moisture at start of hour |
| fish_thickness | cm | 0.5-10 | Average thickness |
| drying_rate | %/hour | 0-10 | Calculated moisture loss rate |

#### Data Validation

Before uploading, check:

1. **No missing values**
   ```python
   # Python code to check
   import pandas as pd
   df = pd.read_csv('my_data.csv')
   print(df.isnull().sum())  # Should be all zeros
   ```

2. **Values in valid ranges**
   ```python
   # Check ranges
   assert df['temperature'].between(15, 50).all()
   assert df['humidity'].between(20, 95).all()
   assert df['solar_radiation'].between(0, 1400).all()
   # ... etc
   ```

3. **Consistent units**
   - All temperatures in Celsius (not Fahrenheit)
   - All moisture in percentage (not decimal)
   - All distances in standard units

4. **Logical relationships**
   - Higher temp + lower humidity = higher drying rate ✓
   - Higher solar radiation = higher drying rate ✓
   - Thicker fish = lower drying rate ✓

### Phase 5: Uploading and Training

#### Upload Your Data

1. Save your data as `my_fish_dryer_data.csv`
2. Open the web interface
3. Click "Upload Your Data (CSV)"
4. Select your file
5. Wait for "Data uploaded successfully" message

#### Train Models

1. Click "Train / Retrain Models"
2. Wait 10-30 seconds (depending on data size)
3. Check the model metrics:
   - **R² > 0.80:** Good model
   - **R² > 0.90:** Excellent model
   - **RMSE < 0.5:** Acceptable error
   - **RMSE < 0.3:** Great accuracy

#### Test Predictions

1. Enter typical conditions from your area
2. Click "Predict Drying Rate"
3. Compare prediction with your experience
4. If way off, check data quality

## Tips for High-Quality Data

### DO ✓

- **Calibrate sensors** before starting
- **Record metadata** (fish type, weather notes)
- **Measure consistently** (same time intervals)
- **Weigh accurately** (use same scale)
- **Vary conditions** (different weather, fish)
- **Double-check entries** (avoid typos)
- **Keep raw notes** (for troubleshooting)
- **Photograph setup** (document sensor positions)

### DON'T ✗

- **Skip measurements** (inconsistent data)
- **Mix units** (Celsius and Fahrenheit)
- **Ignore outliers** (investigate anomalies)
- **Change setup mid-session** (affects consistency)
- **Estimate values** (measure, don't guess)
- **Forget metadata** (record conditions)
- **Rush weighing** (take time for accuracy)

## Budget Options

### Minimal Setup (~$50)
- DHT22 sensor ($10)
- BH1750 light sensor ($5)
- Cheap anemometer ($25)
- Kitchen scale ($15)
- Manual logging (free)

### Recommended Setup (~$150)
- DHT22 sensor ($10)
- Silicon pyranometer ($80)
- Quality anemometer ($40)
- Precision scale ($20)
- Manual logging (free)

### Professional Setup (~$400)
- Research-grade temp/RH sensor ($50)
- Professional pyranometer ($200)
- Calibrated anemometer ($80)
- Laboratory scale ($50)
- Arduino data logger ($25)

## Data Quality Checklist

Before uploading your data:

- [ ] At least 50 data points collected
- [ ] Covers variety of weather conditions
- [ ] All sensors calibrated
- [ ] No missing values in CSV
- [ ] All values in correct units
- [ ] Columns named exactly as specified
- [ ] Drying rates calculated correctly
- [ ] Outliers investigated and verified
- [ ] CSV file opens correctly in Excel/spreadsheet
- [ ] Backup copy saved

## Example Collection Schedule

### Week 1-2: Baseline Data
- **Goal:** 12 sessions in good weather
- **Focus:** Consistent, ideal conditions
- **Fish:** Same thickness, same type

### Week 3: Variation Testing
- **Goal:** 5 sessions in varied weather
- **Focus:** Cloudy days, windy days
- **Fish:** Different thicknesses

### Week 4: Edge Cases
- **Goal:** 3 sessions in challenging conditions
- **Focus:** Very humid, very hot/cold
- **Fish:** Different species if available

### Total
- **20 sessions** × 5 hours each = 100 data points
- **Expected accuracy:** R² = 0.85-0.92
- **Time investment:** ~120 hours over 4 weeks

## Troubleshooting Data Collection

### Sensor Issues

**Readings seem wrong:**
1. Calibrate against known values
2. Check connections/power
3. Verify sensor not damaged
4. Compare with nearby weather station

**Inconsistent readings:**
1. Improve sensor shielding
2. Move away from heat sources
3. Check for loose connections
4. Ensure stable mounting

### Data Issues

**Drying rates don't make sense:**
1. Recalculate manually
2. Check weight measurements
3. Verify time intervals
4. Look for scale errors

**Too much variation:**
1. More frequent measurements
2. Better environmental control
3. Larger fish samples (reduce weighing error)
4. Improve sensor placement

## After Data Collection

Once you have quality data:

1. **Upload to system**
2. **Train models** (should take 10-30 seconds)
3. **Check metrics:**
   - R² should be >0.80
   - RMSE should be <0.5
4. **Test predictions** against known conditions
5. **Iterate:** Collect more data if needed

## Advanced: Improving Data Over Time

As you use the system:

1. **Monthly updates:** Add 5-10 new sessions/month
2. **Seasonal variation:** Cover all seasons
3. **New fish types:** Expand to different species
4. **Equipment changes:** Retrain if dryer modified

Your model will become more accurate over time!

## Questions?

Common questions:

**Q: How long does data collection take?**
A: 3-4 weeks of part-time work (1-2 hours per session)

**Q: Can I use weather station data?**
A: Yes, but less accurate. Local sensors are better.

**Q: Do I need expensive equipment?**
A: No. Budget sensors ($50 total) work well.

**Q: What if I can't measure solar radiation?**
A: Use weather data or estimate from cloud cover.

**Q: How often should I collect data?**
A: Every hour during drying. More frequent is better.

**Q: Can I collect data over multiple days?**
A: Yes! Each drying session is independent.

---

**Ready to start?** Set up your sensors and begin collecting data for the most accurate predictions!
