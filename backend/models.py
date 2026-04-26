"""
Data models for Garmin health metrics
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional


@dataclass
class HeartRatePoint:
    """Single heart rate measurement"""
    timestamp: datetime
    bpm: int
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'bpm': self.bpm
        }


@dataclass
class StressPoint:
    """Stress level measurement"""
    timestamp: datetime
    stress_level: int  # 0-100
    body_battery: Optional[int] = None  # Garmin Body Battery (0-100)
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'stress_level': self.stress_level,
            'body_battery': self.body_battery
        }


@dataclass
class HRVPoint:
    """Heart Rate Variability measurement"""
    timestamp: datetime
    hrv_value: float  # milliseconds
    resting_hr: Optional[int] = None
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'hrv_value': self.hrv_value,
            'resting_hr': self.resting_hr
        }


@dataclass
class Activity:
    """Single activity/workout"""
    name: str
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    calories: int
    avg_hr: int
    max_hr: int
    distance_km: Optional[float] = None
    activity_type: str = "Unknown"
    
    def to_dict(self):
        return {
            'name': self.name,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'duration_minutes': self.duration_minutes,
            'calories': self.calories,
            'avg_hr': self.avg_hr,
            'max_hr': self.max_hr,
            'distance_km': self.distance_km,
            'activity_type': self.activity_type
        }


@dataclass
class HealthSnapshot:
    """Complete health data snapshot"""
    date: datetime
    heart_rate_data: List[HeartRatePoint]
    stress_data: List[StressPoint]
    hrv_data: List[HRVPoint]
    activities: List[Activity]
    sleep_minutes: Optional[int] = None
    steps: Optional[int] = None
    
    def to_dict(self):
        return {
            'date': self.date.isoformat(),
            'heart_rate_data': [p.to_dict() for p in self.heart_rate_data],
            'stress_data': [p.to_dict() for p in self.stress_data],
            'hrv_data': [p.to_dict() for p in self.hrv_data],
            'activities': [a.to_dict() for a in self.activities],
            'sleep_minutes': self.sleep_minutes,
            'steps': self.steps
        }
