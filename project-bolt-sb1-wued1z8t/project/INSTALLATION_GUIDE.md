# Quick Start Guide - Smart Rear-View System

## Prerequisites
- Python 3.8+
- Webcam
- pip installed

## Installation (3 Steps)

### Step 1: Install Dependencies
```bash
pip install customtkinter opencv-python pillow numpy pyttsx3 supabase python-dotenv
```

### Step 2: Set Environment Variables
The `.env` file already contains Supabase credentials. No action needed unless you want to use your own database.

### Step 3: Run the Application
```bash
cd src
python smart_rearview_dashboard.py
```

## First Time Usage

1. **Camera Permission**: Allow camera access when prompted
2. **Dashboard Opens**: You'll see the futuristic automotive interface
3. **Test Controls**:
   - Click "LEFT INDICATOR" - watch arrow blink + camera switch + voice alert
   - Click "RIGHT INDICATOR" - see right camera with different color
   - Click "REVERSE GEAR" - engage rear camera view
   - Toggle "Enable AI Detection" - see real-time object detection
4. **Observe Features**:
   - REC indicator blinks red
   - GPS coordinates update every 2 seconds
   - Speed simulation changes dynamically
5. **Stop System**: Click red "STOP SYSTEM" button when done

## Demo Script for Presentation

**Opening**: "I've built an intelligent automotive rear-view system that replaces traditional mirrors with smart cameras."

**Action 1**: "When I activate the left indicator..." [Click] → Arrow blinks, camera switches, voice says "Left indicator activated"

**Action 2**: "The AI detection layer..." [Toggle AI] → Shows lane lines, detects objects with bounding boxes

**Action 3**: "In reverse gear..." [Click Reverse] → Rear camera activates, voice warns "Keep distance"

**Action 4**: "All events are logged..." [Show Supabase dashboard with logged events]

**Closing**: "This demonstrates real-time computer vision, voice alerts, and modern UI design for automotive safety."

## Common Issues

**No camera feed**: Change camera index in code (line with `start_camera(0)`) to `start_camera(1)`

**Voice not working**: System will still work, voice feedback shows in console

**UI too large**: Supported on 1400x900+ resolution screens

## System Requirements
- OS: Windows 10/11, macOS 10.14+, Linux
- RAM: 4GB minimum
- Camera: Any USB/built-in webcam
- Display: 1400x900 minimum resolution
