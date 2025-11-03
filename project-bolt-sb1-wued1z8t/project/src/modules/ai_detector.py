import cv2
import numpy as np
from typing import List, Dict

class AIDetector:
    def __init__(self):
        self.detection_enabled = False
        self.cascade_classifier = None
        self._initialize_detectors()

    def _initialize_detectors(self):
        try:
            self.cascade_classifier = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
        except Exception as e:
            print(f"AI Detector initialization warning: {e}")

    def detect_lane_lines(self, frame) -> List[np.ndarray]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        height, width = edges.shape
        mask = np.zeros_like(edges)
        polygon = np.array([[
            (0, height),
            (width // 2 - 50, height // 2),
            (width // 2 + 50, height // 2),
            (width, height)
        ]], np.int32)
        cv2.fillPoly(mask, polygon, 255)
        masked_edges = cv2.bitwise_and(edges, mask)

        lines = cv2.HoughLinesP(
            masked_edges,
            rho=2,
            theta=np.pi / 180,
            threshold=50,
            minLineLength=40,
            maxLineGap=100
        )

        return lines if lines is not None else []

    def draw_lane_lines(self, frame, lines: List[np.ndarray]):
        line_image = np.zeros_like(frame)

        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 170), 3)

        return cv2.addWeighted(frame, 0.8, line_image, 1, 0)

    def detect_vehicles(self, frame) -> List[Dict]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        vehicles = []

        height, width = frame.shape[:2]
        roi_y = height // 3
        roi = gray[roi_y:, :]

        blur = cv2.GaussianBlur(roi, (5, 5), 0)
        edges = cv2.Canny(blur, 30, 100)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if 1500 < area < 20000:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / float(h) if h > 0 else 0

                if 0.8 < aspect_ratio < 3.0:
                    vehicles.append({
                        'x': x,
                        'y': y + roi_y,
                        'w': w,
                        'h': h,
                        'area': area,
                        'confidence': min(area / 5000, 1.0)
                    })

        return vehicles

    def draw_vehicle_detections(self, frame, vehicles: List[Dict]):
        for vehicle in vehicles:
            x, y, w, h = vehicle['x'], vehicle['y'], vehicle['w'], vehicle['h']
            confidence = vehicle['confidence']

            color = (0, 255, 0) if confidence > 0.7 else (0, 165, 255)

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

            label = f"Vehicle {int(confidence * 100)}%"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return frame

    def check_blind_spot(self, frame, current_view: str) -> Dict:
        height, width = frame.shape[:2]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if current_view == "left":
            roi = gray[:, :width // 2]
            side = "left"
        elif current_view == "right":
            roi = gray[:, width // 2:]
            side = "right"
        else:
            return {'warning': False, 'side': None}

        blur = cv2.GaussianBlur(roi, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        large_objects = [c for c in contours if cv2.contourArea(c) > 3000]

        return {
            'warning': len(large_objects) > 0,
            'side': side,
            'object_count': len(large_objects)
        }

    def enable_detection(self, enabled: bool):
        self.detection_enabled = enabled

    def is_enabled(self) -> bool:
        return self.detection_enabled
