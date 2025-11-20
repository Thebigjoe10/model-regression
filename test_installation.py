"""
Test script to verify Solar Fish Dryer ML system installation
Run this after installing requirements to check everything works
"""

import sys

def test_imports():
    """Test that all required packages are installed"""
    print("\n🔍 Testing Python Package Imports...")

    packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'scikit-learn',
        'joblib': 'joblib'
    }

    failed = []
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - NOT INSTALLED")
            failed.append(name)

    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False

    print("\n✅ All packages installed correctly!")
    return True

def test_model_training():
    """Test that models can be trained"""
    print("\n🧪 Testing Model Training...")

    try:
        from sklearn.svm import SVR
        from sklearn.tree import DecisionTreeRegressor
        from sklearn.neural_network import MLPRegressor
        import numpy as np

        # Create simple test data
        X = np.random.rand(50, 6)
        y = np.random.rand(50)

        # Test SVR
        svr = SVR(kernel='rbf')
        svr.fit(X, y)
        print("  ✅ SVR model training works")

        # Test Decision Tree
        dt = DecisionTreeRegressor()
        dt.fit(X, y)
        print("  ✅ Decision Tree training works")

        # Test ANN
        ann = MLPRegressor(hidden_layer_sizes=(10,), max_iter=100)
        ann.fit(X, y)
        print("  ✅ ANN training works")

        print("\n✅ All ML models can be trained!")
        return True

    except Exception as e:
        print(f"\n❌ Model training failed: {str(e)}")
        return False

def test_data_processing():
    """Test that data can be loaded and processed"""
    print("\n📊 Testing Data Processing...")

    try:
        import pandas as pd
        import numpy as np

        # Create test dataframe
        df = pd.DataFrame({
            'temperature': np.random.uniform(20, 40, 10),
            'humidity': np.random.uniform(30, 90, 10),
            'solar_radiation': np.random.uniform(300, 1200, 10),
            'wind_speed': np.random.uniform(0, 8, 10),
            'initial_moisture': np.random.uniform(60, 85, 10),
            'fish_thickness': np.random.uniform(1, 5, 10),
            'drying_rate': np.random.uniform(1, 7, 10)
        })

        # Test operations
        X = df.drop('drying_rate', axis=1).values
        y = df['drying_rate'].values

        print(f"  ✅ Created test dataset: {X.shape}")
        print(f"  ✅ Data processing works")

        return True

    except Exception as e:
        print(f"\n❌ Data processing failed: {str(e)}")
        return False

def test_flask():
    """Test that Flask can start"""
    print("\n🌐 Testing Flask...")

    try:
        from flask import Flask
        app = Flask(__name__)

        @app.route('/test')
        def test():
            return {'status': 'ok'}

        print("  ✅ Flask app can be created")
        print("  ✅ Routes can be defined")

        return True

    except Exception as e:
        print(f"\n❌ Flask test failed: {str(e)}")
        return False

def test_python_version():
    """Check Python version"""
    print("\n🐍 Checking Python Version...")

    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 8:
        print("  ✅ Python version is compatible (3.8+)")
        return True
    else:
        print("  ❌ Python 3.8+ required")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🔬 Solar Fish Dryer ML System - Installation Test")
    print("=" * 60)

    tests = [
        ("Python Version", test_python_version),
        ("Package Imports", test_imports),
        ("Data Processing", test_data_processing),
        ("ML Models", test_model_training),
        ("Flask Framework", test_flask)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} test crashed: {str(e)}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 SUCCESS! Your system is ready to use!")
        print("\nNext steps:")
        print("  1. Run: python backend.py")
        print("  2. Open frontend.jsx in your browser")
        print("  3. Start making predictions!")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("  - Reinstall packages: pip install -r requirements.txt")
        print("  - Update Python: Use version 3.8 or higher")
        print("  - Check virtual environment is activated")

    print("=" * 60)

if __name__ == "__main__":
    main()
