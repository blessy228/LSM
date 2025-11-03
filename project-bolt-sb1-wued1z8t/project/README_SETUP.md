# Smart Rear-View System Using Side Cameras

A futuristic automotive dashboard simulation that replaces traditional mirrors with intelligent camera-based visualization, complete with AI detection and voice alerts.

## Features

- **Dynamic Camera Switching**: Automatically switches between left, right, rear, and center camera views based on indicator or reverse gear activation
- **AI-Powered Detection**: Real-time lane detection, vehicle recognition, and blind spot warnings using OpenCV
- **Voice Feedback**: Audio alerts for all system events and warnings
- **GPS Simulation**: Mock GPS coordinates with intersection detection
- **Stunning UI**: Dark automotive-themed dashboard with neon accents and smooth animations
- **Data Logging**: All events logged to Supabase database for analysis

## Technology Stack

- **Frontend**: CustomTkinter (modern dark UI)
- **Computer Vision**: OpenCV (lane & object detection)
- **Voice**: pyttsx3 (text-to-speech)
- **Database**: Supabase (event logging)
- **Language**: Python 3.8+

## Installation

### Prerequisites

- Python 3.8 or higher
- Webcam/Camera
- pip package manager

### Setup Steps

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the project root:
   ```
   VITE_SUPABASE_URL=your_supabase_url
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

3. **Run the Application**:
   ```bash
   python src/smart_rearview_dashboard.py
   ```

## Usage Guide

### Main Controls

- **Left Indicator**: Click to activate left camera view with blinking arrow animation
- **Right Indicator**: Click to activate right camera view with blinking arrow animation
- **Reverse Gear**: Click to engage rear camera view
- **AI Detection Toggle**: Enable/disable real-time AI object and lane detection
- **Stop System**: Safely shutdown all systems

### AI Features

When AI Detection is enabled:
- Lane lines are highlighted in neon green
- Vehicles are detected with bounding boxes
- Blind spot warnings appear when objects detected in side zones
- Real-time confidence percentages displayed

### Voice Alerts

The system provides audio feedback for:
- Indicator activation: "Left/Right indicator activated. Monitoring side camera."
- Reverse gear: "Reverse gear activated. Rear camera engaged. Keep distance."
- Blind spot warnings: "Caution: Vehicle detected in blind spot."

### GPS Simulation

- Mock GPS coordinates update every 2 seconds
- Automatic intersection detection triggers enhanced awareness
- Speed simulation displays current velocity

## Project Structure

```
smart_rearview/
├── src/
│   ├── smart_rearview_dashboard.py    # Main application
│   └── modules/
│       ├── camera_handler.py          # Video feed management
│       ├── voice_module.py            # Voice alerts
│       ├── gps_simulator.py           # GPS simulation
│       ├── ai_detector.py             # AI detection layer
│       └── data_logger.py             # Supabase logging
├── requirements.txt                   # Python dependencies
└── README_SETUP.md                    # This file
```

## Database Schema

### system_logs Table

- `id`: Unique identifier
- `timestamp`: Event occurrence time
- `event_type`: INDICATOR, REVERSE, AI_DETECTION, WARNING, SYSTEM
- `details`: Event description
- `camera_view`: Active camera (left, right, rear, center)

## Demonstration Tips

### For Academic Presentation

1. **Launch**: Run the application to display the futuristic dashboard
2. **Left Indicator**: Press to see blinking arrow + instant camera switch + voice alert
3. **Right Indicator**: Demonstrate smooth transition with different color accent
4. **AI Detection**: Toggle ON to show real-time object detection with bounding boxes
5. **Reverse Gear**: Show rear camera activation with voice guidance
6. **GPS Display**: Point out dynamic coordinate updates and intersection warnings
7. **Data Logging**: Check Supabase dashboard to show logged events

### Key Highlights

- Professional automotive-grade UI design
- Real-time camera processing at 30+ FPS
- Smooth animations with blinking indicators
- Multi-threaded architecture for performance
- Voice feedback enhances safety
- Database logging provides audit trail

## Troubleshooting

### Camera Issues

- Ensure webcam is connected and not used by another application
- Try different camera indices (0, 1, 2) if default doesn't work
- Check camera permissions in system settings

### Voice Not Working

- pyttsx3 requires system TTS engines
- Windows: Uses SAPI5
- macOS: Uses NSSpeechSynthesizer
- Linux: Requires espeak or festival

### UI Display Issues

- Update CustomTkinter: `pip install --upgrade customtkinter`
- Check display scaling settings
- Ensure sufficient screen resolution (1400x900 minimum)

## Future Enhancements

- Integration with actual OBD-II data
- Night vision mode with IR filters
- Recording and playback features
- Multi-camera support (4+ cameras)
- Machine learning model training on custom datasets
- Cloud sync for multi-vehicle fleet management

## Credits

Developed as an advanced automotive driver-assist prototype demonstrating:
- Modern UI/UX design principles
- Real-time computer vision
- Multi-threaded application architecture
- Database-driven event logging
- Voice-enabled safety systems

## License

Educational/Academic Use - Smart Rear-View System Prototype
