#!/usr/bin/env python3
"""
Sample data generator for testing without Garmin device
"""
import sys
import os
from datetime import datetime, timedelta
import pandas as pd
from random import randint, uniform

def generate_sample_csv():
    """Generate sample CSV health data"""
    
    # Generate 24 hours of health data
    data = []
    base_time = datetime.now() - timedelta(days=1)
    
    for hour in range(24):
        for minute in range(0, 60, 5):  # Every 5 minutes
            timestamp = base_time + timedelta(hours=hour, minutes=minute)
            
            # Simulate realistic HR throughout day
            if 0 <= hour < 6:  # Sleep hours
                base_hr = 55
                variation = randint(-5, 5)
            elif 6 <= hour < 9:  # Morning wake up
                base_hr = 65
                variation = randint(0, 15)
            elif 9 <= hour < 17:  # Work hours
                base_hr = 75
                variation = randint(-5, 20)
            elif 17 <= hour < 19:  # Evening exercise
                base_hr = 120
                variation = randint(0, 30)
            else:  # Evening relax
                base_hr = 70
                variation = randint(-5, 10)
            
            hr = max(55, base_hr + variation)
            
            # Stress inverse to sleep, high during work
            if 0 <= hour < 6:
                stress = randint(5, 20)
            elif 6 <= hour < 9:
                stress = randint(20, 40)
            elif 9 <= hour < 17:
                stress = randint(40, 70)
            elif 17 <= hour < 19:
                stress = randint(20, 40)  # Lowers during exercise
            else:
                stress = randint(20, 40)
            
            data.append({
                'timestamp': timestamp.isoformat(),
                'heart_rate': int(hr),
                'stress_level': stress,
                'body_battery': randint(30, 100)
            })
    
    df = pd.DataFrame(data)
    output_path = 'data/sample_health_data.csv'
    os.makedirs('data', exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Generated sample data: {output_path}")
    return output_path

if __name__ == '__main__':
    try:
        generate_sample_csv()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
