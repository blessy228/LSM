import cv2
import threading
import numpy as np
from typing import Optional, Callable

class CameraHandler:
    def __init__(self):
        self.cap: Optional[cv2.VideoCapture] = None
        self.current_view = "center"
        self.is_running = False
        self.frame = None
        self.frame_callback: Optional[Callable] = None
        self.lock = threading.Lock()

    def start_camera(self, camera_index: int = 0):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(camera_index)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.is_running = True
        threading.Thread(target=self._capture_loop, daemon=True).start()

    def _capture_loop(self):
        while self.is_running and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = self._process_frame(frame)

                if self.frame_callback:
                    self.frame_callback(self.frame)

    def _process_frame(self, frame):
        frame = cv2.flip(frame, 1)

        if self.current_view == "left":
            frame = self._add_overlay(frame, "LEFT CAMERA", (0, 255, 170))
        elif self.current_view == "right":
            frame = self._add_overlay(frame, "RIGHT CAMERA", (255, 107, 0))
        elif self.current_view == "rear":
            frame = self._add_overlay(frame, "REAR CAMERA", (0, 123, 255))
        else:
            frame = self._add_overlay(frame, "CENTER VIEW", (255, 255, 255))

        return frame

    def _add_overlay(self, frame, text: str, color: tuple):
        height, width = frame.shape[:2]

        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, 60), (10, 10, 10), -1)
        frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)

        cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_BOLD, 1.2, color, 2)

        cv2.circle(frame, (width - 30, 30), 8, (0, 0, 255), -1)
        cv2.putText(frame, "REC", (width - 80, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return frame

    def switch_view(self, view: str):
        with self.lock:
            self.current_view = view

    def get_current_frame(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def set_frame_callback(self, callback: Callable):
        self.frame_callback = callback

    def stop_camera(self):
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def detect_objects(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detected_objects = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                detected_objects.append({
                    'x': x, 'y': y, 'w': w, 'h': h,
                    'area': area,
                    'position': 'left' if x < frame.shape[1] // 3 else 'right' if x > 2 * frame.shape[1] // 3 else 'center'
                })

        return detected_objects

    def draw_detections(self, frame, objects: list, show_warnings: bool = True):
        for obj in objects:
            x, y, w, h = obj['x'], obj['y'], obj['w'], obj['h']

            color = (0, 255, 0)
            if show_warnings and obj['area'] > 5000:
                color = (0, 165, 255)

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

            label = f"{obj['position'].upper()}"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return frame
