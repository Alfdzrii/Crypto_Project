@echo off
REM Quick Start Script for IDS ML Dashboard
REM This script helps you get started quickly

echo ============================================================
echo IDS MACHINE LEARNING DASHBOARD - QUICK START
echo ============================================================
echo.

REM Check if training data exists
if not exist "data\training_data.csv" (
    echo [1/3] Generating training data...
    python data/generator.py --generate-training --samples 10000
    echo.
) else (
    echo [1/3] Training data already exists (skipping)
    echo.
)

REM Check if model exists
if not exist "models\trained_model.pkl" (
    echo [2/3] Training ML model...
    python models/ml_model.py
    echo.
) else (
    echo [2/3] ML model already exists (skipping)
    echo.
)

echo [3/3] Starting Flask application...
echo.
echo ============================================================
echo Dashboard will be available at: http://localhost:5000
echo ============================================================
echo.
echo IMPORTANT: To simulate real-time traffic, open a NEW terminal and run:
echo    python data/generator.py --simulate-stream
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python app.py
