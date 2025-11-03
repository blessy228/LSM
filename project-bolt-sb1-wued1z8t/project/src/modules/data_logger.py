import os
from datetime import datetime
from typing import Optional
from supabase import create_client, Client

class DataLogger:
    def __init__(self):
        self.supabase: Optional[Client] = None
        self._initialize_supabase()

    def _initialize_supabase(self):
        try:
            supabase_url = os.getenv('VITE_SUPABASE_URL', '')
            supabase_key = os.getenv('VITE_SUPABASE_ANON_KEY', '')

            if supabase_url and supabase_key:
                self.supabase = create_client(supabase_url, supabase_key)
                print("Supabase connection initialized")
            else:
                print("Supabase credentials not found. Logging to console only.")
        except Exception as e:
            print(f"Supabase initialization failed: {e}")
            self.supabase = None

    def log_event(self, event_type: str, details: str, camera_view: str = None):
        timestamp = datetime.now().isoformat()

        log_entry = {
            'timestamp': timestamp,
            'event_type': event_type,
            'details': details,
            'camera_view': camera_view
        }

        print(f"[LOG] {timestamp} | {event_type} | {details} | View: {camera_view}")

        if self.supabase:
            try:
                self.supabase.table('system_logs').insert(log_entry).execute()
            except Exception as e:
                print(f"Failed to log to Supabase: {e}")

    def log_indicator_change(self, direction: str, state: str):
        self.log_event(
            event_type='INDICATOR',
            details=f'{direction.upper()} indicator {state}',
            camera_view=direction if state == 'ON' else 'center'
        )

    def log_reverse_gear(self, engaged: bool):
        self.log_event(
            event_type='REVERSE',
            details='Reverse gear ENGAGED' if engaged else 'Reverse gear DISENGAGED',
            camera_view='rear' if engaged else 'center'
        )

    def log_ai_detection(self, detection_type: str, count: int, view: str):
        self.log_event(
            event_type='AI_DETECTION',
            details=f'{detection_type}: {count} objects detected',
            camera_view=view
        )

    def log_warning(self, warning_type: str, severity: str = 'MEDIUM'):
        self.log_event(
            event_type='WARNING',
            details=f'{severity} - {warning_type}',
            camera_view=None
        )

    def log_system_event(self, event_description: str):
        self.log_event(
            event_type='SYSTEM',
            details=event_description,
            camera_view=None
        )
