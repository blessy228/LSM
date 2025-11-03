import random
import time
import threading
from typing import Callable, Optional, Tuple

class GPSSimulator:
    def __init__(self):
        self.latitude = 12.9716
        self.longitude = 77.5946
        self.speed = 0.0
        self.is_running = False
        self.update_callback: Optional[Callable] = None

        self.intersections = [
            (12.9725, 77.5955),
            (12.9730, 77.5960),
            (12.9740, 77.5970),
            (12.9750, 77.5980),
        ]

    def start(self):
        self.is_running = True
        threading.Thread(target=self._update_loop, daemon=True).start()

    def _update_loop(self):
        while self.is_running:
            self.latitude += random.uniform(-0.0001, 0.0002)
            self.longitude += random.uniform(-0.0001, 0.0002)
            self.speed = random.uniform(20, 80)

            if self.update_callback:
                self.update_callback(self.latitude, self.longitude, self.speed)

            time.sleep(2)

    def get_coordinates(self) -> Tuple[float, float]:
        return (self.latitude, self.longitude)

    def get_speed(self) -> float:
        return self.speed

    def is_near_intersection(self, threshold: float = 0.001) -> bool:
        current_lat, current_lon = self.get_coordinates()

        for int_lat, int_lon in self.intersections:
            distance = ((current_lat - int_lat) ** 2 + (current_lon - int_lon) ** 2) ** 0.5
            if distance < threshold:
                return True

        return False

    def set_update_callback(self, callback: Callable):
        self.update_callback = callback

    def stop(self):
        self.is_running = False
