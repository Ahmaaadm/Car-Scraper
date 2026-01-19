# IAA Car Scraper

A web application to scrape and browse salvage vehicles from IAA Canada.

## Project Structure

```
Car-Scraper/
├── backend/          # Flask API server
│   ├── app.py        # Main Flask application
│   ├── scraper.py    # IAA scraper logic
│   └── requirements.txt
└── frontend/         # React Vite frontend
    └── src/
        ├── App.tsx
        ├── api.ts
        ├── types.ts
        └── components/
```

## Setup & Running

### Backend (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The API will run on http://localhost:5000

### Frontend (React Vite)

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on http://localhost:5173

## API Endpoints

- `GET /api/vehicles` - Get list of vehicles
  - Query params: `page`, `make`, `year_from`, `year_to`
- `GET /api/vehicle/<stock_number>` - Get vehicle details
- `GET /api/makes` - Get list of car makes

## Notes

The scraper includes mock data for development. The actual scraping from IAA may require additional work due to their website's dynamic content loading and potential anti-scraping measures. Consider using Selenium for more reliable scraping.
