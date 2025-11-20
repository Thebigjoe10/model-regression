@echo off
echo ======================================
echo Solar Fish Dryer ML System - Startup
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
echo Checking dependencies...
python -c "import flask, sklearn, pandas" 2>nul
if errorlevel 1 (
    echo Dependencies not installed
    echo Installing requirements...
    pip install -r requirements.txt
    echo Dependencies installed
) else (
    echo Dependencies already installed
)

echo.
echo Starting backend server...
echo    Access at: http://localhost:5000
echo    Press Ctrl+C to stop
echo.

python backend.py

pause
