"""
Health data analysis engine
Analyzes stress, HRV, and heart rate patterns
"""
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from models import HealthSnapshot


class HealthAnalyzer:
    """Analyze health metrics"""
    
    def __init__(self):
        self.data: Optional[HealthSnapshot] = None
    
    def load_data(self, data: HealthSnapshot):
        """Load health data"""
        self.data = data
    
    def analyze(self, data: HealthSnapshot) -> Dict[str, Any]:
        """Run complete analysis"""
        self.load_data(data)
        
        return {
            'stress_analysis': self.analyze_stress_periods(),
            'hrv_analysis': self.analyze_hrv_trends(),
            'hr_patterns': self.analyze_heart_rate_patterns(),
            'activity_summary': self.summarize_activities()
        }
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate overall health summary"""
        if not self.data:
            return {}
        
        return {
            'total_heart_rate_points': len(self.data.heart_rate_data),
            'total_stress_points': len(self.data.stress_data),
            'total_hrv_points': len(self.data.hrv_data),
            'total_activities': len(self.data.activities),
            'avg_resting_hr': self._calculate_resting_hr(),
            'stress_summary': self._get_stress_summary(),
            'hrv_summary': self._get_hrv_summary()
        }
    
    def analyze_stress_periods(self) -> Dict[str, Any]:
        """Identify high stress periods"""
        if not self.data or not self.data.stress_data:
            return {'error': 'No stress data available'}
        
        stress_values = [p.stress_level for p in self.data.stress_data]
        timestamps = [p.timestamp for p in self.data.stress_data]
        
        # Find high stress periods (> 70)
        high_stress_periods = []
        current_period = None
        
        for timestamp, stress in zip(timestamps, stress_values):
            if stress > 70:
                if current_period is None:
                    current_period = {
                        'start': timestamp,
                        'end': timestamp,
                        'peak': stress,
                        'avg': stress,
                        'duration_minutes': 0,
                        'values': [stress]
                    }
                else:
                    current_period['end'] = timestamp
                    current_period['peak'] = max(current_period['peak'], stress)
                    current_period['values'].append(stress)
            else:
                if current_period is not None:
                    current_period['avg'] = np.mean(current_period['values'])
                    current_period['duration_minutes'] = int(
                        (current_period['end'] - current_period['start']).total_seconds() / 60
                    )
                    high_stress_periods.append(current_period)
                    current_period = None
        
        return {
            'high_stress_periods': high_stress_periods,
            'avg_stress': np.mean(stress_values),
            'max_stress': max(stress_values),
            'min_stress': min(stress_values),
            'high_stress_count': sum(1 for v in stress_values if v > 70),
            'recommendations': self._stress_recommendations(np.mean(stress_values))
        }
    
    def analyze_hrv_trends(self) -> Dict[str, Any]:
        """Analyze Heart Rate Variability trends"""
        if not self.data or not self.data.hrv_data:
            return {'error': 'No HRV data available'}
        
        hrv_values = np.array([p.hrv_value for p in self.data.hrv_data])
        timestamps = [p.timestamp for p in self.data.hrv_data]
        
        # HRV trend analysis
        trend = np.polyfit(range(len(hrv_values)), hrv_values, 1)[0]
        
        return {
            'avg_hrv': float(np.mean(hrv_values)),
            'max_hrv': float(np.max(hrv_values)),
            'min_hrv': float(np.min(hrv_values)),
            'std_dev': float(np.std(hrv_values)),
            'trend': 'improving' if trend > 0 else 'declining',
            'trend_slope': float(trend),
            'hrv_category': self._categorize_hrv(np.mean(hrv_values)),
            'recovery_status': self._assess_recovery(hrv_values),
            'recommendations': self._hrv_recommendations(np.mean(hrv_values), trend)
        }
    
    def analyze_heart_rate_patterns(self) -> Dict[str, Any]:
        """Analyze HR patterns and zones"""
        if not self.data or not self.data.heart_rate_data:
            return {'error': 'No heart rate data available'}
        
        hr_values = np.array([p.bpm for p in self.data.heart_rate_data])
        timestamps = [p.timestamp for p in self.data.heart_rate_data]
        
        # Calculate HR zones (using standard Karvonen formula assumes max HR 220-age)
        # Default assumption: age ~30 (max HR ~190)
        max_hr_est = 190
        resting_hr = self._calculate_resting_hr()
        
        zones = {
            'zone1_recovery': (resting_hr, int(resting_hr + (max_hr_est - resting_hr) * 0.50)),
            'zone2_base': (int(resting_hr + (max_hr_est - resting_hr) * 0.50), int(resting_hr + (max_hr_est - resting_hr) * 0.60)),
            'zone3_build': (int(resting_hr + (max_hr_est - resting_hr) * 0.60), int(resting_hr + (max_hr_est - resting_hr) * 0.70)),
            'zone4_hard': (int(resting_hr + (max_hr_est - resting_hr) * 0.70), int(resting_hr + (max_hr_est - resting_hr) * 0.85)),
            'zone5_max': (int(resting_hr + (max_hr_est - resting_hr) * 0.85), max_hr_est)
        }
        
        # Count time in each zone
        zone_distribution = {
            'zone1_recovery': sum(1 for v in hr_values if zones['zone1_recovery'][0] <= v < zones['zone1_recovery'][1]),
            'zone2_base': sum(1 for v in hr_values if zones['zone2_base'][0] <= v < zones['zone2_base'][1]),
            'zone3_build': sum(1 for v in hr_values if zones['zone3_build'][0] <= v < zones['zone3_build'][1]),
            'zone4_hard': sum(1 for v in hr_values if zones['zone4_hard'][0] <= v < zones['zone4_hard'][1]),
            'zone5_max': sum(1 for v in hr_values if zones['zone5_max'][0] <= v <= zones['zone5_max'][1])
        }
        
        return {
            'avg_hr': float(np.mean(hr_values)),
            'max_hr': int(np.max(hr_values)),
            'min_hr': int(np.min(hr_values)),
            'resting_hr': resting_hr,
            'zones': zones,
            'zone_distribution': zone_distribution,
            'daily_pattern': self._analyze_daily_pattern(timestamps, hr_values)
        }
    
    def summarize_activities(self) -> Dict[str, Any]:
        """Summarize activities"""
        if not self.data or not self.data.activities:
            return {'error': 'No activities available'}
        
        activities = self.data.activities
        
        return {
            'total_activities': len(activities),
            'total_duration_minutes': sum(a.duration_minutes for a in activities),
            'total_calories': sum(a.calories for a in activities),
            'avg_activity_duration': int(np.mean([a.duration_minutes for a in activities])),
            'avg_heart_rate': int(np.mean([a.avg_hr for a in activities])),
            'max_heart_rate_recorded': max([a.max_hr for a in activities]),
            'activities': [a.to_dict() for a in activities]
        }
    
    # ========== Helper Methods ==========
    
    def _calculate_resting_hr(self) -> int:
        """Calculate resting heart rate (typically lowest during sleep)"""
        if not self.data or not self.data.heart_rate_data:
            return 60
        
        hr_values = [p.bpm for p in self.data.heart_rate_data]
        # Assume lowest 5% of readings are resting
        sorted_hrs = sorted(hr_values)
        resting_idx = max(0, int(len(sorted_hrs) * 0.05))
        return sorted_hrs[resting_idx]
    
    def _get_stress_summary(self) -> Dict[str, Any]:
        """Get stress summary"""
        if not self.data or not self.data.stress_data:
            return {}
        
        stress_values = [p.stress_level for p in self.data.stress_data]
        return {
            'avg': np.mean(stress_values),
            'max': max(stress_values),
            'high_stress_percentage': (sum(1 for v in stress_values if v > 70) / len(stress_values) * 100)
        }
    
    def _get_hrv_summary(self) -> Dict[str, Any]:
        """Get HRV summary"""
        if not self.data or not self.data.hrv_data:
            return {}
        
        hrv_values = [p.hrv_value for p in self.data.hrv_data]
        return {
            'avg': np.mean(hrv_values),
            'max': max(hrv_values),
            'category': self._categorize_hrv(np.mean(hrv_values))
        }
    
    def _categorize_hrv(self, avg_hrv: float) -> str:
        """Categorize HRV level"""
        if avg_hrv < 20:
            return 'Poor'
        elif avg_hrv < 50:
            return 'Below Average'
        elif avg_hrv < 100:
            return 'Average'
        elif avg_hrv < 150:
            return 'Good'
        else:
            return 'Excellent'
    
    def _assess_recovery(self, hrv_values: np.ndarray) -> str:
        """Assess recovery status based on HRV trend"""
        if len(hrv_values) < 2:
            return 'Unknown'
        
        recent = np.mean(hrv_values[-len(hrv_values)//4:])  # Last 25%
        older = np.mean(hrv_values[:len(hrv_values)//4])    # First 25%
        
        change_percent = ((recent - older) / older * 100) if older > 0 else 0
        
        if change_percent > 10:
            return 'Recovering'
        elif change_percent < -10:
            return 'Fatigued'
        else:
            return 'Stable'
    
    def _analyze_daily_pattern(self, timestamps: List, hr_values: np.ndarray) -> Dict[str, Any]:
        """Analyze HR pattern throughout the day"""
        if not timestamps:
            return {}
        
        # Group by hour
        hourly_patterns = {}
        for ts, hr in zip(timestamps, hr_values):
            hour = ts.hour
            if hour not in hourly_patterns:
                hourly_patterns[hour] = []
            hourly_patterns[hour].append(hr)
        
        pattern = {f"hour_{h:02d}": np.mean(v) for h, v in hourly_patterns.items()}
        return pattern
    
    def _stress_recommendations(self, avg_stress: float) -> List[str]:
        """Generate stress recommendations"""
        recommendations = []
        
        if avg_stress > 70:
            recommendations.append('Consider stress-reduction techniques like meditation')
            recommendations.append('Take regular breaks throughout the day')
            recommendations.append('Ensure adequate sleep (7-9 hours)')
        elif avg_stress > 50:
            recommendations.append('Maintain current stress management practices')
            recommendations.append('Consider light exercise to manage stress')
        else:
            recommendations.append('Great stress levels! Maintain your current routine')
        
        return recommendations
    
    def _hrv_recommendations(self, avg_hrv: float, trend: float) -> List[str]:
        """Generate HRV recommendations"""
        recommendations = []
        
        if trend < 0:
            recommendations.append('HRV is declining - increase recovery activities')
            recommendations.append('Consider reducing training intensity')
            recommendations.append('Prioritize sleep and relaxation')
        elif avg_hrv < 50:
            recommendations.append('HRV is lower than optimal - focus on recovery')
            recommendations.append('Increase relaxation activities like yoga or stretching')
        else:
            recommendations.append('HRV is healthy - continue current training')
            recommendations.append('You can handle moderate to high intensity workouts')
        
        return recommendations
