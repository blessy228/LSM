import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import time
from modules.camera_handler import CameraHandler
from modules.voice_module import VoiceModule
from modules.gps_simulator import GPSSimulator
from modules.ai_detector import AIDetector
from modules.data_logger import DataLogger

class SmartRearViewDashboard:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Smart Rear-View System")
        self.root.geometry("1400x900")
        self.root.configure(fg_color="#0A0A0A")

        self.camera = CameraHandler()
        self.voice = VoiceModule()
        self.gps = GPSSimulator()
        self.ai_detector = AIDetector()
        self.logger = DataLogger()

        self.left_indicator_active = False
        self.right_indicator_active = False
        self.reverse_active = False
        self.ai_enabled = False
        self.is_recording = False

        self.blink_state = False
        self.rec_blink_state = False

        self._setup_ui()
        self._start_systems()

    def _setup_ui(self):
        title_frame = ctk.CTkFrame(self.root, fg_color="#1A1A1A", height=80, corner_radius=0)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            title_frame,
            text="🚗 SMART REAR-VIEW SYSTEM",
            font=("Orbitron", 32, "bold"),
            text_color="#00FFAA"
        )
        title_label.pack(pady=20)

        main_container = ctk.CTkFrame(self.root, fg_color="#0A0A0A")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        left_panel = ctk.CTkFrame(main_container, fg_color="#1A1A1A", width=300, corner_radius=15)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        controls_label = ctk.CTkLabel(
            left_panel,
            text="CONTROLS",
            font=("Segoe UI", 18, "bold"),
            text_color="#00FFAA"
        )
        controls_label.pack(pady=(20, 10))

        self.left_indicator_btn = ctk.CTkButton(
            left_panel,
            text="◄ LEFT INDICATOR",
            font=("Segoe UI", 16, "bold"),
            fg_color="#2A2A2A",
            hover_color="#00FFAA",
            height=60,
            corner_radius=10,
            command=self.toggle_left_indicator
        )
        self.left_indicator_btn.pack(pady=10, padx=20, fill="x")

        self.right_indicator_btn = ctk.CTkButton(
            left_panel,
            text="RIGHT INDICATOR ►",
            font=("Segoe UI", 16, "bold"),
            fg_color="#2A2A2A",
            hover_color="#FF6B00",
            height=60,
            corner_radius=10,
            command=self.toggle_right_indicator
        )
        self.right_indicator_btn.pack(pady=10, padx=20, fill="x")

        self.reverse_btn = ctk.CTkButton(
            left_panel,
            text="⬇ REVERSE GEAR",
            font=("Segoe UI", 16, "bold"),
            fg_color="#2A2A2A",
            hover_color="#007BFF",
            height=60,
            corner_radius=10,
            command=self.toggle_reverse
        )
        self.reverse_btn.pack(pady=10, padx=20, fill="x")

        separator = ctk.CTkFrame(left_panel, fg_color="#00FFAA", height=2)
        separator.pack(pady=20, padx=20, fill="x")

        ai_label = ctk.CTkLabel(
            left_panel,
            text="AI FEATURES",
            font=("Segoe UI", 18, "bold"),
            text_color="#00FFAA"
        )
        ai_label.pack(pady=(10, 10))

        self.ai_toggle = ctk.CTkSwitch(
            left_panel,
            text="Enable AI Detection",
            font=("Segoe UI", 14),
            command=self.toggle_ai,
            fg_color="#00FFAA",
            progress_color="#00FFAA"
        )
        self.ai_toggle.pack(pady=10, padx=20)

        gps_frame = ctk.CTkFrame(left_panel, fg_color="#2A2A2A", corner_radius=10)
        gps_frame.pack(pady=20, padx=20, fill="x")

        gps_title = ctk.CTkLabel(
            gps_frame,
            text="📍 GPS COORDINATES",
            font=("Segoe UI", 14, "bold"),
            text_color="#FFD700"
        )
        gps_title.pack(pady=(10, 5))

        self.gps_label = ctk.CTkLabel(
            gps_frame,
            text="Lat: 0.0000\nLon: 0.0000",
            font=("Courier", 12),
            text_color="#FFFFFF"
        )
        self.gps_label.pack(pady=(5, 10))

        self.speed_label = ctk.CTkLabel(
            gps_frame,
            text="Speed: 0 km/h",
            font=("Segoe UI", 12),
            text_color="#00FFAA"
        )
        self.speed_label.pack(pady=(0, 10))

        self.stop_btn = ctk.CTkButton(
            left_panel,
            text="⏹ STOP SYSTEM",
            font=("Segoe UI", 16, "bold"),
            fg_color="#DC143C",
            hover_color="#FF0000",
            height=60,
            corner_radius=10,
            command=self.stop_system
        )
        self.stop_btn.pack(side="bottom", pady=20, padx=20, fill="x")

        center_panel = ctk.CTkFrame(main_container, fg_color="#1A1A1A", corner_radius=15)
        center_panel.pack(side="left", fill="both", expand=True)

        video_header = ctk.CTkFrame(center_panel, fg_color="#2A2A2A", height=60, corner_radius=(15, 15, 0, 0))
        video_header.pack(fill="x")
        video_header.pack_propagate(False)

        self.view_label = ctk.CTkLabel(
            video_header,
            text="CENTER VIEW",
            font=("Orbitron", 24, "bold"),
            text_color="#FFFFFF"
        )
        self.view_label.pack(side="left", padx=20, pady=15)

        self.rec_indicator = ctk.CTkLabel(
            video_header,
            text="● REC",
            font=("Segoe UI", 16, "bold"),
            text_color="#FF0000"
        )
        self.rec_indicator.pack(side="right", padx=20, pady=15)

        self.video_label = ctk.CTkLabel(center_panel, text="", fg_color="#000000")
        self.video_label.pack(fill="both", expand=True, padx=0, pady=0)

        status_frame = ctk.CTkFrame(center_panel, fg_color="#2A2A2A", height=60, corner_radius=(0, 0, 15, 15))
        status_frame.pack(fill="x")
        status_frame.pack_propagate(False)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="System Ready",
            font=("Segoe UI", 14),
            text_color="#00FFAA"
        )
        self.status_label.pack(pady=18)

    def _start_systems(self):
        self.camera.start_camera(0)
        self.gps.start()
        self.is_recording = True

        self.logger.log_system_event("Smart Rear-View System started")

        self.gps.set_update_callback(self._update_gps_display)

        threading.Thread(target=self._update_video_feed, daemon=True).start()
        threading.Thread(target=self._blink_indicators, daemon=True).start()
        threading.Thread(target=self._blink_rec, daemon=True).start()

    def _update_video_feed(self):
        while self.is_recording:
            frame = self.camera.get_current_frame()

            if frame is not None:
                if self.ai_enabled:
                    lines = self.ai_detector.detect_lane_lines(frame)
                    frame = self.ai_detector.draw_lane_lines(frame, lines)

                    vehicles = self.ai_detector.detect_vehicles(frame)
                    frame = self.ai_detector.draw_vehicle_detections(frame, vehicles)

                    blind_spot = self.ai_detector.check_blind_spot(frame, self.camera.current_view)
                    if blind_spot['warning']:
                        cv2.putText(frame, "⚠ BLIND SPOT WARNING", (10, frame.shape[0] - 20),
                                    cv2.FONT_HERSHEY_BOLD, 1, (0, 0, 255), 2)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = img.resize((1040, 650), Image.Resampling.LANCZOS)
                imgtk = ImageTk.PhotoImage(image=img)

                self.video_label.configure(image=imgtk)
                self.video_label.image = imgtk

            time.sleep(0.03)

    def _blink_indicators(self):
        while self.is_recording:
            self.blink_state = not self.blink_state

            if self.left_indicator_active:
                color = "#00FFAA" if self.blink_state else "#2A2A2A"
                self.left_indicator_btn.configure(fg_color=color)

            if self.right_indicator_active:
                color = "#FF6B00" if self.blink_state else "#2A2A2A"
                self.right_indicator_btn.configure(fg_color=color)

            time.sleep(0.5)

    def _blink_rec(self):
        while self.is_recording:
            self.rec_blink_state = not self.rec_blink_state
            color = "#FF0000" if self.rec_blink_state else "#FFFFFF"
            self.rec_indicator.configure(text_color=color)
            time.sleep(0.8)

    def toggle_left_indicator(self):
        self.left_indicator_active = not self.left_indicator_active

        if self.left_indicator_active:
            self.right_indicator_active = False
            self.reverse_active = False
            self.camera.switch_view("left")
            self.view_label.configure(text="◄ LEFT CAMERA", text_color="#00FFAA")
            self.status_label.configure(text="Left indicator ON - Monitoring left side")
            self.voice.announce_indicator("left")
            self.logger.log_indicator_change("left", "ON")
        else:
            self.camera.switch_view("center")
            self.view_label.configure(text="CENTER VIEW", text_color="#FFFFFF")
            self.status_label.configure(text="System Ready")
            self.voice.announce_indicator("off")
            self.logger.log_indicator_change("left", "OFF")

    def toggle_right_indicator(self):
        self.right_indicator_active = not self.right_indicator_active

        if self.right_indicator_active:
            self.left_indicator_active = False
            self.reverse_active = False
            self.camera.switch_view("right")
            self.view_label.configure(text="RIGHT CAMERA ►", text_color="#FF6B00")
            self.status_label.configure(text="Right indicator ON - Monitoring right side")
            self.voice.announce_indicator("right")
            self.logger.log_indicator_change("right", "ON")
        else:
            self.camera.switch_view("center")
            self.view_label.configure(text="CENTER VIEW", text_color="#FFFFFF")
            self.status_label.configure(text="System Ready")
            self.voice.announce_indicator("off")
            self.logger.log_indicator_change("right", "OFF")

    def toggle_reverse(self):
        self.reverse_active = not self.reverse_active

        if self.reverse_active:
            self.left_indicator_active = False
            self.right_indicator_active = False
            self.camera.switch_view("rear")
            self.view_label.configure(text="⬇ REAR CAMERA", text_color="#007BFF")
            self.status_label.configure(text="Reverse gear ENGAGED - Keep distance")
            self.reverse_btn.configure(fg_color="#007BFF")
            self.voice.announce_reverse(True)
            self.logger.log_reverse_gear(True)
        else:
            self.camera.switch_view("center")
            self.view_label.configure(text="CENTER VIEW", text_color="#FFFFFF")
            self.status_label.configure(text="System Ready")
            self.reverse_btn.configure(fg_color="#2A2A2A")
            self.voice.announce_reverse(False)
            self.logger.log_reverse_gear(False)

    def toggle_ai(self):
        self.ai_enabled = self.ai_toggle.get()
        self.ai_detector.enable_detection(self.ai_enabled)

        if self.ai_enabled:
            self.status_label.configure(text="AI Detection ENABLED - Analyzing environment")
            self.logger.log_system_event("AI Detection enabled")
        else:
            self.status_label.configure(text="AI Detection DISABLED")
            self.logger.log_system_event("AI Detection disabled")

    def _update_gps_display(self, lat, lon, speed):
        self.gps_label.configure(text=f"Lat: {lat:.4f}\nLon: {lon:.4f}")
        self.speed_label.configure(text=f"Speed: {int(speed)} km/h")

        if self.gps.is_near_intersection():
            self.status_label.configure(text="⚠ Approaching intersection - Extra caution")

    def stop_system(self):
        self.is_recording = False
        self.camera.stop_camera()
        self.gps.stop()
        self.voice.stop()
        self.logger.log_system_event("Smart Rear-View System stopped")
        self.root.quit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SmartRearViewDashboard()
    app.run()
