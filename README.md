# Garmin Health Analyzer

Extract and analyze health data from your Garmin Forerunner watch to understand stress periods, HRV recovery, and heart rate patterns.

## Features

- 📊 Extract health metrics from Garmin watch exports
- 💓 Analyze Heart Rate Variability (HRV) trends
- 😰 Identify stress periods and recovery
- 📈 Beautiful interactive dashboard
- 📅 Time-series analysis and patterns

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Garmin Connect account (to export data)

### Setup

1. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

### Data Export from Garmin

1. Go to [Garmin Connect](https://connect.garmin.com)
2. Navigate to Health Dashboard
3. Export your activities as TCX/CSV
4. Upload to the app

## Project Structure

```
garmin-health-analyzer/
├── backend/              # Python API
│   ├── app.py           # Main Flask app
│   ├── models.py        # Data models
│   ├── processors/      # Health data processing
│   ├── analyzers/       # Analysis engines
│   └── requirements.txt
├── frontend/            # React dashboard
├── data/                # Sample/uploaded data
└── docs/                # Documentation
```

## Roadmap

- [ ] Step 1: Backend API & data models
- [ ] Step 2: Garmin data parsers (TCX, CSV, FIT)
- [ ] Step 3: HRV & Stress analysis
- [ ] Step 4: Frontend dashboard
- [ ] Step 5: Advanced visualizations
- [ ] Step 6: Deployment

---

**Next**: Follow the step-by-step guide below
