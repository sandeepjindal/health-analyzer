# 🚀 Quick Start Guide - Garmin Health Analyzer

## ⚡ 5-Minute Setup

### Prerequisites
- ✅ Python 3.9+ installed
- ✅ Node.js 16+ installed
- ✅ Garmin account with exported data

### Step 1: Clone and Navigate
```bash
cd garmin-health-analyzer
```

### Step 2: Auto-Setup (macOS/Linux)
```bash
chmod +x setup.sh
./setup.sh
```

**OR for Windows:**
```bash
setup.bat
```

### Step 3: Start Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate      # macOS/Linux
# OR
venv\Scripts\activate         # Windows

python app.py
```

Expected output:
```
 * Running on http://localhost:5001
 * Debug mode: on
```

### Step 4: Start Frontend (Terminal 2)
```bash
cd frontend
npm start
```

Browser automatically opens to **http://localhost:3000**

---

## 📱 Using the App

### Get Your Garmin Data

**Option A: Export from Garmin Connect (Recommended)**
1. Go to [connect.garmin.com](https://connect.garmin.com)
2. Activities → Select activity → Download → TCX format
3. Save the file

**Option B: Generate Test Data**
```bash
python generate_sample_data.py
# Creates: data/sample_health_data.csv
```

### Upload & Analyze

1. Go to http://localhost:3000
2. Click upload box
3. Select your `.tcx`, `.csv`, or `.fit` file
4. Click "Upload & Analyze"
5. View insights across tabs:
   - **Overview** - Key metrics & AI recommendations
   - **Stress Analysis** - High stress periods
   - **HRV Analysis** - Recovery status
   - **Heart Rate** - Training zones
   - **Activities** - Workout summary

---

## 📚 File Formats Supported

| Format | Source | Best For |
|--------|--------|----------|
| **TCX** | Garmin Connect export | Detailed workout data ⭐ |
| **CSV** | Garmin Connect, health data | Multiple data points |
| **FIT** | Direct from watch | Complete raw data |

### How to Export

**From Garmin Connect:**
```
1. Log in → Activities
2. Click activity → Download (⬇️)
3. Choose: TCX / CSV
4. Save to computer
```

**Multiple Activities:**
```
1. Activities page
2. Select multiple with checkboxes
3. Download Selected
4. Choose format
```

---

## 🎯 Key Insights You'll Get

✅ **Stress Analysis**
- When your stress peaks during the day
- Duration of high stress periods
- Personalized stress management tips

✅ **HRV (Heart Rate Variability)**
- Recovery status (Recovering/Stable/Fatigued)
- HRV category (Poor to Excellent)
- Trend (improving or declining)

✅ **Heart Rate Zones**
- Zone 1: Recovery (easy)
- Zone 2: Base (steady)
- Zone 3: Build (tempo)
- Zone 4: Hard (threshold)
- Zone 5: Max (VO2 max)

✅ **Activity Summary**
- Total workouts and calories
- Average heart rate during exercise
- Training load distribution

---

## 🆘 Troubleshooting

### "Backend won't start"
```bash
cd backend
pip install -r requirements.txt  # Reinstall deps
python app.py
```

### "Port 5000 in use"
```bash
# Edit backend/app.py, change:
# app.run(debug=True, port=5001)  # Use different port
```

### "Frontend won't load"
```bash
cd frontend
npm install  # Reinstall dependencies
npm start
```

### "No data after upload"
1. Verify file format (TCX/CSV/FIT)
2. Check file isn't empty
3. Backend is running on :5000
4. Check browser console (F12) for errors

---

## 📊 Example Workflow

```
1. Export activity from Garmin Connect (TCX)
   ↓
2. Open http://localhost:3000
   ↓
3. Upload file
   ↓
4. Backend parses and analyzes
   ↓
5. View dashboard with:
   - Stress peaks identified
   - HRV recovery trends
   - HR zone breakdown
   - Activity metrics
   ↓
6. Read AI recommendations
   ↓
7. Adjust training/recovery based on insights
```

---

## 🔧 Development

### Add New Analysis Type

1. **Add to analyzer** (`backend/analyzers/health_analyzer.py`):
```python
def analyze_new_metric(self):
    # Your analysis here
    return results
```

2. **Add API endpoint** (`backend/app.py`):
```python
@app.route('/api/new-metric', methods=['GET'])
def get_new_metric():
    return jsonify(analyzer.analyze_new_metric())
```

3. **Add frontend tab** (`frontend/src/App.js`):
```jsx
{activeTab === 'new-metric' && <section>New Metric</section>}
```

---

## 📚 Documentation Files

- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[DATA_EXPORT_GUIDE.md](DATA_EXPORT_GUIDE.md)** - How to export from Garmin
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design & components
- **[README.md](README.md)** - Project overview

---

## 🎓 Learning Resources

- [Garmin Connect](https://connect.garmin.com)
- [Heart Rate Zones Guide](https://www.garmin.com/en-US/blog/health/how-to-use-heart-rate-training-zones/)
- [Understanding HRV](https://www.whoop.com/thelocker/heart-rate-variability/)
- [Flask API Docs](https://flask.palletsprojects.com/)
- [React Docs](https://react.dev/)

---

## ✨ Tips & Tricks

💡 **Better Analysis:**
- Export 1+ weeks of data for trend detection
- Ensure stress/HRV metrics are enabled on your watch
- Regular activities improve pattern recognition

💡 **Optimization:**
- Use TCX format for most detailed data
- Start with recent activities
- Export during different activity types

💡 **Customization:**
- Modify stress thresholds in `health_analyzer.py`
- Add new metrics to CSV export
- Change color scheme in `App.css`

---

## 🚀 Next Steps

1. ✅ Run setup script
2. ✅ Start backend & frontend
3. ✅ Export your Garmin data
4. ✅ Upload and explore
5. ✅ Share insights with your coach/trainer!

---

**Ready? Let's go! 💪**

```bash
./setup.sh    # macOS/Linux
# OR
setup.bat     # Windows

# Then follow Steps 3 & 4 above
```

**Questions?** Check the troubleshooting section or read detailed docs in SETUP.md
