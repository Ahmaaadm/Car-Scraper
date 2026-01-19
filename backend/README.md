# AutoSnap Backend

Vehicle image downloader for IAA Canada.

## Requirements

- **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- **Google Chrome** - [Download Chrome](https://www.google.com/chrome/)

## Setup on Windows

1. **Install Python** (make sure to check "Add Python to PATH" during installation)

2. **Open Command Prompt** (cmd) in this folder

3. **Create virtual environment:**
   ```cmd
   python -m venv venv
   ```

4. **Activate virtual environment:**
   ```cmd
   venv\Scripts\activate
   ```

5. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

6. **Run the server:**
   ```cmd
   python app.py
   ```

The server will start at `http://localhost:5000`

## Quick Start (Windows)

Double-click `start.bat` to run the server (after first-time setup).

## API Endpoints

- `GET /` - Health check
- `POST /api/scrape` - Scrape vehicle images
- `GET /api/download/<year>` - Download ZIP file
- `DELETE /api/delete/<year>` - Delete folder
