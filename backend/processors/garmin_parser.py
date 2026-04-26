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
        """Parse CSV export from Garmin Connect - handles multiple formats"""
        try:
            df = pd.read_csv(filepath)
            print(f"[DEBUG] CSV columns: {list(df.columns)}")
            print(f"[DEBUG] CSV shape: {df.shape}")
            print(f"[DEBUG] First row:\n{df.iloc[0].to_dict()}")
            
            heart_rate_data = []
            stress_data = []
            hrv_data = []
            activities = []
            
            # Find timestamp column (case-insensitive, flexible matching)
            timestamp_col = None
            timestamp_patterns = ['timestamp', 'time', 'date', 'datetime', 'date_time', 'time_stamp']
            for col in df.columns:
                col_lower = col.lower().replace(' ', '').replace('_', '')
                for pattern in timestamp_patterns:
                    if pattern in col_lower:
                        timestamp_col = col
                        print(f"[DEBUG] Found timestamp column: {col}")
                        break
                if timestamp_col:
                    break
            
            # Find heart rate columns
            avg_hr_col = None
            hr_patterns = ['avg hr', 'avg_hr', 'averagehr', 'heart rate']
            for col in df.columns:
                col_lower = col.lower().replace(' ', '').replace('_', '')
                for pattern in hr_patterns:
                    if pattern.replace(' ', '').replace('_', '') in col_lower:
                        avg_hr_col = col
                        print(f"[DEBUG] Found Avg HR column: {col}")
                        break
                if avg_hr_col:
                    break
            
            max_hr_col = None
            max_hr_patterns = ['max hr', 'max_hr', 'maximumhr']
            for col in df.columns:
                col_lower = col.lower().replace(' ', '').replace('_', '')
                for pattern in max_hr_patterns:
                    if pattern.replace(' ', '').replace('_', '') in col_lower:
                        max_hr_col = col
                        print(f"[DEBUG] Found Max HR column: {col}")
                        break
                if max_hr_col:
                    break
            
            # Find stress columns
            avg_stress_col = None
            stress_patterns = ['avg stress', 'avg_stress', 'averagestress', 'stress']
            for col in df.columns:
                col_lower = col.lower().replace(' ', '').replace('_', '')
                for pattern in stress_patterns:
                    if pattern.replace(' ', '').replace('_', '') in col_lower:
                        avg_stress_col = col
                        print(f"[DEBUG] Found Avg Stress column: {col}")
                        break
                if avg_stress_col:
                    break
            
            max_stress_col = None
            for col in df.columns:
                col_lower = col.lower().replace(' ', '').replace('_', '')
                if 'maxstress' in col_lower or ('max' in col_lower and 'stress' in col_lower):
                    max_stress_col = col
                    print(f"[DEBUG] Found Max Stress column: {col}")
                    break
            
            # Find HRV column if exists
            hrv_col = None
            hrv_patterns = ['hrv', 'variability', 'rmssd']
            for col in df.columns:
                col_lower = col.lower().replace(' ', '').replace('_', '')
                for pattern in hrv_patterns:
                    if pattern in col_lower:
                        hrv_col = col
                        print(f"[DEBUG] Found HRV column: {col}")
                        break
                if hrv_col:
                    break
            
            # Parse activities (when we have activity-level data)
            if timestamp_col and (avg_hr_col or avg_stress_col):
                print(f"[DEBUG] Parsing {len(df)} activity records")
                for idx, row in df.iterrows():
                    try:
                        # Get timestamp
                        timestamp = pd.to_datetime(row[timestamp_col])
                        
                        # Extract heart rate (use average)
                        if avg_hr_col and pd.notna(row[avg_hr_col]):
                            try:
                                avg_hr = int(float(row[avg_hr_col]))
                                max_hr = int(float(row[max_hr_col])) if max_hr_col and pd.notna(row[max_hr_col]) else avg_hr
                                
                                # Add activity
                                title = row.get('Title', 'Activity') if 'Title' in df.columns else 'Activity'
                                activity_type = row.get('Activity Type', 'Unknown') if 'Activity Type' in df.columns else 'Unknown'
                                
                                # Try to get duration
                                duration_minutes = 0
                                if 'Time' in df.columns and pd.notna(row['Time']):
                                    time_str = str(row['Time'])
                                    try:
                                        parts = time_str.split(':')
                                        duration_minutes = int(parts[0]) * 60 + int(parts[1]) + int(parts[2].split('.')[0]) // 60
                                    except:
                                        pass
                                
                                calories = 0
                                if 'Calories' in df.columns and pd.notna(row['Calories']):
                                    try:
                                        calories = int(float(row['Calories']))
                                    except:
                                        pass
                                
                                activity = Activity(
                                    name=title,
                                    start_time=timestamp,
                                    end_time=timestamp,
                                    duration_minutes=duration_minutes,
                                    calories=calories,
                                    avg_hr=avg_hr,
                                    max_hr=max_hr,
                                    activity_type=activity_type
                                )
                                activities.append(activity)
                                
                                # Add to heart rate data
                                heart_rate_data.append(HeartRatePoint(timestamp, avg_hr))
                            except (ValueError, TypeError):
                                pass
                        
                        # Extract stress data
                        if avg_stress_col and pd.notna(row[avg_stress_col]):
                            try:
                                stress = int(float(row[avg_stress_col]))
                                if 0 <= stress <= 100:
                                    stress_data.append(StressPoint(timestamp, stress))
                            except (ValueError, TypeError):
                                pass
                        
                        # Extract HRV if available
                        if hrv_col and pd.notna(row[hrv_col]):
                            try:
                                hrv = float(row[hrv_col])
                                if hrv > 0:
                                    hrv_data.append(HRVPoint(timestamp, hrv))
                            except (ValueError, TypeError):
                                pass
                    
                    except Exception as row_error:
                        print(f"[DEBUG] Skipping row {idx}: {str(row_error)}")
                        pass
                
                print(f"[DEBUG] Parsed: Activities={len(activities)}, HR={len(heart_rate_data)}, Stress={len(stress_data)}, HRV={len(hrv_data)}")
            
            # Return data if we found anything
            if activities or heart_rate_data or stress_data or hrv_data:
                print(f"[DEBUG] CSV parse successful!")
                return HealthSnapshot(
                    date=datetime.now(),
                    heart_rate_data=heart_rate_data,
                    stress_data=stress_data,
                    hrv_data=hrv_data,
                    activities=activities
                )
            
            print(f"[ERROR] No usable data found. Available columns: {list(df.columns)}")
            return None
        except Exception as e:
            print(f"[ERROR] Error parsing CSV: {e}")
            import traceback
            traceback.print_exc()
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
