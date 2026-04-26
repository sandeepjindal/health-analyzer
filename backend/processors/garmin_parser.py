"""
Garmin data file parser
Supports: TCX, CSV, FIT formats
"""
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
from typing import Optional, List
from models import HealthSnapshot, HeartRatePoint, StressPoint, HRVPoint, Activity


class GarminParser:
    """Parse Garmin export files"""
    
    def parse_file(self, filepath: str) -> Optional[HealthSnapshot]:
        """Parse Garmin file based on format"""
        if filepath.endswith('.tcx'):
            return self.parse_tcx(filepath)
        elif filepath.endswith('.csv'):
            return self.parse_csv(filepath)
        elif filepath.endswith('.fit'):
            return self.parse_fit(filepath)
        else:
            raise ValueError(f"Unsupported file format: {filepath}")
    
    def parse_tcx(self, filepath: str) -> Optional[HealthSnapshot]:
        """Parse TCX (Training Center XML) files"""
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            # TCX namespace
            ns = {'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
            
            heart_rate_data = []
            activities = []
            
            # Parse activities
            for activity in root.findall('.//tcx:Activity', ns):
                activity_obj = self._parse_tcx_activity(activity, ns)
                if activity_obj:
                    activities.append(activity_obj)
                    # Extract heart rate data from trackpoints
                    for trackpoint in activity.findall('.//tcx:Trackpoint', ns):
                        hr_elem = trackpoint.find('tcx:HeartRateBpm/tcx:Value', ns)
                        time_elem = trackpoint.find('tcx:Time', ns)
                        if hr_elem is not None and time_elem is not None:
                            try:
                                timestamp = datetime.fromisoformat(time_elem.text.replace('Z', '+00:00'))
                                bpm = int(hr_elem.text)
                                heart_rate_data.append(HeartRatePoint(timestamp, bpm))
                            except:
                                pass
            
            # Create snapshot
            if activities or heart_rate_data:
                return HealthSnapshot(
                    date=datetime.now(),
                    heart_rate_data=heart_rate_data,
                    stress_data=[],
                    hrv_data=[],
                    activities=activities
                )
            return None
        except Exception as e:
            print(f"Error parsing TCX: {e}")
            return None
    
    def parse_csv(self, filepath: str) -> Optional[HealthSnapshot]:
        """Parse CSV export from Garmin Connect"""
        try:
            df = pd.read_csv(filepath)
            
            heart_rate_data = []
            stress_data = []
            hrv_data = []
            activities = []
            
            # Try to detect columns
            if 'heart_rate' in df.columns or 'Heart Rate' in df.columns:
                hr_col = 'heart_rate' if 'heart_rate' in df.columns else 'Heart Rate'
                timestamp_col = None
                for col in ['timestamp', 'Timestamp', 'time', 'Time', 'datetime']:
                    if col in df.columns:
                        timestamp_col = col
                        break
                
                if timestamp_col:
                    for _, row in df.iterrows():
                        try:
                            timestamp = pd.to_datetime(row[timestamp_col])
                            bpm = int(row[hr_col])
                            heart_rate_data.append(HeartRatePoint(timestamp, bpm))
                        except:
                            pass
            
            # Parse stress data if available
            if 'stress_level' in df.columns or 'Stress' in df.columns:
                stress_col = 'stress_level' if 'stress_level' in df.columns else 'Stress'
                timestamp_col = None
                for col in ['timestamp', 'Timestamp', 'time', 'Time', 'datetime']:
                    if col in df.columns:
                        timestamp_col = col
                        break
                
                if timestamp_col:
                    for _, row in df.iterrows():
                        try:
                            timestamp = pd.to_datetime(row[timestamp_col])
                            stress = int(row[stress_col])
                            stress_data.append(StressPoint(timestamp, stress))
                        except:
                            pass
            
            if heart_rate_data or stress_data or hrv_data:
                return HealthSnapshot(
                    date=datetime.now(),
                    heart_rate_data=heart_rate_data,
                    stress_data=stress_data,
                    hrv_data=hrv_data,
                    activities=activities
                )
            return None
        except Exception as e:
            print(f"Error parsing CSV: {e}")
            return None
    
    def parse_fit(self, filepath: str) -> Optional[HealthSnapshot]:
        """Parse FIT files from Garmin devices"""
        try:
            import fitparse
            
            fitfile = fitparse.FitFile(filepath)
            heart_rate_data = []
            activities = []
            
            for record in fitfile.records:
                if record.name == 'record':
                    # Extract heart rate from records
                    timestamp = record.get_value('timestamp')
                    heart_rate = record.get_value('heart_rate')
                    
                    if timestamp and heart_rate:
                        heart_rate_data.append(HeartRatePoint(timestamp, int(heart_rate)))
                
                elif record.name == 'session':
                    # Extract activity session data
                    activity = self._parse_fit_session(record)
                    if activity:
                        activities.append(activity)
            
            if heart_rate_data or activities:
                return HealthSnapshot(
                    date=datetime.now(),
                    heart_rate_data=heart_rate_data,
                    stress_data=[],
                    hrv_data=[],
                    activities=activities
                )
            return None
        except ImportError:
            print("fitparse not installed. Install with: pip install fitparse")
            return None
        except Exception as e:
            print(f"Error parsing FIT: {e}")
            return None
    
    def _parse_tcx_activity(self, activity_elem, ns) -> Optional[Activity]:
        """Parse single TCX activity"""
        try:
            start_time_elem = activity_elem.find('.//tcx:Lap', ns).find('tcx:StartTime', ns)
            duration_elem = activity_elem.find('.//tcx:Lap', ns).find('tcx:TotalTimeSeconds', ns)
            calories_elem = activity_elem.find('.//tcx:Lap', ns).find('tcx:Calories', ns)
            
            if not all([start_time_elem, duration_elem, calories_elem]):
                return None
            
            start_time = datetime.fromisoformat(start_time_elem.text.replace('Z', '+00:00'))
            duration_minutes = int(float(duration_elem.text)) // 60
            calories = int(calories_elem.text)
            
            # Get HR stats
            max_hr_elem = activity_elem.find('.//tcx:MaximumHeartRateBpm/tcx:Value', ns)
            avg_hr_elem = activity_elem.find('.//tcx:AverageHeartRateBpm/tcx:Value', ns)
            
            max_hr = int(max_hr_elem.text) if max_hr_elem is not None else 0
            avg_hr = int(avg_hr_elem.text) if avg_hr_elem is not None else 0
            
            return Activity(
                name=f"Activity {start_time.strftime('%Y-%m-%d %H:%M')}",
                start_time=start_time,
                end_time=start_time,
                duration_minutes=duration_minutes,
                calories=calories,
                avg_hr=avg_hr,
                max_hr=max_hr
            )
        except:
            return None
    
    def _parse_fit_session(self, session) -> Optional[Activity]:
        """Parse single FIT session"""
        try:
            start_time = session.get_value('start_time')
            total_elapsed_time = session.get_value('total_elapsed_time')
            total_calories = session.get_value('total_calories')
            max_heart_rate = session.get_value('max_heart_rate')
            avg_heart_rate = session.get_value('avg_heart_rate')
            distance = session.get_value('total_distance')
            
            if not all([start_time, total_elapsed_time, total_calories]):
                return None
            
            duration_minutes = int(total_elapsed_time) // 60
            distance_km = distance / 1000 if distance else None
            
            return Activity(
                name=f"Activity {start_time.strftime('%Y-%m-%d %H:%M')}",
                start_time=start_time,
                end_time=start_time,
                duration_minutes=duration_minutes,
                calories=total_calories,
                avg_hr=int(avg_heart_rate) if avg_heart_rate else 0,
                max_hr=int(max_heart_rate) if max_heart_rate else 0,
                distance_km=distance_km
            )
        except:
            return None
