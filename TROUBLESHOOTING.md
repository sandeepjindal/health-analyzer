# 🔧 Troubleshooting Upload Errors

## Network Error - Diagnosis Steps

### 1. ✅ Check Backend is Running

**Terminal 1:**
```bash
cd garmin-health-analyzer/backend
source venv/bin/activate
python app.py
```

Look for:
```
 * Running on http://localhost:5000
 * Debug mode: on
```

**Verify it's accessible:**
```bash
curl http://localhost:5001/health
# Should return: {"status":"healthy"}
```

---

### 2. ✅ Check Frontend is Running

**Terminal 2:**
```bash
cd garmin-health-analyzer/frontend
npm start
```

Should open http://localhost:3000 automatically

---

### 3. ✅ Check Browser Console

When you get the error:
1. Open **DevTools** (F12 or Cmd+Opt+I)
2. Go to **Console** tab
3. Look for detailed error message
4. Copy exact error and check section below

---

## Common Errors & Fixes

### Error: "No response from server. Is backend running on port 5000?"

**Problem**: Backend not running or not accessible

**Fix:**
```bash
# Terminal 1: Check if backend is running on port 5001
lsof -i :5001
kill -9 <PID>

# Start fresh
cd garmin-health-analyzer/backend
source venv/bin/activate
python app.py
```

---

### Error: "Server error" or 500 error

**Problem**: Backend crashed or module not loaded

**Fix:**
```bash
# Check backend terminal for error messages
# Should show detailed Python traceback

# Reinstall dependencies
cd backend
source venv/bin/activate
pip install -r requirements.txt --force-reinstall

# Restart
python app.py
```

---

### Error: "Invalid file format"

**Problem**: File not in correct format

**Fix:**
- Use **TCX format** (best option)
- Export from Garmin Connect: Activities → Download → TCX
- Supported: .tcx, .csv, .fit only
- Check file extension is lowercase

---

### Error: "File parsed but contained no usable data"

**Problem**: File doesn't have compatible data

**Fix:**
1. Check file isn't empty
2. Try a different export from Garmin
3. Generate test data:
   ```bash
   python generate_sample_data.py
   # Uses: data/sample_health_data.csv
   ```

---

### Error: "CORS" related error in console

**Problem**: Frontend can't reach backend due to CORS

**Fix:**
```bash
# Backend should have CORS enabled, but if not:
# In backend/app.py around line 12, ensure:
from flask_cors import CORS
CORS(app)  # This should be present
```

---

## Diagnostic Commands

### Test Backend is Running
```bash
curl -X GET http://localhost:5001/health
```

Expected response:
```json
{"status":"healthy"}
```

### Test Backend Modules
```bash
cd backend && source venv/bin/activate
python3 -c "from app import app; print('✅ Backend OK')"
```

### Check Python/Flask Process
```bash
lsof -i :5001  # Backend should be here
```

### Check Node Process
```bash
lsof -i :3000  # Frontend should be here
```

Should show Node running on port 3000

---

## Step-by-Step Recovery

### If Everything Broken:

1. **Kill all processes:**
   ```bash
   lsof -i :5000
   lsof -i :3000
   # kill -9 <PID> for each
   ```

2. **Clean reinstall backend:**
   ```bash
   cd garmin-health-analyzer/backend
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```

3. **Clean reinstall frontend:**
   ```bash
   cd garmin-health-analyzer/frontend
   rm -rf node_modules package-lock.json
   npm install
   npm start
   ```

4. **Test:**
   - Open http://localhost:3000
   - Check DevTools Console
   - Try uploading a file

---

## Advanced Debugging

### Enable Verbose Logging

Edit `backend/app.py` and add at top:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Backend Console Logs

Look in terminal where `python app.py` is running:
- `[DEBUG]` messages show what's happening
- `[ERROR]` messages show problems
- Python tracebacks show exact errors

### Browser DevTools Network Tab

1. Open F12 → Network tab
2. Try uploading
3. Click POST request to `/api/upload`
4. Check:
   - Request Headers (should have CORS headers)
   - Response (should be JSON with error details)
   - Status code (200 = success, 400 = bad request, 500 = server error)

---

## Final Checklist

- [ ] Backend running: `curl http://localhost:5000/health` returns healthy
- [ ] Frontend running: http://localhost:3000 loads
- [ ] Browser console open while uploading (watch for errors)
- [ ] File is .tcx, .csv, or .fit format
- [ ] File is not empty and has data
- [ ] Both terminals show no error messages
- [ ] No port conflicts (5000 and 3000 available)

---

## Still Not Working?

1. **Share the error message** from browser console (F12)
2. **Share the backend terminal output** (copy full traceback)
3. **Run diagnostic:**
   ```bash
   curl -v http://localhost:5000/health
   # Shows detailed connection info
   ```

Then we can pinpoint the exact issue!
