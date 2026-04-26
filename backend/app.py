"""
Main Flask API for Garmin Health Analyzer
"""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from processors.garmin_parser import GarminParser
from analyzers.health_analyzer import HealthAnalyzer

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Initialize processors
parser = GarminParser()
analyzer = HealthAnalyzer()


@app.route('/api/health', methods=['GET'])
def get_health_summary():
    """Get overall health summary"""
    try:
        summary = analyzer.generate_summary()
        return jsonify({
            'status': 'success',
            'data': summary
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and process Garmin data file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file
        filename = datetime.now().strftime('%Y%m%d_%H%M%S_') + file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse file
        data = parser.parse_file(filepath)
        
        # Analyze data
        insights = analyzer.analyze(data)
        
        return jsonify({
            'status': 'success',
            'filename': filename,
            'data': data.to_dict() if data else None,
            'insights': insights
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/stress-analysis', methods=['GET'])
def get_stress_analysis():
    """Get stress period analysis"""
    try:
        analysis = analyzer.analyze_stress_periods()
        return jsonify({
            'status': 'success',
            'data': analysis
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/hrv-analysis', methods=['GET'])
def get_hrv_analysis():
    """Get HRV trends and recovery analysis"""
    try:
        analysis = analyzer.analyze_hrv_trends()
        return jsonify({
            'status': 'success',
            'data': analysis
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/heart-rate-patterns', methods=['GET'])
def get_hr_patterns():
    """Get heart rate patterns and zones"""
    try:
        patterns = analyzer.analyze_heart_rate_patterns()
        return jsonify({
            'status': 'success',
            'data': patterns
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
