# Garmin Health Analyzer - Setup Guide

## 📋 Table of Contents
1. Backend Setup
2. Frontend Setup
3. How to Export Data from Garmin
4. Running the Application
5. Troubleshooting

---

## 1️⃣ Backend Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation Steps

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Backend

```bash
# Start Flask development server
python app.py
```

Expected output:
```
 * Running on http://localhost:5000
 * Debug mode: on
```

The API will be available at `http://localhost:5001`

**Note**: Port 5000 is often used by Apple AirTunes on macOS, so we use 5001 instead.

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/upload` | POST | Upload and process Garmin data file |
| `/api/health` | GET | Get overall health summary |
| `/api/stress-analysis` | GET | Get stress period analysis |
| `/api/hrv-analysis` | GET | Get HRV trends and recovery |
| `/api/heart-rate-patterns` | GET | Get HR patterns and zones |
| `/health` | GET | API health check |

---

## 2️⃣ Frontend Setup

### Prerequisites
- Node.js 16 or higher
- npm (comes with Node.js)

### Installation Steps

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

---

## 3️⃣ How to Export Data from Garmin Forerunner

### Option 1: Export from Garmin Connect (Web)

1. Go to [Garmin Connect](https://connect.garmin.com)
2. Log in with your Garmin account
3. Click on **Activities** in the top menu
4. Select the activity you want to analyze
5. Click the **Download** button (⬇️)
6. Choose **TCX** or **CSV** format
7. Save the file

### Option 2: Export Multiple Activities

1. Go to Activities page
2. Select multiple activities using checkboxes
3. Click **Download Selected**
4. Choose format (TCX recommended)

### Option 3: Export Daily Health Data

1. Go to **Health Dashboard**
2. Look for **Export Data** option
3. Select date range
4. Choose **CSV** format
5. Save the file

### Supported Formats

- **TCX** (Training Center XML) - Best for detailed workout data
- **CSV** (Comma-separated values) - Best for multiple data points
- **FIT** (Garmin proprietary format) - If you have raw device exports

---

## 4️⃣ Running the Application

### Terminal 1 - Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

### Terminal 2 - Frontend

```bash
cd frontend
npm start
```

### Access the Application

Open your browser and go to: **http://localhost:3000**

---

## 5️⃣ Troubleshooting

### Issue: Backend won't start

**Solution:**
```bash
# Make sure you're in the backend directory
cd backend

# Verify virtual environment is activated
# (should see (venv) at the start of your terminal line)

# Try installing requirements again
pip install -r requirements.txt

# Run with verbose output
python -u app.py
```

### Issue: Port 5000 already in use

**Solution:**
```bash
# The app already uses port 5001 (5000 conflicts with AirTunes on macOS)

# Also update frontend API_BASE to match
```

### Issue: Frontend won't start

**Solution:**
```bash
# Clear node modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Issue: CORS errors when uploading

**Solution:**
The backend has CORS enabled, but verify in `app.py`:
```python
from flask_cors import CORS
CORS(app)  # Should be present
```

### Issue: File upload fails

**Verify:**
1. File is in supported format (TCX, CSV, FIT)
2. File size is under 50MB
3. Backend is running on port 5000
4. Check browser console for error messages

---

## 📊 Using the Dashboard

### Upload Your Data

1. Click the upload box or select a file
2. Choose a Garmin export file (TCX, CSV, or FIT)
3. Click "Upload & Analyze"
4. Wait for processing (may take a few seconds for large files)

### View Analysis

**Overview Tab:**
- Heart rate summary
- Stress levels
- HRV metrics
- Activity count
- AI-powered recommendations

**Stress Analysis Tab:**
- Average, max, and min stress levels
- High stress periods identified
- Time in high stress state
- Personalized recommendations

**HRV Analysis Tab:**
- Average HRV value
- HRV category (Poor, Below Average, Average, Good, Excellent)
- Recovery status
- Trend analysis (improving/declining)

**Heart Rate Tab:**
- Resting, average, and max heart rate
- Heart rate zones breakdown
- Time spent in each training zone

**Activities Tab:**
- List of all activities
- Duration, calories, and heart rate stats
- Total activity duration and calories

---

## 🔧 Development

### Adding New Analysis Features

1. Add new analyzer method in `backend/analyzers/health_analyzer.py`
2. Add new API endpoint in `backend/app.py`
3. Create new component in `frontend/src/`
4. Add new tab in `frontend/src/App.js`

### File Structure

```
backend/
├── app.py                  # Flask app
├── models.py              # Data models
├── processors/
│   └── garmin_parser.py   # File parsers
└── analyzers/
    └── health_analyzer.py # Analysis engine

frontend/
├── package.json
├── public/
│   └── index.html
└── src/
    ├── App.js
    ├── App.css
    ├── index.js
    └── index.css
```

---

## 📚 Next Steps

1. **Export your Garmin data** - Follow section 3️⃣
2. **Start both servers** - Follow section 4️⃣
3. **Upload your data** - Use the dashboard
4. **Analyze insights** - Explore different tabs
5. **Implement improvements** - See section 🔧

---

## 🆘 Need Help?

Check these resources:
- [Garmin Connect Help](https://support.garmin.com/en-US/faq/fa12308.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Recharts Documentation](https://recharts.org/)

---

**Happy analyzing! 🚀**
