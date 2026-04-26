# Deployment Guide - Garmin Health Analyzer

## 🚀 Deployment Options

Choose based on your needs:

| Option | Cost | Difficulty | Best For |
|--------|------|-----------|----------|
| **Local Machine** | Free | ⭐ Easy | Personal use |
| **Heroku** | Free-$50/mo | ⭐⭐ Medium | Quick cloud deployment |
| **AWS/GCP** | Variable | ⭐⭐⭐ Hard | Production scale |
| **Docker** | Free | ⭐⭐ Medium | Containerized deployment |

---

## 1️⃣ Local Deployment (macOS/Linux/Windows)

### Already Configured!
The project is ready to run locally:

```bash
./setup.sh     # macOS/Linux
# OR
setup.bat      # Windows

# Then:
# Terminal 1: cd backend && python app.py
# Terminal 2: cd frontend && npm start
```

**Pros:**
- ✅ No cost
- ✅ Full control
- ✅ Easy testing

**Cons:**
- ❌ Only accessible from your computer
- ❌ Requires manual start-stop

---

## 2️⃣ Heroku Deployment

### Prerequisites
- Heroku account (free at heroku.com)
- Heroku CLI installed

### Backend Setup

1. **Create Heroku app:**
```bash
cd backend
heroku login
heroku create your-app-name
```

2. **Set up Procfile:**
Create `backend/Procfile`:
```
web: gunicorn app:app
```

3. **Deploy:**
```bash
git push heroku main
```

### Frontend Setup

1. **Build optimized version:**
```bash
cd frontend
npm run build
```

2. **Create Heroku app for frontend:**
```bash
heroku create your-frontend-name --buildpack mars/create-react-app
```

3. **Set API endpoint:**
In `frontend/.env`:
```
REACT_APP_API_BASE=https://your-app-name.herokuapp.com/api
```

4. **Deploy:**
```bash
git push heroku main
```

### Update Frontend API Base
Modify `frontend/src/App.js`:
```javascript
const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:5000/api';
```

---

## 3️⃣ Docker Deployment

### Create Dockerfile for Backend

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

### Create Dockerfile for Frontend

Create `frontend/Dockerfile`:
```dockerfile
FROM node:16 as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:16-slim
RUN npm install -g serve
COPY --from=build /app/build /app/build
EXPOSE 3000
CMD ["serve", "-s", "/app/build", "-l", "3000"]
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_BASE=http://localhost:5000/api
    depends_on:
      - backend

volumes:
  data:
```

### Run with Docker
```bash
docker-compose up
```

---

## 4️⃣ Production Checklist

### Backend Production Settings

Update `backend/app.py`:
```python
# Production config
app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["your-frontend-domain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

if __name__ == '__main__':
    # Use gunicorn in production
    # python -m gunicorn -w 4 app:app
    app.run(debug=False, port=5000)
```

### Create `.env` file

```env
FLASK_ENV=production
DEBUG=False
MAX_CONTENT_LENGTH=52428800  # 50MB
```

### Frontend Production Build

```bash
cd frontend
npm run build
# Generates optimized build/ directory
```

---

## 🐳 AWS/GCP Deployment

### AWS Elastic Beanstalk

1. **Install EB CLI:**
```bash
pip install awsebcli
```

2. **Initialize EB:**
```bash
eb init -p python-3.9 garmin-health
```

3. **Create environment:**
```bash
eb create production
```

4. **Deploy:**
```bash
eb deploy
```

### Google Cloud Run

```bash
# Build image
docker build -t gcr.io/my-project/garmin-backend .

# Push to GCR
docker push gcr.io/my-project/garmin-backend

# Deploy
gcloud run deploy garmin-backend \
  --image gcr.io/my-project/garmin-backend \
  --platform managed \
  --region us-central1
```

---

## 📊 Performance Optimization

### Backend Optimization
```python
# Use caching
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/health')
@cache.cached(timeout=300)
def get_health_summary():
    # Cached for 5 minutes
    pass
```

### Frontend Optimization
```bash
# Enable gzip compression
npm run build
# Then configure web server to serve gzipped files

# Use code splitting
npm install @loadable/component
```

---

## 🔒 Security Checklist

- [ ] Use HTTPS in production
- [ ] Set secure CORS headers
- [ ] Validate file uploads (size, type)
- [ ] Add rate limiting
- [ ] Use environment variables for secrets
- [ ] Sanitize user inputs
- [ ] Add authentication if multi-user
- [ ] Regular security updates

### Add Rate Limiting

```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/upload', methods=['POST'])
@limiter.limit("10 per hour")
def upload_file():
    pass
```

---

## 📈 Monitoring & Logging

### Enable Application Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/garmin_health.log',
                                      maxBytes=10240000,
                                      backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Monitor with Services
- **Heroku**: Built-in metrics
- **AWS**: CloudWatch
- **GCP**: Cloud Monitoring
- **Self-hosted**: Prometheus + Grafana

---

## 🔄 Continuous Deployment

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Heroku
        run: |
          git push https://heroku:${{ secrets.HEROKU_API_KEY }}@git.heroku.com/${{ secrets.HEROKU_APP_NAME }}.git HEAD:main
```

---

## 💾 Database Migration (Future)

To add persistent storage:

```bash
pip install flask-sqlalchemy
```

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100))
    data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

## 🚨 Troubleshooting Deployment

### Issue: Port already in use
```bash
# Find process using port
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Issue: CORS errors
- Check backend CORS configuration
- Verify frontend URL matches CORS allowed origins
- Set correct API endpoint in frontend

### Issue: File upload fails
- Check file size limit (set to 50MB)
- Verify upload directory exists and has write permissions
- Check server logs for detailed errors

### Issue: Memory issues
- Use pagination for large datasets
- Implement data cleanup/archival
- Monitor with profiling tools

---

## 📚 Resources

- [Heroku Deployment Guide](https://devcenter.heroku.com/articles/python-support)
- [Docker Documentation](https://docs.docker.com/)
- [AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.3.x/tutorial/deploy/)

---

**Next Step:** Choose your deployment option and follow the corresponding section above!
