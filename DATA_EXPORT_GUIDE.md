# Garmin Data Export Guide

## 🏃 For Garmin Forerunner Watches

Your Garmin Forerunner watch can sync data in multiple ways:

### Automatic Sync (Easiest)
1. Wear your watch regularly
2. Sync via Garmin Connect app on your phone
3. Data automatically uploads to Garmin Connect

### Manual Export from Device
1. Connect your Garmin Forerunner via USB to your computer
2. The watch appears as a storage device
3. Navigate to: `GARMIN/ACTIVITIES/`
4. Copy `.FIT` files to your computer

### Export from Garmin Connect Web

#### Export Single Activity
1. Visit [connect.garmin.com](https://connect.garmin.com)
2. Go to **Activities**
3. Find your activity (run, walk, cycle, etc.)
4. Click the activity title
5. Look for **Download** (gear icon or ⬇️)
6. Select format:
   - **TCX** - Contains all detailed trackpoints (recommended)
   - **CSV** - Simpler format, good for spreadsheet import
   - **GPX** - Maps/GPS tracking

#### Export Daily Health Data
1. Go to **Health Dashboard**
2. Scroll to the bottom
3. Look for **Export Data** or **Reports**
4. Select date range (last week, month, etc.)
5. Download as **CSV**

#### Bulk Export Multiple Activities
1. Go to **Activities**
2. Filter by date range (e.g., "Last 30 Days")
3. Use checkboxes to select multiple activities
4. Click **Download Selected**
5. All selected activities download as a ZIP file with TCX files

### CSV Format Tips
If exporting CSV, ensure it includes:
- Timestamp
- Heart Rate
- Stress Level (if available)
- Steps
- Calories

If your CSV is missing columns, try the TCX format instead.

### FIT File Format
`.FIT` (Flexible and Interoperable Data Transfer) is Garmin's proprietary format.
- Most detailed data
- Requires `fitparse` Python library (already included in requirements)
- Recommended for advanced analysis

---

## 📱 Via Garmin Mobile App

If you use the Garmin Connect app on your phone:

1. Open **Garmin Connect**
2. Go to **Activities**
3. Select the activity
4. Tap the **Menu** (three dots)
5. Choose **Export**
6. Select **TCX** or **CSV**
7. Share/Save to your computer

---

## ✅ Data Ready?

Once you have your file:
1. Go to http://localhost:3000
2. Upload your TCX/CSV/FIT file
3. Dashboard will automatically analyze and visualize your data!

---

**Tips:**
- TCX format has the most detailed information
- Start with recent activities (last week or month)
- The analyzer works best with 3+ days of health data
- For stress/HRV analysis, make sure your watch has these metrics enabled
