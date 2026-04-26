## 🚀 **START HERE** - Garmin Health Analyzer

Welcome! This app analyzes your Garmin watch data to understand stress, HRV, and heart rate patterns.

---

## 📍 Where to Go?

### 🆕 **First Time Setup?**
→ Read: [QUICKSTART.md](QUICKSTART.md) (5 minutes)

### 🔧 **Need Detailed Setup?**
→ Read: [SETUP.md](SETUP.md)

### 📊 **How do I export from my Garmin?**
→ Read: [DATA_EXPORT_GUIDE.md](DATA_EXPORT_GUIDE.md)

### 🏗️ **Want to understand the architecture?**
→ Read: [ARCHITECTURE.md](ARCHITECTURE.md)

### 🌐 **Ready to deploy to production?**
→ Read: [DEPLOYMENT.md](DEPLOYMENT.md)

### 📋 **Project complete! What's included?**
→ Read: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### 📖 **Full project details?**
→ Read: [README.md](README.md)

---

## ⚡ Quick Start (Choose One)

### Option A: Auto-Setup (Recommended)
```bash
# macOS/Linux
chmod +x setup.sh && ./setup.sh

# Windows
setup.bat
```

### Option B: Manual Setup
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

Then:
1. Backend runs on http://localhost:5000
2. Frontend opens at http://localhost:3000

---

## 📂 File Structure

```
garmin-health-analyzer/
├── 📄 QUICKSTART.md          ← Start here!
├── 📄 SETUP.md               ← Detailed setup
├── 📄 DATA_EXPORT_GUIDE.md   ← Export from Garmin
├── 📄 ARCHITECTURE.md        ← How it works
├── 📄 DEPLOYMENT.md          ← Go live
├── 📄 PROJECT_SUMMARY.md     ← What's built
├── 📄 README.md              ← Project info
│
├── setup.sh / setup.bat      ← Auto-setup scripts
├── backend/                  ← Python/Flask API
├── frontend/                 ← React dashboard
└── data/                     ← Data storage
```

---

## 🎯 Typical Workflow

```
1. QUICKSTART.md
   ↓
2. Run setup script
   ↓
3. Start backend & frontend
   ↓
4. Export Garmin data
   ↓
5. Upload in dashboard
   ↓
6. View insights!
```

---

## ❓ FAQ

**Q: Do I need to run both backend and frontend?**
A: Yes! Open 2 terminals:
- Terminal 1: Backend (backend/)
- Terminal 2: Frontend (frontend/)

**Q: Where do I upload my Garmin file?**
A: Go to http://localhost:3000 after both servers start

**Q: What file formats work?**
A: TCX, CSV, or FIT files exported from Garmin Connect

**Q: Can I deploy this online?**
A: Yes! See DEPLOYMENT.md for Heroku, Docker, AWS options

**Q: I'm stuck, what do I do?**
A: 
1. Check SETUP.md for your OS
2. Verify both backend & frontend are running
3. Check the terminal for error messages
4. Restart both services

---

## 🎓 Key Features

✅ Parse Garmin data (TCX, CSV, FIT)
✅ Analyze stress patterns
✅ Track HRV recovery
✅ Visualize heart rate zones
✅ Get AI recommendations
✅ Beautiful dashboard
✅ Responsive design

---

## 🔗 Quick Links

- 📖 [Full Documentation](README.md)
- ⚙️ [Setup Instructions](SETUP.md)
- 📲 [Export Guide](DATA_EXPORT_GUIDE.md)
- 🏗️ [Architecture](ARCHITECTURE.md)
- 🚀 [Deployment](DEPLOYMENT.md)

---

## 💡 Pro Tips

1. **Use TCX format** for best results - most detailed data
2. **Start with 1-week data** - trends need some history
3. **Enable stress/HRV** on your Garmin device first
4. **Check browser console** (F12) if something breaks

---

## 🎉 Ready?

1. If **Windows**: Run `setup.bat`
2. If **macOS/Linux**: Run `./setup.sh`
3. Then follow Terminal instructions

**Questions?** Check the relevant doc above!

---

**Let's go! 🚀**
