# Garmin Health Analyzer - Project Architecture

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser (React)                      │
│                  http://localhost:3000                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Dashboard Component                                 │   │
│  │  ├─ Upload Section                                  │   │
│  │  ├─ Overview Tab (Stats & Recommendations)          │   │
│  │  ├─ Stress Analysis Tab                             │   │
│  │  ├─ HRV Analysis Tab                                │   │
│  │  ├─ Heart Rate Patterns Tab                         │   │
│  │  └─ Activities Tab                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────┬──────────────────────────────────────┘
                      │ HTTP REST API
                      │ (CORS enabled)
┌─────────────────────┴──────────────────────────────────────┐
│             Flask Backend API Server                        │
│              http://localhost:5000                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Routes:                                             │  │
│  │  POST   /api/upload → File Processing               │  │
│  │  GET    /api/health → Health Summary                │  │
│  │  GET    /api/stress-analysis → Stress Insights      │  │
│  │  GET    /api/hrv-analysis → HRV Analysis            │  │
│  │  GET    /api/heart-rate-patterns → HR Zones         │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│         ┌───────────────┼───────────────┐                   │
│         ▼               ▼               ▼                   │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐          │
│  │ Garmin     │  │ Models     │  │ Analyzers    │          │
│  │ Parser     │  │ (Data)     │  │ (Analysis)   │          │
│  │            │  │            │  │              │          │
│  │ • TCX      │  │ • Activity │  │ • Stress     │          │
│  │ • CSV      │  │ • HeartRate│  │ • HRV        │          │
│  │ • FIT      │  │ • Stress   │  │ • HR Zones   │          │
│  │            │  │ • HRV      │  │ • Patterns   │          │
│  └────────────┘  └────────────┘  └──────────────┘          │
└──────────────────────────────────────────────────────────┘
                      │
                      ▼
         ┌─────────────────────────┐
         │  Garmin Data Files      │
         │  ├─ activity.tcx        │
         │  ├─ health_data.csv     │
         │  └─ recording.fit       │
         └─────────────────────────┘
```

## 📊 Data Flow

### 1. File Upload
```
User selects file (TCX/CSV/FIT)
         │
         ▼
Frontend sends to /api/upload
         │
         ▼
GarminParser determines format
         │
         ▼
Parse file → Extract data points
         │
         ▼
Create HealthSnapshot object
         │
         ▼
HealthAnalyzer processes data
         │
         ▼
Return insights JSON
         │
         ▼
Frontend displays results
```

### 2. Analysis Pipeline
```
Raw Data Points
├─ HeartRatePoint (timestamp, bpm)
├─ StressPoint (timestamp, stress_level)
├─ HRVPoint (timestamp, hrv_value)
└─ Activity (name, duration, calories, HR stats)
         │
         ▼
HealthAnalyzer
├─ analyze_stress_periods() → High stress times
├─ analyze_hrv_trends() → Recovery status
├─ analyze_heart_rate_patterns() → Training zones
└─ summarize_activities() → Activity stats
         │
         ▼
Insights JSON
├─ stress_analysis
├─ hrv_analysis
├─ hr_patterns
└─ activity_summary
         │
         ▼
Dashboard Visualization
```

## 🔧 Component Details

### Backend Components

**app.py** - Flask Application
- Initializes Flask with CORS
- Defines all API routes
- Handles file uploads
- Manages data flow

**models.py** - Data Models
- `HeartRatePoint` - Individual HR measurement
- `StressPoint` - Stress level with body battery
- `HRVPoint` - Heart rate variability
- `Activity` - Workout/activity data
- `HealthSnapshot` - Complete daily snapshot

**processors/garmin_parser.py** - File Parsers
- `parse_tcx()` - Training Center XML format
- `parse_csv()` - Comma-separated values
- `parse_fit()` - Garmin FIT format
- Converts files to HealthSnapshot objects

**analyzers/health_analyzer.py** - Analysis Engine
- `analyze_stress_periods()` - Identifies high stress times
- `analyze_hrv_trends()` - Calculates HRV statistics
- `analyze_heart_rate_patterns()` - Determines training zones
- `summarize_activities()` - Aggregates activity data

### Frontend Components

**App.js** - Main Component
- Upload file input
- Tab navigation
- Data visualization sections
- API integration

**Tab Sections:**
- **Overview** - Stats cards with recommendations
- **Stress Analysis** - Stress periods and levels
- **HRV Analysis** - Recovery and HRV trends
- **Heart Rate** - HR zones and patterns
- **Activities** - Workout list and summary

## 🔐 Data Security

- Files uploaded to `/data/uploads/` directory
- No data sent to external services
- All analysis happens locally
- CORS configured for localhost only

## 📈 Supported Metrics

| Metric | Source | Analysis |
|--------|--------|----------|
| Heart Rate | All formats | Zones, patterns, resting HR |
| Stress Level | CSV, TCX | High periods, trends |
| HRV | CSV, FIT | Recovery, trends, category |
| Body Battery | CSV | Fatigue indicator |
| Activities | TCX, FIT | Duration, calories, intensity |
| Steps | CSV | Daily activity level |

## 🚀 Deployment Considerations

**Development:**
- Flask debug mode enabled
- Hot reload on file changes
- CORS enabled
- Logging to console

**Production:**
- Use production WSGI server (Gunicorn)
- Disable debug mode
- Enable HTTPS
- Add authentication
- Implement database
- Add rate limiting

```bash
# Production backend
pip install gunicorn
gunicorn -w 4 app:app

# Frontend build
npm run build
# Serve from build/ directory
```

## 🔄 Adding New Features

### Add New Analysis
1. Add method to `HealthAnalyzer` class
2. Add API route to `app.py`
3. Add new tab component to React
4. Call new API endpoint from React

### Add New File Format
1. Add parser method to `GarminParser`
2. Extend `parse_file()` to detect format
3. Return `HealthSnapshot` object
4. Test with sample file

### Add Database Support
1. Install SQLAlchemy
2. Create database models
3. Store HealthSnapshot in DB
4. Add history/trends endpoint

---

**Architecture designed for:**
- ✅ Modularity - Easy to add features
- ✅ Scalability - Can add database layer
- ✅ Extensibility - Support more file formats
- ✅ Maintainability - Clear separation of concerns
