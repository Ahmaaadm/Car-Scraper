@echo off
echo Starting AutoSnap Backend...
echo.

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate venv
call venv\Scripts\activate

REM Install requirements if needed
pip install -r requirements.txt --quiet

echo.
echo Server starting at http://localhost:5000
echo Press Ctrl+C to stop
echo.

python app.py

pause
