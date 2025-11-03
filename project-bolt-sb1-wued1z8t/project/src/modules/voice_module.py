import threading
from queue import Queue
from typing import Optional

class VoiceModule:
    def __init__(self):
        self.speech_queue = Queue()
        self.is_running = False
        self.engine = None
        self._initialize_engine()

    def _initialize_engine(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)

            voices = self.engine.getProperty('voices')
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)

            self.is_running = True
            threading.Thread(target=self._speech_worker, daemon=True).start()
        except Exception as e:
            print(f"Voice module initialization failed: {e}")
            self.engine = None

    def _speech_worker(self):
        while self.is_running:
            try:
                message = self.speech_queue.get(timeout=1)
                if self.engine and message:
                    self.engine.say(message)
                    self.engine.runAndWait()
            except:
                continue

    def speak(self, message: str):
        if self.engine:
            self.speech_queue.put(message)
        else:
            print(f"[VOICE]: {message}")

    def announce_indicator(self, direction: str):
        messages = {
            'left': "Left indicator activated. Monitoring side camera.",
            'right': "Right indicator activated. Monitoring side camera.",
            'off': "Indicators deactivated. Returning to center view."
        }
        self.speak(messages.get(direction, ""))

    def announce_reverse(self, engaged: bool):
        if engaged:
            self.speak("Reverse gear activated. Rear camera engaged. Keep distance.")
        else:
            self.speak("Reverse gear disengaged. Returning to normal view.")

    def announce_warning(self, warning_type: str):
        warnings = {
            'blind_spot_left': "Caution: Vehicle detected in left blind spot.",
            'blind_spot_right': "Caution: Vehicle detected in right blind spot.",
            'obstacle_rear': "Warning: Obstacle detected behind vehicle.",
            'lane_deviation': "Lane deviation detected. Adjust steering."
        }
        self.speak(warnings.get(warning_type, "Warning detected."))

    def stop(self):
        self.is_running = False
        if self.engine:
            self.engine.stop()
